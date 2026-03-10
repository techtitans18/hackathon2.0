from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import hashlib

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from pymongo.errors import DuplicateKeyError, PyMongoError

from database.db import (
    DatabaseConnectionError,
    get_hospital_collection,
    get_patient_collection,
    get_user_collection,
)
from routes.auth_routes import (
    ROLE_ADMIN,
    ROLE_HOSPITAL,
    ROLE_PATIENT,
    SessionUser,
    normalize_email,
    require_roles,
)

router = APIRouter(tags=["Administration"])
VALID_ROLES = {ROLE_ADMIN, ROLE_HOSPITAL, ROLE_PATIENT}


class AdminUserUpsertRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: str = Field(..., min_length=5, max_length=320)
    role: str = Field(..., min_length=4, max_length=20)
    name: str | None = Field(default=None, max_length=120)
    health_id: str | None = Field(default=None, max_length=80)
    hospital_id: str | None = Field(default=None, max_length=200)
    hospital_name: str | None = Field(default=None, max_length=180)
    hospital_type: str | None = Field(default=None, max_length=120)
    is_active: bool = True


class AdminUserSummary(BaseModel):
    email: str
    role: str
    name: str | None = None
    health_id: str | None = None
    hospital_id: str | None = None
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None
    last_login_at: datetime | None = None


class AdminUserUpsertResponse(BaseModel):
    message: str
    created: bool
    user: AdminUserSummary


class AdminUsersListResponse(BaseModel):
    users: list[AdminUserSummary]


def _normalize_role(role: str) -> str:
    normalized = role.strip().lower()
    if normalized not in VALID_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="role must be one of: admin, hospital, patient.",
        )
    return normalized


def _validate_email(email: str) -> str:
    normalized = normalize_email(email)
    if "@" not in normalized or normalized.startswith("@") or normalized.endswith("@"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email must be a valid address.",
        )
    return normalized


def _clean_optional(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned if cleaned else None


def _assert_role_links(role: str, health_id: str | None, hospital_id: str | None, hospital_name: str | None, hospital_type: str | None) -> str | None:
    """Validate and create hospital if needed. Returns hospital_id."""
    try:
        if role == ROLE_PATIENT:
            if not health_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Patient role requires health_id.",
                )
            patient_exists = (
                get_patient_collection().count_documents({"health_id": health_id}, limit=1)
                > 0
            )
            if not patient_exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="health_id does not exist in patients.",
                )
            return None

        if role == ROLE_HOSPITAL:
            # If hospital_id looks like "name|type", create hospital
            if hospital_id and "|" in hospital_id:
                parts = hospital_id.split("|")
                if len(parts) == 2:
                    hospital_name = parts[0].strip()
                    hospital_type = parts[1].strip()
            
            if not hospital_name or not hospital_type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Hospital role requires hospital_name and hospital_type.",
                )
            
            # Generate deterministic hospital_id
            hospital_id_input = f"{hospital_name}|{hospital_type}"
            generated_hospital_id = hashlib.sha256(hospital_id_input.encode('utf-8')).hexdigest()[:16].upper()
            
            # Create hospital if doesn't exist
            hospital_collection = get_hospital_collection()
            existing_hospital = hospital_collection.find_one({"hospital_id": generated_hospital_id})
            
            if not existing_hospital:
                hospital_doc = {
                    "hospital_id": generated_hospital_id,
                    "hospital_name": hospital_name,
                    "hospital_type": hospital_type,
                    "created_at": datetime.now(timezone.utc),
                }
                hospital_collection.insert_one(hospital_doc)
            
            return generated_hospital_id
            
        return None
    except HTTPException:
        raise
    except DuplicateKeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "User link conflict. health_id/hospital_id or email is already assigned."
            ),
        ) from exc
    except DatabaseConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while validating user links.",
        ) from exc


def _to_summary(user_doc: dict[str, Any]) -> AdminUserSummary:
    return AdminUserSummary(
        email=str(user_doc.get("email", "")),
        role=str(user_doc.get("role", "")),
        name=user_doc.get("name"),
        health_id=user_doc.get("health_id"),
        hospital_id=user_doc.get("hospital_id"),
        is_active=bool(user_doc.get("is_active", True)),
        created_at=user_doc.get("created_at"),
        updated_at=user_doc.get("updated_at"),
        last_login_at=user_doc.get("last_login_at"),
    )


@router.get("/admin/users", response_model=AdminUsersListResponse)
def list_users(
    _: SessionUser = Depends(require_roles(ROLE_ADMIN)),
) -> AdminUsersListResponse:
    try:
        user_docs = list(
            get_user_collection()
            .find({}, {"_id": 0})
            .sort([("role", 1), ("email", 1)])
        )
    except DatabaseConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while listing users.",
        ) from exc

    return AdminUsersListResponse(users=[_to_summary(doc) for doc in user_docs])


@router.post(
    "/admin/users",
    response_model=AdminUserUpsertResponse,
    status_code=status.HTTP_200_OK,
)
def upsert_user(
    payload: AdminUserUpsertRequest,
    _: SessionUser = Depends(require_roles(ROLE_ADMIN)),
) -> AdminUserUpsertResponse:
    email = _validate_email(payload.email)
    role = _normalize_role(payload.role)
    health_id = _clean_optional(payload.health_id)
    hospital_id = _clean_optional(payload.hospital_id)
    hospital_name = _clean_optional(payload.hospital_name)
    hospital_type = _clean_optional(payload.hospital_type)

    if role == ROLE_ADMIN:
        health_id = None
        hospital_id = None
    elif role == ROLE_PATIENT:
        hospital_id = None
    elif role == ROLE_HOSPITAL:
        health_id = None

    # Validate and create hospital if needed
    generated_hospital_id = _assert_role_links(role, health_id, hospital_id, hospital_name, hospital_type)
    if generated_hospital_id:
        hospital_id = generated_hospital_id

    now = datetime.now(timezone.utc)
    update_fields: dict[str, Any] = {
        "role": role,
        "name": _clean_optional(payload.name),
        "health_id": health_id,
        "hospital_id": hospital_id,
        "is_active": payload.is_active,
        "updated_at": now,
    }

    try:
        users = get_user_collection()
        existing = users.find_one({"email": email}, {"_id": 0})

        if existing is None:
            user_doc = {
                "email": email,
                "subject": None,
                "picture": None,
                "last_login_at": None,
                "created_at": now,
                **update_fields,
            }
            users.insert_one(user_doc)
            created = True
            stored_doc = user_doc
        else:
            users.update_one({"email": email}, {"$set": update_fields})
            stored_doc = users.find_one({"email": email}, {"_id": 0})
            if stored_doc is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="User update failed unexpectedly.",
                )
            created = False
    except HTTPException:
        raise
    except DatabaseConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while saving user.",
        ) from exc

    return AdminUserUpsertResponse(
        message="User access updated successfully.",
        created=created,
        user=_to_summary(stored_doc),
    )
