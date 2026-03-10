from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.responses import JSONResponse

from routes.auth_routes import SessionUser, get_current_user

from .emergency_models import (
    EmergencyDataUpsertRequest,
    EmergencyDataUpsertResponse,
    EmergencyProfileRequest,
    EmergencyProfileResponse,
    EmergencySearchRequest,
    EmergencySearchResponse,
)
from .emergency_security import (
    UNAUTHORIZED_EMERGENCY_ACCESS_MESSAGE,
    UnauthorizedEmergencyAccessError,
    enforce_emergency_access,
)
from .emergency_service import (
    find_patient_emergency,
    get_emergency_profile,
    upsert_emergency_data,
)

router = APIRouter(tags=["Emergency Access"])


def _resolve_emergency_user(
    authorization: str | None = Header(default=None),
) -> SessionUser | None:
    try:
        return get_current_user(authorization)
    except HTTPException:
        return None


@router.post("/emergency/search", response_model=EmergencySearchResponse)
def emergency_search(
    payload: EmergencySearchRequest,
    current_user: SessionUser | None = Depends(_resolve_emergency_user),
) -> EmergencySearchResponse | JSONResponse:
    try:
        enforce_emergency_access(role=payload.role, current_user=current_user)
    except UnauthorizedEmergencyAccessError:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"error": UNAUTHORIZED_EMERGENCY_ACCESS_MESSAGE},
        )

    result = find_patient_emergency(
        search_type=payload.search_type,
        value=payload.value,
        name=payload.name,
        dob=payload.dob,
    )
    return EmergencySearchResponse(**result)


@router.post("/emergency/profile", response_model=EmergencyProfileResponse)
def emergency_profile(
    payload: EmergencyProfileRequest,
    current_user: SessionUser | None = Depends(_resolve_emergency_user),
) -> EmergencyProfileResponse | JSONResponse:
    try:
        enforce_emergency_access(role=payload.role, current_user=current_user)
    except UnauthorizedEmergencyAccessError:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"error": UNAUTHORIZED_EMERGENCY_ACCESS_MESSAGE},
        )

    result = get_emergency_profile(
        health_id=payload.health_id,
        hospital_id=current_user.hospital_id if current_user else "",
    )
    return EmergencyProfileResponse(**result)


@router.post("/emergency/upsert", response_model=EmergencyDataUpsertResponse)
def emergency_upsert(
    payload: EmergencyDataUpsertRequest,
    current_user: SessionUser | None = Depends(_resolve_emergency_user),
) -> EmergencyDataUpsertResponse | JSONResponse:
    try:
        enforce_emergency_access(role=payload.role, current_user=current_user)
    except UnauthorizedEmergencyAccessError:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"error": UNAUTHORIZED_EMERGENCY_ACCESS_MESSAGE},
        )

    result = upsert_emergency_data(
        health_id=payload.health_id,
        blood_group=payload.blood_group,
        allergies=payload.allergies,
        diseases=payload.diseases,
        surgeries=payload.surgeries,
        emergency_contact=payload.emergency_contact,
    )
    return EmergencyDataUpsertResponse(**result)
