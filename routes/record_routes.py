from __future__ import annotations

import hashlib
import string
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from pymongo.errors import PyMongoError

from blockchain.verify import verify_blockchain_integrity

from app.ai_summary.summarizer import (
    SummarizerUnavailableError,
    generate_medical_summary,
    is_summarizer_ready,
    load_summarizer_model,
)
from blockchain.blockchain import healthcare_chain
from database.db import (
    DatabaseConnectionError,
    get_hospital_collection,
    get_patient_collection,
    get_record_collection,
)
from models.record import AddRecordResponse
from routes.auth_routes import (
    ROLE_ADMIN,
    ROLE_HOSPITAL,
    ROLE_PATIENT,
    SessionUser,
    require_roles,
)

router = APIRouter(tags=["Records"])
BASE_DIR = Path(__file__).resolve().parent.parent
RECORDS_DIR = BASE_DIR / "records"


def _is_valid_sha256_hash(hash_value: str) -> bool:
    return len(hash_value) == 64 and all(ch in string.hexdigits for ch in hash_value)


def _delete_local_file(path: Path | None) -> None:
    if path is not None and path.exists():
        path.unlink(missing_ok=True)


def _extract_report_text(file_content: bytes) -> str:
    """
    Read report bytes in memory for AI summarization only.

    This does not call external APIs and does not persist extracted text.
    """
    if b"\x00" in file_content[:4096]:
        return ""

    decoded_text = ""
    for encoding in ("utf-8", "utf-16", "latin-1"):
        try:
            decoded_text = file_content.decode(encoding)
            break
        except UnicodeDecodeError:
            continue

    if not decoded_text:
        decoded_text = file_content.decode("utf-8", errors="ignore")

    normalized = " ".join(decoded_text.split())
    return normalized[:12000]


def _build_ai_summary_source_text(
    record_type: str,
    description: str,
    file_content: bytes,
) -> str:
    extracted_report_text = _extract_report_text(file_content)
    parts = [
        f"Record type: {record_type.strip()}",
        f"Clinical description: {description.strip()}",
    ]
    if extracted_report_text:
        parts.append(f"Report content: {extracted_report_text}")
    return "\n".join(parts)


@router.post(
    "/add_record",
    response_model=AddRecordResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_record(
    HealthID: str = Form(...),
    HospitalID: str = Form(...),
    record_type: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    current_user: SessionUser = Depends(require_roles(ROLE_HOSPITAL)),
) -> AddRecordResponse:
    if not current_user.hospital_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hospital account is missing assigned HospitalID.",
        )

    if HospitalID.strip() != current_user.hospital_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hospital can only add records under its own HospitalID.",
        )

    if not file.filename or not file.filename.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must include a file name.",
        )
    if not record_type.strip() or not description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="record_type and description must be non-empty.",
        )
    if not HealthID.strip() or not HospitalID.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="HealthID and HospitalID must be non-empty.",
        )

    stored_path: Path | None = None
    summary_stored_path: Path | None = None

    try:
        patient = get_patient_collection().find_one(
            {"health_id": HealthID},
            {"_id": 0, "created_by_hospital_id": 1},
        )
        if patient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid HealthID. Patient does not exist.",
            )
        if patient.get("created_by_hospital_id") != current_user.hospital_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Hospital can only add records for patients registered by the same hospital."
                ),
            )

        hospital_exists = (
            get_hospital_collection().count_documents(
                {"hospital_id": current_user.hospital_id},
                limit=1,
            )
            > 0
        )
        if not hospital_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid HospitalID. Hospital does not exist.",
            )

        file_content = await file.read()
        if not file_content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty.",
            )

        RECORDS_DIR.mkdir(parents=True, exist_ok=True)
        safe_filename = Path(file.filename).name
        stored_filename = f"{uuid4()}_{safe_filename}"
        stored_path = RECORDS_DIR / stored_filename
        stored_path.write_bytes(file_content)

        if not is_summarizer_ready():
            try:
                load_summarizer_model()
            except SummarizerUnavailableError as exc:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=(
                        "AI summary is unavailable. Ensure local summarizer model is ready."
                    ),
                ) from exc

        ai_input_text = _build_ai_summary_source_text(
            record_type=record_type,
            description=description,
            file_content=file_content,
        )
        try:
            summary_text = generate_medical_summary(ai_input_text)
        except (ValueError, SummarizerUnavailableError) as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to summarize the uploaded report.",
            ) from exc

        summary_file_name = f"{Path(safe_filename).stem}_ai_summary.txt"
        summary_stored_filename = f"{uuid4()}_{summary_file_name}"
        summary_stored_path = RECORDS_DIR / summary_stored_filename
        summary_stored_path.write_text(f"{summary_text}\n", encoding="utf-8")

        record_hash = hashlib.sha256(file_content).hexdigest()
        timestamp = datetime.now(timezone.utc)

        record_doc = {
            "health_id": HealthID,
            "hospital_id": current_user.hospital_id,
            "record_type": record_type,
            "description": description,
            "file_name": safe_filename,
            "stored_file_name": stored_filename,
            "file_path": f"records/{stored_filename}",
            "summary_file_name": summary_file_name,
            "summary_stored_file_name": summary_stored_filename,
            "summary_file_path": f"records/{summary_stored_filename}",
            "record_hash": record_hash,
            "timestamp": timestamp,
        }
        insert_result = get_record_collection().insert_one(record_doc)

        block = healthcare_chain.create_block(
            health_id=HealthID,
            hospital_id=current_user.hospital_id,
            record_type=record_type,
            record_hash=record_hash,
        )
    except HTTPException:
        raise
    except PyMongoError as exc:
        _delete_local_file(stored_path)
        _delete_local_file(summary_stored_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while adding medical record.",
        ) from exc
    except DatabaseConnectionError as exc:
        _delete_local_file(stored_path)
        _delete_local_file(summary_stored_path)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except OSError as exc:
        _delete_local_file(stored_path)
        _delete_local_file(summary_stored_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="File storage error while saving medical record.",
        ) from exc
    finally:
        await file.close()

    return AddRecordResponse(
        message="Medical record added successfully.",
        record_id=str(insert_result.inserted_id),
        record_hash=record_hash,
        block=block,
        summary_file_name=summary_file_name,
        summary_download_url=f"/record/summary/{summary_stored_filename}",
    )


@router.get("/blockchain")
def get_blockchain(
    _: SessionUser = Depends(require_roles(ROLE_ADMIN)),
) -> dict[str, object]:
    chain = healthcare_chain.get_chain()
    integrity = verify_blockchain_integrity()
    return {
        "length": len(chain),
        "chain": chain,
        "integrity": integrity,
    }


@router.get("/record/hash/{record_hash}")
def get_record_by_hash(
    record_hash: str,
    _: SessionUser = Depends(require_roles(ROLE_ADMIN)),
) -> dict[str, object]:
    normalized_hash = record_hash.strip().lower()
    if not _is_valid_sha256_hash(normalized_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="record_hash must be a valid 64-character SHA256 hex string.",
        )

    try:
        records = list(
            get_record_collection()
            .find({"record_hash": normalized_hash}, {"_id": 0})
            .sort("timestamp", -1)
        )
    except DatabaseConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while fetching record by hash.",
        ) from exc

    blocks = [
        block
        for block in healthcare_chain.get_chain()
        if str(block.get("RecordHash", "")).lower() == normalized_hash
    ]

    if not records and not blocks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No record found for the provided hash.",
        )

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

    return {
        "record_hash": normalized_hash,
        "record_count": len(formatted_records),
        "block_count": len(blocks),
        "records": formatted_records,
        "blockchain_blocks": blocks,
    }


@router.get("/record/file/{stored_file_name}")
def download_record_file(
    stored_file_name: str,
    current_user: SessionUser = Depends(require_roles(ROLE_ADMIN, ROLE_PATIENT)),
) -> FileResponse:
    safe_stored_name = Path(stored_file_name).name
    if safe_stored_name != stored_file_name or not safe_stored_name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file reference.",
        )

    try:
        record = get_record_collection().find_one(
            {"stored_file_name": safe_stored_name},
            {"_id": 0, "file_name": 1, "health_id": 1},
        )
    except DatabaseConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while resolving record file.",
        ) from exc

    if not isinstance(record, dict):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record file not found.",
        )

    if current_user.role == ROLE_PATIENT and record.get("health_id") != current_user.health_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patients can only download their own files.",
        )

    file_path = RECORDS_DIR / safe_stored_name
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record file not found.",
        )

    download_name = str(record.get("file_name", safe_stored_name))
    return FileResponse(path=file_path, filename=download_name)


@router.get("/record/summary/{summary_stored_file_name}")
def download_summary_file(
    summary_stored_file_name: str,
    current_user: SessionUser = Depends(require_roles(ROLE_ADMIN, ROLE_PATIENT)),
) -> FileResponse:
    safe_stored_name = Path(summary_stored_file_name).name
    if safe_stored_name != summary_stored_file_name or not safe_stored_name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid summary file reference.",
        )

    try:
        record = get_record_collection().find_one(
            {"summary_stored_file_name": safe_stored_name},
            {"_id": 0, "summary_file_name": 1, "health_id": 1},
        )
    except DatabaseConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except PyMongoError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while resolving summary file.",
        ) from exc

    if not isinstance(record, dict):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Summary file not found.",
        )

    if current_user.role == ROLE_PATIENT and record.get("health_id") != current_user.health_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patients can only download their own summary files.",
        )

    file_path = RECORDS_DIR / safe_stored_name
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Summary file not found.",
        )

    download_name = str(record.get("summary_file_name", safe_stored_name))
    return FileResponse(path=file_path, filename=download_name)
