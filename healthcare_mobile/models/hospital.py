from dataclasses import dataclass
from typing import Optional

@dataclass
class Hospital:
    id: str
    name: str
    address: str
    phone: str
    email: str
    license_number: str
    specializations: list = None
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            address=data.get('address'),
            phone=data.get('phone'),
            email=data.get('email'),
            license_number=data.get('license_number'),
            specializations=data.get('specializations', [])
        )
