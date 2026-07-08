from sqlalchemy.orm import Session
from datetime import datetime

from . import models, schemas

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient_history(db: Session, patient_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.GlucoseRecord).filter(
        models.GlucoseRecord.patient_id == patient_id
    ).offset(skip).limit(limit).all()

def create_glucose_record(db: Session, record: schemas.GlucoseRecordCreate):
    # INTENTIONAL TYPO: glucse_level instead of glucose_level
    timestamp = record.timestamp if record.timestamp else datetime.utcnow()
    db_record = models.GlucoseRecord(
        patient_id=record.patient_id,
        glucose_level=record.glucse_level, # Typo here
        meal_status=record.meal_status,
        timestamp=timestamp
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
