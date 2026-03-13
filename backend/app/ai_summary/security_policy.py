from __future__ import annotations

import logging
import os
from datetime import datetime, timezone

ALLOWED_AI_ROLES = {"hospital", "doctor"}
AI_SUMMARY_ACTION = "AI_SUMMARY"
UNAUTHORIZED_AI_ACCESS_MESSAGE = "Unauthorized AI access"

logger = logging.getLogger("ai_summary_access")


class UnauthorizedAIAccessError(Exception):
    """Raised when a caller is not allowed to run AI summarization."""


def _env_flag(name: str, default: str = "1") -> bool:
    raw = os.getenv(name, default).strip().lower()
    return raw not in {"0", "false", "no", "off"}


def offline_mode_enabled() -> bool:
    """
    Return whether strict offline model mode is enabled.

    Default:
    - enabled (1) for healthcare privacy-by-default posture.
    """
    return _env_flag("AI_SUMMARY_OFFLINE_MODE", "1")


def get_model_dir() -> str | None:
    """
    Optional local model directory override.

    If provided, the summarizer loads directly from this local path.
    """
    value = os.getenv("AI_SUMMARY_MODEL_DIR", "").strip()
    return value or None


def enforce_local_ai_runtime() -> None:
    """
    Enforce local-only AI runtime settings.

    Policy:
    1) AI runs locally only.
    2) No external API calls.

    Notes:
    - Deployment should pre-download model artifacts onto the host.
    - Telemetry is disabled by default.
    - Offline mode is enabled by default for strict privacy.
    """
    os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
    if offline_mode_enabled():
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
    else:
        # Optional bootstrap mode for one-time model download.
        os.environ["HF_HUB_OFFLINE"] = "0"
        os.environ["TRANSFORMERS_OFFLINE"] = "0"


def _clean(value: str | None) -> str:
    return value.strip() if isinstance(value, str) else ""


def enforce_ai_access(user_id: str, role: str, health_id: str) -> None:
    """
    Validate request-level access controls for AI usage.

    Required fields:
    - user_id
    - role
    - health_id

    Allowed roles:
    - hospital
    - doctor
    """
    cleaned_user_id = _clean(user_id)
    cleaned_role = _clean(role).lower()
    cleaned_health_id = _clean(health_id)

    if not cleaned_user_id or not cleaned_role or not cleaned_health_id:
        raise UnauthorizedAIAccessError(UNAUTHORIZED_AI_ACCESS_MESSAGE)

    if cleaned_role not in ALLOWED_AI_ROLES:
        raise UnauthorizedAIAccessError(UNAUTHORIZED_AI_ACCESS_MESSAGE)


def log_ai_access(user_id: str, health_id: str) -> None:
    """
    Audit log for AI access events.

    Required format fields:
    - user_id
    - health_id
    - timestamp
    - action = "AI_SUMMARY"
    """
    logger.info(
        "user_id=%s health_id=%s timestamp=%s action=%s",
        _clean(user_id),
        _clean(health_id),
        datetime.now(timezone.utc).isoformat(),
        AI_SUMMARY_ACTION,
    )
