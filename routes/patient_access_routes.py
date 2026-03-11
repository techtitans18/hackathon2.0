from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from pymongo.errors import PyMongoError

from database.db import (
    DatabaseConnectionError,
    get_patient_collection,
    get_record_collection,
)
from routes.auth_routes import ROLE_HOSPITAL, SessionUser, require_roles

router = APIRouter(tags=["Patient Access"])

# In-memory OTP storage (for production, use Redis or database)
_otp_store: dict[str, dict] = {}
OTP_EXPIRY_MINUTES = 10
OTP_LENGTH = 6


class PatientAccessRequest(BaseModel):
    search_type: str = Field(..., pattern="^(health_id|mobile|email)$")
    search_value: str = Field(..., min_length=1)


class OTPSendResponse(BaseModel):
    message: str
    email_masked: str
    expires_in_minutes: int


class OTPVerifyRequest(BaseModel):
    search_type: str = Field(..., pattern="^(health_id|mobile|email)$")
    search_value: str = Field(..., min_length=1)
    otp: str = Field(..., min_length=6, max_length=6)


class PatientAccessResponse(BaseModel):
    patient: dict
    records: list[dict]


def _generate_otp() -> str:
    """Generate 6-digit OTP"""
    return "".join([str(secrets.randbelow(10)) for _ in range(OTP_LENGTH)])


def _mask_email(email: str) -> str:
    """Mask email for privacy: abc***@example.com"""
    if "@" not in email:
        return email[:3] + "***"
    local, domain = email.split("@", 1)
    if len(local) <= 3:
        return local[0] + "***@" + domain
    return local[:3] + "***@" + domain


def _send_otp_email(email: str, otp: str) -> None:
    """
    Send OTP via email using SMTP.
    Falls back to console logging if email fails.
    """
    import os
    
    # Check if SMTP is configured
    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = os.getenv('SMTP_PORT', '587')
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    smtp_from = os.getenv('SMTP_FROM', 'noreply@healthcare.com')
    
    # If SMTP not configured, print to console (development mode)
    if not smtp_host or not smtp_user or not smtp_password:
        print(f"\n{'='*60}")
        print(f"[OTP EMAIL - DEVELOPMENT MODE]")
        print(f"To: {email}")
        print(f"OTP: {otp}")
        print(f"Valid for: {OTP_EXPIRY_MINUTES} minutes")
        print(f"{'='*60}\n")
        return
    
    # Send actual email
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Healthcare Access OTP'
        msg['From'] = smtp_from
        msg['To'] = email
        
        # Email body
        text = f"""
Healthcare Access OTP

Your OTP for healthcare record access is: {otp}

This code is valid for {OTP_EXPIRY_MINUTES} minutes.

If you did not request this code, please ignore this email.

Thank you,
Healthcare System
"""
        
        html = f"""
<html>
  <body style="font-family: Arial, sans-serif; padding: 20px;">
    <div style="max-width: 600px; margin: 0 auto; border: 1px solid #ddd; border-radius: 8px; padding: 20px;">
      <h2 style="color: #007bff;">Healthcare Access OTP</h2>
      <p>Your OTP for healthcare record access is:</p>
      <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center; margin: 20px 0;">
        <h1 style="color: #007bff; margin: 0; font-size: 32px; letter-spacing: 5px;">{otp}</h1>
      </div>
      <p style="color: #666;">This code is valid for <strong>{OTP_EXPIRY_MINUTES} minutes</strong>.</p>
      <p style="color: #999; font-size: 12px; margin-top: 30px;">
        If you did not request this code, please ignore this email.
      </p>
      <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
      <p style="color: #999; font-size: 12px;">Healthcare System</p>
    </div>
  </body>
</html>
"""
        
        # Attach both plain text and HTML versions
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP(smtp_host, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        print(f"[OTP EMAIL] Successfully sent to {email}")
        
    except Exception as e:
        # If email fails, print to console as fallback
        print(f"[OTP EMAIL ERROR] Failed to send email: {e}")
        print(f"[OTP EMAIL - FALLBACK] To: {email}, OTP: {otp}")


def _store_otp(key: str, otp: str, email: str) -> datetime:
    """Store OTP with expiry"""
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=OTP_EXPIRY_MINUTES)
    _otp_store[key] = {
        "otp": otp,
        "email": email,
        "expires_at": expires_at,
        "attempts": 0,
    }
    return expires_at


def _verify_otp(key: str, otp: str) -> bool:
    """Verify OTP and check expiry"""
    stored = _otp_store.get(key)
    if not stored:
        return False

    # Check expiry
    if datetime.now(timezone.utc) > stored["expires_at"]:
        _otp_store.pop(key, None)
        return False

    # Check attempts (max 3)
    stored["attempts"] += 1
    if stored["attempts"] > 3:
        _otp_store.pop(key, None)
        return False

    # Verify OTP
    if stored["otp"] == otp:
        _otp_store.pop(key, None)
        return True

    return False


@router.post("/patient_access/send_otp", response_model=OTPSendResponse)
def send_patient_access_otp(
    request: PatientAccessRequest,
    current_user: SessionUser = Depends(require_roles(ROLE_HOSPITAL)),
) -> OTPSendResponse:
    """
    Send OTP to patient's email for hospital access verification.
    Hospital staff can search by Health ID, mobile number, or email.
    """
    # Debug logging
    print(f"[DEBUG] Current user role: {current_user.role}")
    print(f"[DEBUG] Current user hospital_id: {current_user.hospital_id}")
    print(f"[DEBUG] Search type: {request.search_type}")
    print(f"[DEBUG] Search value: {request.search_value}")
    
    try:
        # Find patient by health_id, phone, or email
        query = {}
        if request.search_type == "health_id":
            query = {"health_id": request.search_value.strip()}
        elif request.search_type == "mobile":
            query = {"phone": request.search_value.strip()}
        elif request.search_type == "email":
            query = {"email": request.search_value.strip().lower()}

        patient = get_patient_collection().find_one(query, {"_id": 0})

        # Debug logging
        print(f"[DEBUG] Search query: {query}")
        print(f"[DEBUG] Patient found: {patient is not None}")
        if patient:
            print(f"[DEBUG] Patient hospital: {patient.get('created_by_hospital_id')}")
            print(f"[DEBUG] Current hospital: {current_user.hospital_id}")

        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Patient not found with provided information. Query: {query}",
            )

        # REMOVED: Hospital restriction - Allow any hospital to access any patient
        # This enables cross-hospital patient access for better healthcare coordination

        email = patient.get("email")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Patient email not found. Cannot send OTP.",
            )

        # Generate and store OTP
        otp = _generate_otp()
        key = hashlib.sha256(
            f"{request.search_type}:{request.search_value}".encode()
        ).hexdigest()
        _store_otp(key, otp, email)

        # Send OTP via email
        _send_otp_email(email, otp)

        return OTPSendResponse(
            message="OTP sent successfully to patient's email.",
            email_masked=_mask_email(email),
            expires_in_minutes=OTP_EXPIRY_MINUTES,
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
            detail="Database error while processing patient access request.",
        ) from exc


@router.post("/patient_access/verify_otp", response_model=PatientAccessResponse)
def verify_patient_access_otp(
    request: OTPVerifyRequest,
    current_user: SessionUser = Depends(require_roles(ROLE_HOSPITAL)),
) -> PatientAccessResponse:
    """
    Verify OTP and return patient profile with medical records.
    """
    try:
        # Generate key
        key = hashlib.sha256(
            f"{request.search_type}:{request.search_value}".encode()
        ).hexdigest()

        # Verify OTP
        if not _verify_otp(key, request.otp.strip()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired OTP. Please request a new one.",
            )

        # Find patient
        query = {}
        if request.search_type == "health_id":
            query = {"health_id": request.search_value.strip()}
        elif request.search_type == "mobile":
            query = {"phone": request.search_value.strip()}
        elif request.search_type == "email":
            query = {"email": request.search_value.strip().lower()}

        patient = get_patient_collection().find_one(query, {"_id": 0})

        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found.",
            )

        # REMOVED: Hospital restriction - Allow any hospital to access any patient after OTP verification
        # This enables cross-hospital patient access for emergency and consultation purposes

        # Get patient records
        health_id = patient.get("health_id")
        records = list(
            get_record_collection()
            .find({"health_id": health_id}, {"_id": 0})
            .sort("timestamp", -1)
        )

        # Format records with download URLs
        formatted_records = []
        for record in records:
            stored_file_name = record.get("stored_file_name")
            summary_stored_file_name = record.get("summary_stored_file_name")
            formatted_records.append(
                {
                    "record_type": record.get("record_type"),
                    "description": record.get("description"),
                    "file_name": record.get("file_name"),
                    "download_url": f"/record/file/{stored_file_name}"
                    if stored_file_name
                    else None,
                    "summary_file_name": record.get("summary_file_name"),
                    "summary_download_url": f"/record/summary/{summary_stored_file_name}"
                    if summary_stored_file_name
                    else None,
                    "record_hash": record.get("record_hash"),
                    "timestamp": record.get("timestamp"),
                    "hospital_id": record.get("hospital_id"),
                }
            )

        return PatientAccessResponse(patient=patient, records=formatted_records)

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
            detail="Database error while verifying patient access.",
        ) from exc
