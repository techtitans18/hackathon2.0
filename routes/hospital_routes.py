from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4
import hashlib

from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError, PyMongoError

from database.db import DatabaseConnectionError, get_hospital_collection
from models.hospital import (
    HospitalListResponse,
    HospitalRegistrationRequest,
    HospitalRegistrationResponse,
    HospitalUpdateRequest,
    HospitalUpdateResponse,
    Hospital,
)
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
    # Generate deterministic HospitalID using SHA256
    # Use hospital name + type for deterministic ID
    hospital_id_input = f"{payload.hospital_name}|{payload.hospital_type}"
    hospital_id = hashlib.sha256(hospital_id_input.encode('utf-8')).hexdigest()[:16].upper()
    
    hospital_doc = {
        "hospital_id": hospital_id,
        "hospital_name": payload.hospital_name,
        "hospital_type": payload.hospital_type,
        "created_at": datetime.now(timezone.utc),
    }

    try:
        hospital_collection = get_hospital_collection()
        # Check if hospital already exists
        existing = hospital_collection.find_one({"hospital_id": hospital_id})
        if existing:
            # Return existing hospital ID (idempotent)
            return HospitalRegistrationResponse(HospitalID=hospital_id)
        
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


@router.get("/hospitals", response_model=HospitalListResponse)
def list_hospitals(
    _: SessionUser = Depends(require_roles(ROLE_ADMIN)),
) -> HospitalListResponse:
    """List all registered hospitals. Admin only."""
    try:
        hospital_collection = get_hospital_collection()
        hospitals_docs = hospital_collection.find({}, {"_id": 0}).sort(
            "created_at", -1
        )
        hospitals = [
            Hospital(
                hospital_id=doc["hospital_id"],
                hospital_name=doc["hospital_name"],
                hospital_type=doc["hospital_type"],
                created_at=doc["created_at"],
            )
            for doc in hospitals_docs
        ]
        return HospitalListResponse(hospitals=hospitals)
    except DatabaseConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while listing hospitals.",
        ) from exc


@router.put("/hospitals/{hospital_id}", response_model=HospitalUpdateResponse)
def update_hospital(
    hospital_id: str,
    payload: HospitalUpdateRequest,
    _: SessionUser = Depends(require_roles(ROLE_ADMIN)),
) -> HospitalUpdateResponse:
    """Update hospital details. Admin only."""
    try:
        hospital_collection = get_hospital_collection()
        result = hospital_collection.update_one(
            {"hospital_id": hospital_id},
            {
                "$set": {
                    "hospital_name": payload.hospital_name,
                    "hospital_type": payload.hospital_type,
                }
            },
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Hospital with ID {hospital_id} not found.",
            )

        return HospitalUpdateResponse(
            message="Hospital updated successfully",
            hospital_id=hospital_id,
        )
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while updating hospital.",
        ) from exc
    except DatabaseConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
