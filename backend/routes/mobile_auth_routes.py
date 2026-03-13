"""
Email/password and Google OAuth authentication for web and mobile apps.
Supports both authentication methods with password hashing.
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from pymongo.errors import PyMongoError

from database.db import DatabaseConnectionError, get_user_collection
from routes.auth_routes import (
    AUTH_SECRET_CONFIGURED,
    _build_session_user,
    _create_access_token,
    _now_utc,
    normalize_email,
    SESSION_TTL_SECONDS,
)

router = APIRouter(tags=["Email/Password Authentication"])


class EmailPasswordLoginRequest(BaseModel):
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class EmailPasswordRegisterRequest(BaseModel):
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
    name: str = Field(..., min_length=2)
    role: str = Field(default="patient")


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
    expires_at: datetime
    user: dict[str, Any]


def _hash_password(password: str) -> str:
    """Hash password using SHA-256 (simple for demo, use bcrypt in production)"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def _verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return _hash_password(password) == hashed


@router.post("/auth/login", response_model=AuthResponse)
def email_password_login(payload: EmailPasswordLoginRequest) -> AuthResponse:
    """
    Email/password login for web and mobile apps.
    Works alongside Google OAuth.
    """
    if not AUTH_SECRET_CONFIGURED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication is not configured on the server.",
        )

    email = normalize_email(payload.email)
    
    # Load user from database
    try:
        user_doc = get_user_collection().find_one(
            {"email": email},
            {"_id": 0},
        )
    except DatabaseConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while loading user.",
        ) from exc

    if user_doc is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not bool(user_doc.get("is_active", True)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is disabled. Contact admin.",
        )

    # Verify password
    stored_password_hash = user_doc.get("password_hash")
    if stored_password_hash:
        # User has password set - verify it
        if not _verify_password(payload.password, stored_password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )
    else:
        # User registered via Google OAuth - no password set
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This account uses Google Sign-In. Please login with Google.",
        )
    
    # Build session user
    session_user = _build_session_user(
        subject=user_doc.get("subject", email),
        email=email,
        name=str(user_doc.get("name", email)),
        picture=user_doc.get("picture"),
        role=str(user_doc.get("role", "")).strip().lower(),
        health_id=str(user_doc.get("health_id")) if user_doc.get("health_id") else None,
        hospital_id=str(user_doc.get("hospital_id")) if user_doc.get("hospital_id") else None,
    )

    # Update last login
    try:
        get_user_collection().update_one(
            {"email": email},
            {"$set": {"last_login_at": _now_utc()}},
        )
    except Exception:
        pass  # Non-critical

    # Create access token
    expires_at = _now_utc() + timedelta(seconds=SESSION_TTL_SECONDS)
    token = _create_access_token(user=session_user, expires_at=expires_at)

    return AuthResponse(
        access_token=token,
        refresh_token=None,
        expires_at=expires_at,
        user={
            "email": session_user.email,
            "name": session_user.name,
            "role": session_user.role,
            "picture": session_user.picture,
            "health_id": session_user.health_id,
            "hospital_id": session_user.hospital_id,
        },
    )


@router.post("/auth/register", response_model=AuthResponse)
def email_password_register(payload: EmailPasswordRegisterRequest) -> AuthResponse:
    """
    Register new user with email/password.
    Only allows patient registration by default.
    Admins can create hospital/admin accounts via admin panel.
    """
    if not AUTH_SECRET_CONFIGURED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication is not configured on the server.",
        )

    email = normalize_email(payload.email)
    
    # Check if user already exists
    try:
        existing_user = get_user_collection().find_one(
            {"email": email},
            {"_id": 0, "email": 1},
        )
    except DatabaseConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while checking user.",
        ) from exc

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    # Only allow patient registration via public endpoint
    # Admins/hospitals must be created by admin
    if payload.role.lower() not in ["patient"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only patient accounts can be self-registered. Contact admin for other roles.",
        )

    # Hash password
    password_hash = _hash_password(payload.password)
    
    # Create user document
    now = _now_utc()
    user_doc = {
        "email": email,
        "subject": email,  # Use email as subject for email/password users
        "name": payload.name.strip(),
        "password_hash": password_hash,
        "picture": None,
        "role": "patient",
        "health_id": None,  # Will be assigned when patient profile is created
        "hospital_id": None,
        "is_active": True,
        "created_at": now,
        "updated_at": now,
        "last_login_at": now,
    }

    # Insert user
    try:
        get_user_collection().insert_one(user_doc)
    except DatabaseConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while creating user.",
        ) from exc

    # Build session user
    session_user = _build_session_user(
        subject=email,
        email=email,
        name=payload.name.strip(),
        picture=None,
        role="patient",
        health_id=None,
        hospital_id=None,
    )

    # Create access token
    expires_at = _now_utc() + timedelta(seconds=SESSION_TTL_SECONDS)
    token = _create_access_token(user=session_user, expires_at=expires_at)

    return AuthResponse(
        access_token=token,
        refresh_token=None,
        expires_at=expires_at,
        user={
            "email": session_user.email,
            "name": session_user.name,
            "role": session_user.role,
            "picture": session_user.picture,
            "health_id": session_user.health_id,
            "hospital_id": session_user.hospital_id,
        },
    )
