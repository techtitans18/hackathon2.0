"""AI summarization module."""

from .ai_routes import router as ai_summary_router
from .summarizer import (
    generate_medical_summary,
    get_summarizer_error,
    is_summarizer_ready,
    load_summarizer_model,
)

__all__ = [
    "ai_summary_router",
    "generate_medical_summary",
    "get_summarizer_error",
    "is_summarizer_ready",
    "load_summarizer_model",
]
