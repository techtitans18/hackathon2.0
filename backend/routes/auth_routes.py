from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from pymongo.errors import PyMongoError

from database.db import DatabaseConnectionError, get_user_collection

try:
    from google.auth.transport import requests as google_requests
    from google.oauth2 import id_token

    GOOGLE_AUTH_AVAILABLE = True
except Exception:  # pragma: no cover - optional runtime dependency
    google_requests = None
    id_token = None
    GOOGLE_AUTH_AVAILABLE = False

ROLE_ADMIN = "admin"
ROLE_HOSPITAL = "hospital"
ROLE_PATIENT = "patient"
VALID_ROLES = {ROLE_ADMIN, ROLE_HOSPITAL, ROLE_PATIENT}
SESSION_TTL_SECONDS = 8 * 60 * 60
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID") or os.getenv("google_client_id") or ""
AUTH_SECRET_KEY = (
    os.getenv("AUTH_SECRET_KEY")
    or os.getenv("SECRET_KEY")
    or os.getenv("secret_key")
    or ""
)
MIN_SECRET_KEY_LENGTH = 32
AUTH_SECRET_CONFIGURED = len(AUTH_SECRET_KEY) >= MIN_SECRET_KEY_LENGTH
TRUSTED_ISSUERS = {"accounts.google.com", "https://accounts.google.com"}

_bootstrap_raw = (
    os.getenv("ADMIN_BOOTSTRAP_EMAILS")
    or os.getenv("ADMIN_BOOTSTRAP_EMAIL")
    or os.getenv("ADMIN_EMAILS")
    or ""
)
BOOTSTRAP_ADMIN_EMAILS = {
    email.strip().lower()
    for email in _bootstrap_raw.split(",")
    if email.strip()
}

router = APIRouter(tags=["Authentication"])


class GoogleLoginRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    credential: str = Field(..., min_length=20)


class SessionUser(BaseModel):
    subject: str
    email: str
    name: str
    role: str
    picture: str | None = None
    health_id: str | None = None
    hospital_id: str | None = None


class GoogleLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    user: SessionUser


class SessionResponse(BaseModel):
    authenticated: bool
    expires_at: datetime
    user: SessionUser


class GoogleConfigResponse(BaseModel):
    enabled: bool
    google_client_id: str


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64url_decode(raw: str) -> bytes:
    padding = "=" * ((4 - (len(raw) % 4)) % 4)
    return base64.urlsafe_b64decode(raw + padding)


def normalize_email(value: str) -> str:
    return value.strip().lower()


def _extract_bearer_token(authorization: str | None) -> str:
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header.",
        )
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must be in the format: Bearer <token>.",
        )
    return token.strip()


def _sign_payload(payload_segment: str) -> str:
    if not AUTH_SECRET_CONFIGURED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                f"AUTH_SECRET_KEY is not configured. Set at least "
                f"{MIN_SECRET_KEY_LENGTH} characters."
            ),
        )
    signature = hmac.new(
        AUTH_SECRET_KEY.encode("utf-8"),
        payload_segment.encode("ascii"),
        digestmod=hashlib.sha256,
    ).digest()
    return _b64url_encode(signature)


def _validate_role(role: str) -> str:
    normalized = role.strip().lower()
    if normalized not in VALID_ROLES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid account role in session.",
        )
    return normalized


def _build_session_user(
    *,
    subject: str,
    email: str,
    name: str,
    picture: str | None,
    role: str,
    health_id: str | None,
    hospital_id: str | None,
) -> SessionUser:
    normalized_role = _validate_role(role)
    normalized_health_id = health_id.strip() if isinstance(health_id, str) else None
    normalized_hospital_id = (
        hospital_id.strip() if isinstance(hospital_id, str) else None
    )

    if normalized_role == ROLE_PATIENT and not normalized_health_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient account is missing an assigned HealthID.",
        )

    if normalized_role == ROLE_HOSPITAL and not normalized_hospital_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hospital account is missing an assigned HospitalID.",
        )

    return SessionUser(
        subject=subject,
        email=normalize_email(email),
        name=name.strip() or normalize_email(email),
        role=normalized_role,
        picture=picture.strip() if isinstance(picture, str) and picture.strip() else None,
        health_id=normalized_health_id,
        hospital_id=normalized_hospital_id,
    )


def _create_access_token(user: SessionUser, expires_at: datetime) -> str:
    payload: dict[str, Any] = {
        "sub": user.subject,
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "picture": user.picture,
        "health_id": user.health_id,
        "hospital_id": user.hospital_id,
        "exp": int(expires_at.timestamp()),
    }
    payload_bytes = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode(
        "utf-8"
    )
    payload_segment = _b64url_encode(payload_bytes)
    signature_segment = _sign_payload(payload_segment)
    return f"{payload_segment}.{signature_segment}"


def _decode_access_token(token: str) -> SessionResponse:
    segments = token.split(".")
    if len(segments) != 2:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token format.",
        )

    payload_segment, signature_segment = segments
    expected_signature = _sign_payload(payload_segment)
    if not hmac.compare_digest(signature_segment, expected_signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token signature.",
        )

    try:
        payload_raw = _b64url_decode(payload_segment)
        payload = json.loads(payload_raw.decode("utf-8"))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token payload.",
        ) from exc

    expires_at_ts = int(payload.get("exp", 0))
    now_ts = int(_now_utc().timestamp())
    if expires_at_ts <= now_ts:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is expired. Sign in again.",
        )

    subject = str(payload.get("sub", "")).strip()
    email = normalize_email(str(payload.get("email", "")))
    name = str(payload.get("name", email)).strip() or email
    picture_raw = payload.get("picture")
    picture = str(picture_raw) if picture_raw else None
    role = str(payload.get("role", "")).strip().lower()
    health_id_raw = payload.get("health_id")
    hospital_id_raw = payload.get("hospital_id")

    if not subject or not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token user payload is incomplete.",
        )

    user = _build_session_user(
        subject=subject,
        email=email,
        name=name,
        picture=picture,
        role=role,
        health_id=str(health_id_raw) if health_id_raw else None,
        hospital_id=str(hospital_id_raw) if hospital_id_raw else None,
    )

    expires_at = datetime.fromtimestamp(expires_at_ts, tz=timezone.utc)
    return SessionResponse(authenticated=True, expires_at=expires_at, user=user)


def _load_managed_user(email: str) -> dict[str, Any] | None:
    try:
        return get_user_collection().find_one(
            {"email": normalize_email(email)},
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
            detail="Database error while resolving user account.",
        ) from exc


def _sync_managed_user_login(
    *,
    email: str,
    subject: str,
    name: str,
    picture: str | None,
    role: str,
    health_id: str | None,
    hospital_id: str | None,
) -> None:
    now = _now_utc()
    try:
        get_user_collection().update_one(
            {"email": normalize_email(email)},
            {
                "$set": {
                    "subject": subject,
                    "name": name,
                    "picture": picture,
                    "role": role,
                    "health_id": health_id,
                    "hospital_id": hospital_id,
                    "last_login_at": now,
                    "updated_at": now,
                }
            },
        )
    except DatabaseConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while updating user login metadata.",
        ) from exc


def _provision_bootstrap_admin(
    *,
    email: str,
    subject: str,
    name: str,
    picture: str | None,
) -> dict[str, Any]:
    now = _now_utc()
    admin_doc = {
        "email": normalize_email(email),
        "subject": subject,
        "name": name,
        "picture": picture,
        "role": ROLE_ADMIN,
        "health_id": None,
        "hospital_id": None,
        "is_active": True,
        "created_at": now,
        "updated_at": now,
        "last_login_at": now,
    }
    try:
        users = get_user_collection()
        users.update_one(
            {"email": admin_doc["email"]},
            {"$setOnInsert": admin_doc},
            upsert=True,
        )
        provisioned = users.find_one({"email": admin_doc["email"]}, {"_id": 0})
    except DatabaseConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while bootstrapping admin account.",
        ) from exc

    if provisioned is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to bootstrap admin account.",
        )
    return provisioned


@router.get("/auth/google/config", response_model=GoogleConfigResponse)
def google_client_config() -> GoogleConfigResponse:
    return GoogleConfigResponse(
        enabled=bool(GOOGLE_CLIENT_ID)
        and GOOGLE_AUTH_AVAILABLE
        and AUTH_SECRET_CONFIGURED,
        google_client_id=GOOGLE_CLIENT_ID,
    )


@router.post("/auth/google", response_model=GoogleLoginResponse)
def google_login(payload: GoogleLoginRequest) -> GoogleLoginResponse:
    if not GOOGLE_AUTH_AVAILABLE or google_requests is None or id_token is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google auth dependency missing. Install with: pip install google-auth",
        )

    if not GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="GOOGLE_CLIENT_ID is not configured on the server.",
        )
    if not AUTH_SECRET_CONFIGURED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                f"AUTH_SECRET_KEY is not configured. Set at least "
                f"{MIN_SECRET_KEY_LENGTH} characters."
            ),
        )

    try:
        claims = id_token.verify_oauth2_token(
            payload.credential,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google ID token.",
        ) from exc

    issuer = str(claims.get("iss", ""))
    if issuer not in TRUSTED_ISSUERS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Untrusted token issuer.",
        )

    email = normalize_email(str(claims.get("email", "")))
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Google account email is missing.",
        )

    if not bool(claims.get("email_verified", False)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Google account email must be verified.",
        )

    subject = str(claims.get("sub", "")).strip()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Google account subject claim is missing.",
        )

    display_name = str(claims.get("name", email)).strip() or email
    picture = str(claims.get("picture")) if claims.get("picture") else None

    managed_user = _load_managed_user(email)
    if managed_user is None:
        if email in BOOTSTRAP_ADMIN_EMAILS:
            managed_user = _provision_bootstrap_admin(
                email=email,
                subject=subject,
                name=display_name,
                picture=picture,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This account is not provisioned. Contact admin.",
            )

    if not bool(managed_user.get("is_active", True)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is disabled. Contact admin.",
        )

    session_user = _build_session_user(
        subject=subject,
        email=email,
        name=str(managed_user.get("name") or display_name),
        picture=picture,
        role=str(managed_user.get("role", "")).strip().lower(),
        health_id=(
            str(managed_user.get("health_id"))
            if managed_user.get("health_id")
            else None
        ),
        hospital_id=(
            str(managed_user.get("hospital_id"))
            if managed_user.get("hospital_id")
            else None
        ),
    )

    _sync_managed_user_login(
        email=session_user.email,
        subject=session_user.subject,
        name=session_user.name,
        picture=session_user.picture,
        role=session_user.role,
        health_id=session_user.health_id,
        hospital_id=session_user.hospital_id,
    )

    expires_at = _now_utc() + timedelta(seconds=SESSION_TTL_SECONDS)
    token = _create_access_token(user=session_user, expires_at=expires_at)
    return GoogleLoginResponse(
        access_token=token,
        expires_at=expires_at,
        user=session_user,
    )


@router.get("/auth/session", response_model=SessionResponse)
def get_active_session(
    authorization: str | None = Header(default=None),
) -> SessionResponse:
    token = _extract_bearer_token(authorization)
    session = _decode_access_token(token)

    managed_user = _load_managed_user(session.user.email)
    if managed_user is None or not bool(managed_user.get("is_active", True)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session account is no longer active.",
        )

    resolved_user = _build_session_user(
        subject=session.user.subject,
        email=session.user.email,
        name=str(managed_user.get("name") or session.user.name),
        picture=session.user.picture,
        role=str(managed_user.get("role", "")).strip().lower(),
        health_id=(
            str(managed_user.get("health_id"))
            if managed_user.get("health_id")
            else None
        ),
        hospital_id=(
            str(managed_user.get("hospital_id"))
            if managed_user.get("hospital_id")
            else None
        ),
    )

    return SessionResponse(
        authenticated=True,
        expires_at=session.expires_at,
        user=resolved_user,
    )


@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(authorization: str | None = Header(default=None)) -> None:
    token = _extract_bearer_token(authorization)
    _decode_access_token(token)


def get_current_user(
    authorization: str | None = Header(default=None),
) -> SessionUser:
    token = _extract_bearer_token(authorization)
    session = _decode_access_token(token)
    managed_user = _load_managed_user(session.user.email)

    if managed_user is None or not bool(managed_user.get("is_active", True)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session account is no longer active.",
        )

    return _build_session_user(
        subject=session.user.subject,
        email=session.user.email,
        name=str(managed_user.get("name") or session.user.name),
        picture=session.user.picture,
        role=str(managed_user.get("role", "")).strip().lower(),
        health_id=(
            str(managed_user.get("health_id")) if managed_user.get("health_id") else None
        ),
        hospital_id=(
            str(managed_user.get("hospital_id"))
            if managed_user.get("hospital_id")
            else None
        ),
    )


def require_roles(*allowed_roles: str) -> Callable[[SessionUser], SessionUser]:
    normalized_allowed = {role.strip().lower() for role in allowed_roles}
    invalid_roles = normalized_allowed - VALID_ROLES
    if invalid_roles:
        raise ValueError(f"Unsupported role(s): {', '.join(sorted(invalid_roles))}")

    def _role_dependency(
        current_user: SessionUser = Depends(get_current_user),
    ) -> SessionUser:
        if current_user.role not in normalized_allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )
        return current_user

    return _role_dependency
