from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class GlucoseRecordBase(BaseModel):
    glucose_level: float
    meal_status: str

class GlucoseRecordCreate(GlucoseRecordBase):
    patient_id: int
    timestamp: Optional[datetime] = None

class GlucoseRecord(GlucoseRecordBase):
    id: int
    patient_id: int
    timestamp: datetime

    class Config:
        orm_mode = True


class PatientBase(BaseModel):
    name: str
    age: int
    gender: str
    diabetes_type: str
    medication: str

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    glucose_records: List[GlucoseRecord] = []

    class Config:
        orm_mode = True

class ChatRequest(BaseModel):
    message: str
