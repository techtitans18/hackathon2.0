from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from database.db import get_blockchain_collection


class HealthcareBlockchain:
    """Simple append-only blockchain for medical record integrity."""

    def __init__(self) -> None:
        self._chain: list[dict[str, Any]] = []
        self._load_from_db()
        if not self._chain:
            self._create_genesis_block()

    def _load_from_db(self) -> None:
        """Load blockchain from MongoDB on startup."""
        try:
            collection = get_blockchain_collection()
            blocks = list(collection.find({}, {"_id": 0}).sort("index", 1))
            self._chain = blocks
        except Exception:
            pass

    def _create_genesis_block(self) -> None:
        genesis_block = {
            "index": 0,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "HealthID": "GENESIS",
            "HospitalID": "GENESIS",
            "RecordType": "GENESIS",
            "RecordHash": "0",
            "previous_hash": "0",
        }
        genesis_block["hash"] = self.generate_hash(genesis_block)
        self._chain.append(genesis_block)
        self._save_block_to_db(genesis_block)

    def generate_hash(self, block_data: dict[str, Any]) -> str:
        payload = json.dumps(block_data, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def create_block(
        self,
        health_id: str,
        hospital_id: str,
        record_type: str,
        record_hash: str,
    ) -> dict[str, Any]:
        previous_hash = self._chain[-1]["hash"]
        block = {
            "index": len(self._chain),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "HealthID": health_id,
            "HospitalID": hospital_id,
            "RecordType": record_type,
            "RecordHash": record_hash,
            "previous_hash": previous_hash,
        }
        block["hash"] = self.generate_hash(block)
        self._chain.append(block)
        self._save_block_to_db(block)
        return block

    def _save_block_to_db(self, block: dict[str, Any]) -> None:
        """Persist block to MongoDB."""
        try:
            collection = get_blockchain_collection()
            collection.replace_one({"index": block["index"]}, block, upsert=True)
        except Exception:
            pass

    def get_chain(self) -> list[dict[str, Any]]:
        return list(self._chain)


healthcare_chain = HealthcareBlockchain()
