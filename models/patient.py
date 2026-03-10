from pydantic import BaseModel, ConfigDict, Field


class PatientRegistrationRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(..., min_length=2, max_length=120)
    age: int = Field(..., ge=0, le=130)
    phone: str = Field(..., min_length=7, max_length=20)
    email: str = Field(..., min_length=5, max_length=320)
    dob: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    blood_group: str = Field(..., min_length=2, max_length=5)
    photo_url: str | None = Field(default=None, max_length=1000)
    emergency_contact: str | None = Field(default=None, min_length=7, max_length=20)
    allergies: list[str] = Field(default_factory=list)
    diseases: list[str] = Field(default_factory=list)
    surgeries: list[str] = Field(default_factory=list)


class PatientRegistrationResponse(BaseModel):
    HealthID: str


class EHealthCardResponse(BaseModel):
    health_id: str
    name: str
    blood_group: str
    phone: str
    photo_url: str | None = None
