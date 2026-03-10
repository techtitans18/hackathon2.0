from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EmergencySearchRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    role: str = Field(..., min_length=1, max_length=40)
    search_type: Literal["health_id", "phone", "name_dob"]
    value: str | None = Field(default=None, max_length=120)
    name: str | None = Field(default=None, min_length=1, max_length=120)
    dob: str | None = Field(default=None, min_length=1, max_length=20)

    @model_validator(mode="after")
    def _validate_search_input(self) -> EmergencySearchRequest:
        if self.search_type in {"health_id", "phone"} and not self.value:
            raise ValueError("value is required for search_type health_id or phone.")
        if self.search_type == "name_dob" and (not self.name or not self.dob):
            raise ValueError("name and dob are required for search_type name_dob.")
        return self


class EmergencySearchResponse(BaseModel):
    health_id: str
    name: str


class EmergencyProfileRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    role: str = Field(..., min_length=1, max_length=40)
    health_id: str = Field(..., min_length=1, max_length=120)


class EmergencyProfileResponse(BaseModel):
    health_id: str
    name: str
    blood_group: str
    allergies: list[str]
    diseases: list[str]
    surgeries: list[str]
    emergency_contact: str
    blockchain_status: str


class EmergencyDataUpsertRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    role: str = Field(..., min_length=1, max_length=40)
    health_id: str = Field(..., min_length=1, max_length=120)
    blood_group: str = Field(..., min_length=2, max_length=5)
    emergency_contact: str = Field(..., min_length=7, max_length=20)
    allergies: list[str] = Field(default_factory=list)
    diseases: list[str] = Field(default_factory=list)
    surgeries: list[str] = Field(default_factory=list)


class EmergencyDataUpsertResponse(BaseModel):
    health_id: str
    blood_group: str
    blockchain_hash: str
    message: str
