from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, status
from pymongo.errors import PyMongoError

from database.db import (
    DatabaseConnectionError,
    get_emergency_data_collection,
    get_emergency_log_collection,
    get_patient_collection,
)

ALLOWED_SEARCH_TYPES = {"health_id", "phone", "name_dob"}
BLOOD_GROUPS = {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}


def _normalize_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    normalized: list[str] = []
    for item in value:
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


def generate_emergency_hash(
    *,
    health_id: str,
    blood_group: str,
    allergies: list[str],
    diseases: list[str],
    surgeries: list[str],
) -> str:
    payload = {
        "health_id": health_id.strip(),
        "blood_group": blood_group.strip(),
        "allergies": allergies,
        "diseases": diseases,
        "surgeries": surgeries,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def find_patient_emergency(
    *,
    search_type: str,
    value: str | None = None,
    name: str | None = None,
    dob: str | None = None,
) -> dict[str, str]:
    normalized_type = search_type.strip().lower()
    if normalized_type not in ALLOWED_SEARCH_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="search_type must be one of: health_id, phone, name_dob.",
        )

    query: dict[str, Any]
    if normalized_type == "health_id":
        health_id = (value or "").strip()
        if not health_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="value is required when search_type is health_id.",
            )
        query = {"health_id": health_id}
    elif normalized_type == "phone":
        phone = (value or "").strip()
        if not phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="value is required when search_type is phone.",
            )
        query = {"phone": phone}
    else:
        patient_name = (name or "").strip()
        patient_dob = (dob or "").strip()
        if not patient_name or not patient_dob:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="name and dob are required when search_type is name_dob.",
            )
        query = {
            "name": {"$regex": f"^{re.escape(patient_name)}$", "$options": "i"},
            "dob": patient_dob,
        }

    try:
        patient_doc = get_patient_collection().find_one(
            query,
            {"_id": 0, "health_id": 1, "name": 1},
        )
    except DatabaseConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while searching emergency patient.",
        ) from exc

    if not isinstance(patient_doc, dict):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found.",
        )

    return {
        "health_id": str(patient_doc.get("health_id", "")).strip(),
        "name": str(patient_doc.get("name", "")).strip(),
    }


def log_emergency_access(*, hospital_id: str, health_id: str) -> None:
    normalized_hospital_id = hospital_id.strip()
    normalized_health_id = health_id.strip()
    if not normalized_hospital_id or not normalized_health_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="hospital_id and health_id are required for emergency logging.",
        )

    log_doc = {
        "hospital_id": normalized_hospital_id,
        "health_id": normalized_health_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": "Emergency Access",
    }

    try:
        get_emergency_log_collection().insert_one(log_doc)
    except DatabaseConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while logging emergency access.",
        ) from exc


def get_emergency_profile(*, health_id: str, hospital_id: str) -> dict[str, Any]:
    normalized_health_id = health_id.strip()
    if not normalized_health_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="health_id is required.",
        )

    # Log every emergency profile access attempt for auditing.
    log_emergency_access(
        hospital_id=hospital_id,
        health_id=normalized_health_id,
    )

    try:
        patient_doc = get_patient_collection().find_one(
            {"health_id": normalized_health_id},
            {"_id": 0, "name": 1},
        )
        emergency_doc = get_emergency_data_collection().find_one(
            {"health_id": normalized_health_id},
            {
                "_id": 0,
                "health_id": 1,
                "blood_group": 1,
                "allergies": 1,
                "diseases": 1,
                "surgeries": 1,
                "emergency_contact": 1,
                "blockchain_hash": 1,
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
            detail="Database error while loading emergency profile.",
        ) from exc

    if not isinstance(patient_doc, dict):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found.",
        )
    if not isinstance(emergency_doc, dict):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency data not found.",
        )

    blood_group = str(emergency_doc.get("blood_group", "")).strip()
    allergies = _normalize_list(emergency_doc.get("allergies"))
    diseases = _normalize_list(emergency_doc.get("diseases"))
    surgeries = _normalize_list(emergency_doc.get("surgeries"))
    emergency_contact = str(emergency_doc.get("emergency_contact", "")).strip()

    computed_hash = generate_emergency_hash(
        health_id=normalized_health_id,
        blood_group=blood_group,
        allergies=allergies,
        diseases=diseases,
        surgeries=surgeries,
    )
    stored_hash = str(emergency_doc.get("blockchain_hash", "")).strip().lower()
    blockchain_status = (
        "Verified"
        if stored_hash and computed_hash == stored_hash
        else "Tampered Data"
    )

    return {
        "health_id": normalized_health_id,
        "name": str(patient_doc.get("name", "")).strip(),
        "blood_group": blood_group,
        "allergies": allergies,
        "diseases": diseases,
        "surgeries": surgeries,
        "emergency_contact": emergency_contact,
        "blockchain_status": blockchain_status,
    }


def upsert_emergency_data(
    *,
    health_id: str,
    blood_group: str,
    allergies: list[str],
    diseases: list[str],
    surgeries: list[str],
    emergency_contact: str,
) -> dict[str, str]:
    normalized_health_id = health_id.strip()
    normalized_contact = emergency_contact.strip()
    normalized_blood_group = _normalize_blood_group(blood_group)
    normalized_allergies = _normalize_list(allergies)
    normalized_diseases = _normalize_list(diseases)
    normalized_surgeries = _normalize_list(surgeries)

    if not normalized_health_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="health_id is required.",
        )
    if not normalized_contact:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="emergency_contact is required.",
        )

    blockchain_hash = generate_emergency_hash(
        health_id=normalized_health_id,
        blood_group=normalized_blood_group,
        allergies=normalized_allergies,
        diseases=normalized_diseases,
        surgeries=normalized_surgeries,
    )
    now = datetime.now(timezone.utc).isoformat()

    try:
        patient_exists = (
            get_patient_collection().count_documents(
                {"health_id": normalized_health_id},
                limit=1,
            )
            > 0
        )
        if not patient_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found.",
            )

        get_emergency_data_collection().update_one(
            {"health_id": normalized_health_id},
            {
                "$set": {
                    "health_id": normalized_health_id,
                    "blood_group": normalized_blood_group,
                    "allergies": normalized_allergies,
                    "diseases": normalized_diseases,
                    "surgeries": normalized_surgeries,
                    "emergency_contact": normalized_contact,
                    "blockchain_hash": blockchain_hash,
                    "updated_at": now,
                },
                "$setOnInsert": {"created_at": now},
            },
            upsert=True,
        )
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
            detail="Database error while saving emergency data.",
        ) from exc

    return {
        "health_id": normalized_health_id,
        "blood_group": normalized_blood_group,
        "blockchain_hash": blockchain_hash,
        "message": "Emergency data saved successfully.",
    }
