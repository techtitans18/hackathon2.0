from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HospitalRegistrationRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    hospital_name: str = Field(..., min_length=2, max_length=180)
    hospital_type: str = Field(..., min_length=2, max_length=120)


class HospitalRegistrationResponse(BaseModel):
    HospitalID: str


class HospitalUpdateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    hospital_name: str = Field(..., min_length=2, max_length=180)
    hospital_type: str = Field(..., min_length=2, max_length=120)


class HospitalUpdateResponse(BaseModel):
    message: str
    hospital_id: str


class Hospital(BaseModel):
    hospital_id: str
    hospital_name: str
    hospital_type: str
    created_at: datetime


class HospitalListResponse(BaseModel):
    hospitals: list[Hospital]
