from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Patient:
    id: str
    name: str
    email: str
    phone: str
    date_of_birth: str
    blood_group: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            date_of_birth=data.get('date_of_birth'),
            blood_group=data.get('blood_group'),
            address=data.get('address'),
            emergency_contact=data.get('emergency_contact')
        )

@dataclass
class MedicalRecord:
    id: str
    patient_id: str
    hospital_id: str
    diagnosis: str
    treatment: str
    date: str
    doctor_name: str
    files: List[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            patient_id=data.get('patient_id'),
            hospital_id=data.get('hospital_id'),
            diagnosis=data.get('diagnosis'),
            treatment=data.get('treatment'),
            date=data.get('date'),
            doctor_name=data.get('doctor_name'),
            files=data.get('files', [])
        )
