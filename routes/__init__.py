from .hospital_routes import router as hospital_router
from .patient_routes import router as patient_router
from .record_routes import router as record_router

__all__ = ["patient_router", "hospital_router", "record_router"]
