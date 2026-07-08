from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    diabetes_type = Column(String)
    medication = Column(String)

    glucose_records = relationship("GlucoseRecord", back_populates="patient")


class GlucoseRecord(Base):
    __tablename__ = "glucose_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    glucose_level = Column(Float)
    meal_status = Column(String)

    patient = relationship("Patient", back_populates="glucose_records")
