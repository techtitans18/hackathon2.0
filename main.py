import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


from app.ai_summary.ai_routes import router as ai_summary_router
from app.emergency.emergency_routes import router as emergency_router
from app.ai_summary.summarizer import (
    SummarizerUnavailableError,
    load_summarizer_model,
)
from database.db import DatabaseConnectionError, initialize_database
from routes.admin_routes import router as admin_router
from routes.auth_routes import router as auth_router
from routes.hospital_routes import router as hospital_router
from routes.patient_routes import router as patient_router
from routes.patient_access_routes import router as patient_access_router
from routes.record_routes import router as record_router

logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
RECORDS_DIR = BASE_DIR / "records"

app = FastAPI(
    title="Healthcare Blockchain Backend API",
    description=(
        "Demo healthcare blockchain backend where sensitive medical files are "
        "stored locally and only metadata + hashes are written to blockchain."
    ),
    version="1.0.0",
)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR, check_dir=False),
    name="static",
)


@app.on_event("startup")
def on_startup() -> None:
    # Ensure local storage folder exists for uploaded records.
    RECORDS_DIR.mkdir(parents=True, exist_ok=True)
    try:
        initialize_database()
    except DatabaseConnectionError as exc:
        logger.warning("%s", exc)
    try:
        load_summarizer_model()
    except SummarizerUnavailableError as exc:
        logger.warning("%s", exc)


@app.get("/")
def health_check() -> dict[str, str]:
    return {"message": "Healthcare Blockchain API is running"}


@app.get("/app", include_in_schema=False)
def frontend_app() -> FileResponse:
    return _serve_frontend_page("index.html")


@app.get("/app/admin", include_in_schema=False)
def frontend_admin() -> FileResponse:
    return _serve_frontend_page("admin.html")


@app.get("/app/hospital", include_in_schema=False)
def frontend_hospital() -> FileResponse:
    return _serve_frontend_page("hospital.html")


@app.get("/app/patient", include_in_schema=False)
def frontend_patient() -> FileResponse:
    return _serve_frontend_page("patient.html")


def _serve_frontend_page(file_name: str) -> FileResponse:
    index_file = FRONTEND_DIR / file_name
    if not index_file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Frontend page is missing: frontend/{file_name}.",
        )
    return FileResponse(index_file)


app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(patient_router)
app.include_router(hospital_router)
app.include_router(patient_access_router)
app.include_router(record_router)
app.include_router(ai_summary_router)
app.include_router(emergency_router)
