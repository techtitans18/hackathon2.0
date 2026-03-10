from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import PyMongoError

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional dependency at runtime
    load_dotenv = None

BASE_DIR = Path(__file__).resolve().parent.parent
if load_dotenv is not None:
    load_dotenv(BASE_DIR / ".env", override=False)

_raw_mongo_uri = (
    os.getenv("MONGO_URI")
    or os.getenv("MONGO_URL")
    or os.getenv("MONGODB_URI")
    or os.getenv("mongo_url")
)
MONGO_URI = _raw_mongo_uri or "mongodb://localhost:27017"
MONGO_DB_NAME = (
    os.getenv("MONGO_DB_NAME")
    or os.getenv("mongo_db_name")
    or os.getenv("mongo1")
    or "healthcare_blockchain"
)
USING_DEFAULT_URI = _raw_mongo_uri is None

_client: MongoClient | None = None
_database: Database | None = None


class DatabaseConnectionError(Exception):
    """Raised when MongoDB is unavailable for the API."""


def _mask_mongo_uri(uri: str) -> str:
    """Hide password if credentials are present in the URI."""
    try:
        parts = urlsplit(uri)
        if "@" not in parts.netloc:
            return uri

        credentials, host = parts.netloc.rsplit("@", 1)
        if ":" not in credentials:
            return uri

        username, _ = credentials.split(":", 1)
        safe_netloc = f"{username}:***@{host}"
        return urlunsplit(
            (parts.scheme, safe_netloc, parts.path, parts.query, parts.fragment)
        )
    except Exception:
        return "<configured-uri>"


def get_database() -> Database:
    global _client, _database
    if _database is None:
        try:
            if "<" in MONGO_URI and ">" in MONGO_URI:
                raise DatabaseConnectionError(
                    "MONGO_URI contains placeholder values. Replace <...> with real credentials."
                )
            _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            _client.admin.command("ping")
            _database = _client[MONGO_DB_NAME]
        except DatabaseConnectionError:
            raise
        except PyMongoError as exc:
            _client = None
            _database = None
            source_hint = (
                "default localhost fallback"
                if USING_DEFAULT_URI
                else "configured environment variable"
            )
            raise DatabaseConnectionError(
                f"MongoDB is unavailable at '{_mask_mongo_uri(MONGO_URI)}'. "
                f"Source: {source_hint}. Verify MONGO_URI/MONGO_URL, Atlas IP whitelist, and credentials. Reason: {exc}"
            ) from exc
    return _database


def initialize_database() -> None:
    db = get_database()
    db["patients"].create_index("health_id", unique=True)
    db["patients"].create_index("phone")
    db["patients"].create_index([("name", 1), ("dob", 1)])
    db["patients"].create_index(
        "email",
        unique=True,
        partialFilterExpression={"email": {"$type": "string"}},
    )
    db["hospitals"].create_index("hospital_id", unique=True)
    db["records"].create_index([("health_id", 1), ("timestamp", -1)])
    db["records"].create_index("stored_file_name", unique=True)
    db["users"].create_index("email", unique=True)
    db["users"].create_index(
        "health_id",
        unique=True,
        partialFilterExpression={"health_id": {"$type": "string"}},
    )
    db["users"].create_index(
        "hospital_id",
        unique=True,
        partialFilterExpression={"hospital_id": {"$type": "string"}},
    )
    db["users"].create_index([("role", 1), ("is_active", 1)])
    db["emergency_data"].create_index("health_id", unique=True)
    db["emergency_logs"].create_index([("health_id", 1), ("timestamp", -1)])
    db["emergency_logs"].create_index([("hospital_id", 1), ("timestamp", -1)])


def get_patient_collection() -> Collection:
    return get_database()["patients"]


def get_hospital_collection() -> Collection:
    return get_database()["hospitals"]


def get_record_collection() -> Collection:
    return get_database()["records"]


def get_user_collection() -> Collection:
    return get_database()["users"]


def get_emergency_data_collection() -> Collection:
    return get_database()["emergency_data"]


def get_emergency_log_collection() -> Collection:
    return get_database()["emergency_logs"]
