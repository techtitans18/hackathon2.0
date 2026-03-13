from .db import (
    get_database,
    get_hospital_collection,
    get_patient_collection,
    get_record_collection,
    initialize_database,
)

__all__ = [
    "get_database",
    "get_patient_collection",
    "get_hospital_collection",
    "get_record_collection",
    "initialize_database",
]
