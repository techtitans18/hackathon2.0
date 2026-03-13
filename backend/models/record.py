from typing import Any

from pydantic import BaseModel


class AddRecordResponse(BaseModel):
    message: str
    record_id: str
    record_hash: str
    block: dict[str, Any]
    summary_file_name: str | None = None
    summary_download_url: str | None = None
