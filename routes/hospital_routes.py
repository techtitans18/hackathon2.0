from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError, PyMongoError

from database.db import DatabaseConnectionError, get_hospital_collection
from models.hospital import HospitalRegistrationRequest, HospitalRegistrationResponse
from routes.auth_routes import ROLE_ADMIN, SessionUser, require_roles

router = APIRouter(tags=["Hospitals"])


@router.post(
    "/register_hospital",
    response_model=HospitalRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_hospital(
    payload: HospitalRegistrationRequest,
    _: SessionUser = Depends(require_roles(ROLE_ADMIN)),
) -> HospitalRegistrationResponse:
    hospital_id = str(uuid4())
    hospital_doc = {
        "hospital_id": hospital_id,
        "hospital_name": payload.hospital_name,
        "hospital_type": payload.hospital_type,
        "created_at": datetime.now(timezone.utc),
    }

    try:
        hospital_collection = get_hospital_collection()
        hospital_collection.insert_one(hospital_doc)
    except DuplicateKeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Hospital registration conflict. Please retry.",
        ) from exc
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while registering hospital.",
        ) from exc
    except DatabaseConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    return HospitalRegistrationResponse(HospitalID=hospital_id)
