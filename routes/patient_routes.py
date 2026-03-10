from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError, PyMongoError

from app.emergency.emergency_service import generate_emergency_hash
from database.db import (
    DatabaseConnectionError,
    get_emergency_data_collection,
    get_patient_collection,
    get_record_collection,
    get_user_collection,
)
from models.patient import (
    EHealthCardResponse,
    PatientRegistrationRequest,
    PatientRegistrationResponse,
)
from routes.auth_routes import (
    ROLE_ADMIN,
    ROLE_HOSPITAL,
    ROLE_PATIENT,
    SessionUser,
    normalize_email,
    require_roles,
)

router = APIRouter(tags=["Patients"])
BLOOD_GROUPS = {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}


def _is_valid_email(email: str) -> bool:
    return "@" in email and not email.startswith("@") and not email.endswith("@")


def _normalize_optional_text(value: str | None) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    return cleaned if cleaned else None


def _normalize_text_list(values: list[str]) -> list[str]:
    normalized: list[str] = []
    for item in values:
        cleaned = str(item).strip()
        if cleaned:
            normalized.append(cleaned)
    return normalized


def _normalize_blood_group(value: str) -> str:
    normalized = value.strip().upper()
    if normalized not in BLOOD_GROUPS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="blood_group must be one of: A+, A-, B+, B-, AB+, AB-, O+, O-.",
        )
    return normalized


def _build_emergency_doc(
    *,
    health_id: str,
    blood_group: str,
    allergies: list[str],
    diseases: list[str],
    surgeries: list[str],
    emergency_contact: str,
) -> dict[str, Any]:
    blockchain_hash = generate_emergency_hash(
        health_id=health_id,
        blood_group=blood_group,
        allergies=allergies,
        diseases=diseases,
        surgeries=surgeries,
    )
    return {
        "health_id": health_id,
        "blood_group": blood_group,
        "allergies": allergies,
        "diseases": diseases,
        "surgeries": surgeries,
        "emergency_contact": emergency_contact,
        "blockchain_hash": blockchain_hash,
    }


def _fetch_patient_records(health_id: str) -> dict[str, Any]:
    try:
        patient = get_patient_collection().find_one({"health_id": health_id}, {"_id": 0})
        if patient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found.",
            )

        records = list(
            get_record_collection().find({"health_id": health_id}, {"_id": 0}).sort(
                "timestamp", -1
            )
        )
    except HTTPException:
        raise
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while fetching patient records.",
        ) from exc
    except DatabaseConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    patient_response = {
        "HealthID": patient["health_id"],
        "name": patient["name"],
        "age": patient["age"],
        "phone": patient["phone"],
        "dob": patient.get("dob"),
        "blood_group": patient.get("blood_group"),
        "photo_url": patient.get("photo_url"),
        "email": patient.get("email"),
        "created_at": patient.get("created_at"),
    }

    formatted_records = []
    for record in records:
        stored_file_name = record.get("stored_file_name")
        summary_stored_file_name = record.get("summary_stored_file_name")
        download_url = (
            f"/record/file/{stored_file_name}" if isinstance(stored_file_name, str) else None
        )
        summary_download_url = (
            f"/record/summary/{summary_stored_file_name}"
            if isinstance(summary_stored_file_name, str)
            else None
        )
        formatted_records.append(
            {
                "HealthID": record["health_id"],
                "HospitalID": record["hospital_id"],
                "record_type": record["record_type"],
                "description": record["description"],
                "file_name": record["file_name"],
                "file_reference": stored_file_name,
                "download_url": download_url,
                "summary_file_name": record.get("summary_file_name"),
                "summary_file_reference": summary_stored_file_name,
                "summary_download_url": summary_download_url,
                "record_hash": record["record_hash"],
                "timestamp": record["timestamp"],
            }
        )

    return {"patient": patient_response, "records": formatted_records}


def _fetch_ehealth_card(health_id: str) -> EHealthCardResponse:
    try:
        patient = get_patient_collection().find_one(
            {"health_id": health_id},
            {"_id": 0, "health_id": 1, "name": 1, "phone": 1, "blood_group": 1, "photo_url": 1},
        )
        emergency_data = get_emergency_data_collection().find_one(
            {"health_id": health_id},
            {"_id": 0, "blood_group": 1},
        )
    except DatabaseConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while loading e-healthcard.",
        ) from exc

    if not isinstance(patient, dict):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found.",
        )

    blood_group = str(patient.get("blood_group") or "").strip().upper()
    if not blood_group and isinstance(emergency_data, dict):
        blood_group = str(emergency_data.get("blood_group") or "").strip().upper()

    return EHealthCardResponse(
        health_id=str(patient.get("health_id", "")).strip(),
        name=str(patient.get("name", "")).strip(),
        blood_group=blood_group or "UNKNOWN",
        phone=str(patient.get("phone", "")).strip(),
        photo_url=_normalize_optional_text(patient.get("photo_url")),
    )


@router.post(
    "/register_patient",
    response_model=PatientRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_patient(
    payload: PatientRegistrationRequest,
    current_user: SessionUser = Depends(require_roles(ROLE_HOSPITAL)),
) -> PatientRegistrationResponse:
    if not current_user.hospital_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hospital account is missing assigned HospitalID.",
        )

    email = normalize_email(payload.email)
    if not _is_valid_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient email is invalid.",
        )
    blood_group = _normalize_blood_group(payload.blood_group)
    photo_url = _normalize_optional_text(payload.photo_url)
    allergies = _normalize_text_list(payload.allergies)
    diseases = _normalize_text_list(payload.diseases)
    surgeries = _normalize_text_list(payload.surgeries)
    emergency_contact = _normalize_optional_text(payload.emergency_contact) or payload.phone

    now = datetime.now(timezone.utc)
    health_id = str(uuid4())
    patient_doc = {
        "health_id": health_id,
        "name": payload.name,
        "age": payload.age,
        "phone": payload.phone,
        "dob": payload.dob,
        "blood_group": blood_group,
        "photo_url": photo_url,
        "email": email,
        "created_at": now,
        "created_by_hospital_id": current_user.hospital_id,
    }

    patient_collection = None
    patient_inserted = False
    emergency_data_upserted = False

    try:
        patient_collection = get_patient_collection()
        emergency_data_collection = get_emergency_data_collection()
        user_collection = get_user_collection()

        existing_patient = patient_collection.find_one(
            {"email": email},
            {"_id": 0, "health_id": 1, "created_by_hospital_id": 1},
        )
        if isinstance(existing_patient, dict):
            existing_health_id = str(existing_patient.get("health_id", "")).strip()
            existing_hospital_id = str(
                existing_patient.get("created_by_hospital_id", "")
            ).strip()
            if existing_hospital_id != current_user.hospital_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Patient email is already registered under another hospital.",
                )
            if not existing_health_id:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Existing patient record is missing HealthID.",
                )

            # Idempotent re-submission for the same hospital:
            # keep patient details in sync and return the same HealthID.
            patient_collection.update_one(
                {"health_id": existing_health_id},
                {
                    "$set": {
                        "name": payload.name,
                        "age": payload.age,
                        "phone": payload.phone,
                        "dob": payload.dob,
                        "blood_group": blood_group,
                        "photo_url": photo_url,
                        "updated_at": now,
                    }
                },
            )
            emergency_data_collection.update_one(
                {"health_id": existing_health_id},
                {
                    "$set": {
                        **_build_emergency_doc(
                            health_id=existing_health_id,
                            blood_group=blood_group,
                            allergies=allergies,
                            diseases=diseases,
                            surgeries=surgeries,
                            emergency_contact=emergency_contact,
                        ),
                        "updated_at": now,
                    },
                    "$setOnInsert": {"created_at": now},
                },
                upsert=True,
            )

            existing_user = user_collection.find_one(
                {"email": email},
                {"_id": 0, "role": 1},
            )
            if existing_user is None:
                user_collection.insert_one(
                    {
                        "email": email,
                        "subject": None,
                        "name": payload.name,
                        "picture": None,
                        "role": ROLE_PATIENT,
                        "health_id": existing_health_id,
                        "hospital_id": None,
                        "is_active": True,
                        "created_at": now,
                        "updated_at": now,
                        "last_login_at": None,
                    }
                )
            else:
                existing_role = str(existing_user.get("role", "")).strip().lower()
                if existing_role and existing_role != ROLE_PATIENT:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Email is already assigned to a non-patient account.",
                    )
                user_collection.update_one(
                    {"email": email},
                    {
                        "$set": {
                            "name": payload.name,
                            "role": ROLE_PATIENT,
                            "health_id": existing_health_id,
                            "hospital_id": None,
                            "is_active": True,
                            "updated_at": now,
                        }
                    },
                )

            return PatientRegistrationResponse(HealthID=existing_health_id)

        existing_user = user_collection.find_one(
            {"email": email},
            {"_id": 0, "role": 1, "health_id": 1},
        )
        if isinstance(existing_user, dict):
            existing_role = str(existing_user.get("role", "")).strip().lower()
            if existing_role and existing_role != ROLE_PATIENT:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email is already assigned to a non-patient account.",
                )

            if existing_user.get("health_id"):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email is already linked to another patient account.",
                )

        patient_collection.insert_one(patient_doc)
        patient_inserted = True
        emergency_data_collection.update_one(
            {"health_id": health_id},
            {
                "$set": {
                    **_build_emergency_doc(
                        health_id=health_id,
                        blood_group=blood_group,
                        allergies=allergies,
                        diseases=diseases,
                        surgeries=surgeries,
                        emergency_contact=emergency_contact,
                    ),
                    "updated_at": now,
                },
                "$setOnInsert": {"created_at": now},
            },
            upsert=True,
        )
        emergency_data_upserted = True

        if existing_user is None:
            user_collection.insert_one(
                {
                    "email": email,
                    "subject": None,
                    "name": payload.name,
                    "picture": None,
                    "role": ROLE_PATIENT,
                    "health_id": health_id,
                    "hospital_id": None,
                    "is_active": True,
                    "created_at": now,
                    "updated_at": now,
                    "last_login_at": None,
                }
            )
        else:
            user_collection.update_one(
                {"email": email},
                {
                    "$set": {
                        "name": payload.name,
                        "role": ROLE_PATIENT,
                        "health_id": health_id,
                        "hospital_id": None,
                        "is_active": True,
                        "updated_at": now,
                    }
                },
            )
    except DuplicateKeyError as exc:
        if patient_inserted and patient_collection is not None:
            patient_collection.delete_one({"health_id": health_id})
        if emergency_data_upserted:
            get_emergency_data_collection().delete_one({"health_id": health_id})
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Patient registration conflict. Please retry.",
        ) from exc
    except PyMongoError as exc:
        if patient_inserted and patient_collection is not None:
            patient_collection.delete_one({"health_id": health_id})
        if emergency_data_upserted:
            get_emergency_data_collection().delete_one({"health_id": health_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while registering patient.",
        ) from exc
    except DatabaseConnectionError as exc:
        if patient_inserted and patient_collection is not None:
            patient_collection.delete_one({"health_id": health_id})
        if emergency_data_upserted:
            get_emergency_data_collection().delete_one({"health_id": health_id})
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    return PatientRegistrationResponse(HealthID=health_id)


@router.get("/patient/me")
def get_my_patient_records(
    current_user: SessionUser = Depends(require_roles(ROLE_PATIENT)),
) -> dict[str, Any]:
    if not current_user.health_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient account is missing assigned HealthID.",
        )

    return _fetch_patient_records(current_user.health_id)


@router.get("/patient/me/e-healthcard", response_model=EHealthCardResponse)
def get_my_ehealth_card(
    current_user: SessionUser = Depends(require_roles(ROLE_PATIENT)),
) -> EHealthCardResponse:
    if not current_user.health_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient account is missing assigned HealthID.",
        )

    return _fetch_ehealth_card(current_user.health_id)


@router.get("/patient/{HealthID}")
def get_patient_records(
    HealthID: str,
    current_user: SessionUser = Depends(require_roles(ROLE_ADMIN, ROLE_PATIENT)),
) -> dict[str, Any]:
    if current_user.role == ROLE_PATIENT and current_user.health_id != HealthID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patients can only access their own records.",
        )

    return _fetch_patient_records(HealthID)
