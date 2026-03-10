from __future__ import annotations

import logging
from pathlib import Path
from threading import Lock
from typing import Any

from .security_policy import (
    enforce_local_ai_runtime,
    get_model_dir,
    offline_mode_enabled,
)

MODEL_NAME = "facebook/bart-large-cnn"
SUMMARY_MAX_LENGTH = 120
SUMMARY_MIN_LENGTH = 30

logger = logging.getLogger(__name__)

_summarizer_lock = Lock()
_summarizer: Any | None = None
_last_load_error: str | None = None
_active_task: str = "summarization"


class SummarizerUnavailableError(RuntimeError):
    """Raised when the local summarizer model is not available."""


def is_summarizer_ready() -> bool:
    """Return whether the summarizer model is loaded in memory."""
    return _summarizer is not None


def get_summarizer_error() -> str | None:
    """Return the last model-load/generation error for diagnostics."""
    return _last_load_error


def _resolve_model_source() -> tuple[str, bool]:
    configured_model_dir = get_model_dir()
    model_source = MODEL_NAME
    local_files_only = offline_mode_enabled()

    if configured_model_dir:
        model_path = Path(configured_model_dir).expanduser().resolve()
        if not model_path.exists() or not model_path.is_dir():
            raise SummarizerUnavailableError(
                f"Configured AI_SUMMARY_MODEL_DIR not found: {model_path}"
            )
        model_source = str(model_path)
        local_files_only = True

    return model_source, local_files_only


def _build_seq2seq_summarizer(model_source: str, local_files_only: bool) -> Any:
    """
    Build a local callable summarizer using AutoModelForSeq2SeqLM.

    This is a fallback for transformers builds where pipeline task aliases
    like "summarization" or "text2text-generation" are not registered.
    """
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        model_source,
        local_files_only=local_files_only,
    )
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_source,
        local_files_only=local_files_only,
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    def _run(
        text: str,
        max_length: int,
        min_length: int,
        do_sample: bool,
        truncation: bool,
    ) -> list[dict[str, str]]:
        token_limit = getattr(tokenizer, "model_max_length", 1024)
        if not isinstance(token_limit, int) or token_limit <= 0 or token_limit > 100000:
            token_limit = 1024

        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=bool(truncation),
            max_length=token_limit if truncation else None,
        )
        inputs = {key: value.to(device) for key, value in inputs.items()}

        with torch.no_grad():
            summary_ids = model.generate(
                **inputs,
                max_length=max_length,
                min_length=min_length,
                do_sample=do_sample,
            )

        summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return [{"summary_text": summary_text}]

    return _run


def load_summarizer_model() -> None:
    """
    Load the HuggingFace summarizer once for process lifetime.

    The model executes locally through transformers pipeline.
    """
    global _summarizer, _last_load_error, _active_task
    if _summarizer is not None:
        return

    with _summarizer_lock:
        if _summarizer is not None:
            return

        try:
            enforce_local_ai_runtime()
            # Import lazily so missing AI deps do not crash whole API startup.
            from transformers import pipeline

            model_source, local_files_only = _resolve_model_source()

            try:
                _summarizer = pipeline(
                    "summarization",
                    model=model_source,
                    local_files_only=local_files_only,
                )
                _active_task = "summarization"
            except Exception as task_exc:
                if "Unknown task" not in str(task_exc):
                    raise
                try:
                    _summarizer = pipeline(
                        "text2text-generation",
                        model=model_source,
                        local_files_only=local_files_only,
                    )
                    _active_task = "text2text-generation"
                except Exception as text2text_exc:
                    if "Unknown task" not in str(text2text_exc):
                        raise
                    _summarizer = _build_seq2seq_summarizer(
                        model_source=model_source,
                        local_files_only=local_files_only,
                    )
                    _active_task = "seq2seq-generate"
            _last_load_error = None
        except ModuleNotFoundError as exc:
            _last_load_error = (
                "transformers dependencies are missing. Install: "
                "pip install transformers torch sentencepiece"
            )
            raise SummarizerUnavailableError(
                _last_load_error
            ) from exc
        except SummarizerUnavailableError:
            raise
        except Exception as exc:
            if offline_mode_enabled():
                _last_load_error = (
                    "Model load failed in offline mode. "
                    "Either pre-download facebook/bart-large-cnn to local cache, "
                    "or run once with AI_SUMMARY_OFFLINE_MODE=0, then switch back to 1."
                )
            else:
                _last_load_error = f"Model load failed: {exc}"
            raise SummarizerUnavailableError(
                "Unable to load local summarization model."
            ) from exc

        logger.info("Loaded AI summarizer model: %s (task=%s)", MODEL_NAME, _active_task)


def _get_summarizer() -> Any:
    if _summarizer is None:
        raise SummarizerUnavailableError(
            "Summarizer model is not loaded. Run startup model loading first."
        )
    return _summarizer


def generate_medical_summary(text: str) -> str:
    """
    Generate a short medical summary from report text.

    Security:
    - Processes text in memory only.
    - Does not persist or mutate source records.
    """
    global _last_load_error
    cleaned_text = text.strip() if isinstance(text, str) else ""
    if not cleaned_text:
        raise ValueError("report_text must be a non-empty string.")

    summarizer = _get_summarizer()
    try:
        result = summarizer(
            cleaned_text,
            max_length=SUMMARY_MAX_LENGTH,
            min_length=SUMMARY_MIN_LENGTH,
            do_sample=False,
            truncation=True,
        )
    except Exception as exc:
        _last_load_error = f"Summary generation failed: {exc}"
        raise SummarizerUnavailableError(
            "Unable to generate summary from provided report text."
        ) from exc

    if not result:
        raise SummarizerUnavailableError("Summarizer returned an empty response.")

    summary_text = ""
    first_result = result[0]
    if isinstance(first_result, dict):
        summary_text = str(
            first_result.get("summary_text")
            or first_result.get("generated_text")
            or ""
        ).strip()
    if not summary_text:
        raise SummarizerUnavailableError("Summarizer returned invalid response payload.")

    return " ".join(summary_text.split())
