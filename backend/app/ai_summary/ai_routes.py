from __future__ import annotations

from fastapi import APIRouter, status
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from .security_policy import (
    UNAUTHORIZED_AI_ACCESS_MESSAGE,
    UnauthorizedAIAccessError,
    enforce_ai_access,
    log_ai_access,
)
from .summarizer import (
    MODEL_NAME,
    SummarizerUnavailableError,
    get_summarizer_error,
    generate_medical_summary,
    is_summarizer_ready,
)

router = APIRouter(tags=["AI Summary"])


class AISummaryRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    user_id: str = Field(..., min_length=1, max_length=120)
    role: str = Field(..., min_length=1, max_length=40)
    health_id: str = Field(..., min_length=1, max_length=120)
    report_text: str = Field(..., min_length=1)


class AISummaryResponse(BaseModel):
    summary: str


class AISummaryHealthResponse(BaseModel):
    ready: bool
    model: str
    status: str
    reason: str | None = None


@router.get("/ai/health", response_model=AISummaryHealthResponse)
async def ai_summary_health() -> AISummaryHealthResponse:
    ready = is_summarizer_ready()
    reason = None if ready else get_summarizer_error()
    return AISummaryHealthResponse(
        ready=ready,
        model=MODEL_NAME,
        status="ready" if ready else "not_ready",
        reason=reason,
    )


@router.post("/ai/summary", response_model=AISummaryResponse)
async def ai_summary(payload: AISummaryRequest):
    try:
        enforce_ai_access(payload.user_id, payload.role, payload.health_id)
    except UnauthorizedAIAccessError:
        log_ai_access(payload.user_id, payload.health_id)
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"error": UNAUTHORIZED_AI_ACCESS_MESSAGE},
        )

    try:
        summary = await run_in_threadpool(
            generate_medical_summary,
            payload.report_text,
        )
    except ValueError as exc:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": str(exc)},
        )
    except SummarizerUnavailableError as exc:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"error": str(exc)},
        )

    log_ai_access(payload.user_id, payload.health_id)
    return AISummaryResponse(summary=summary)
