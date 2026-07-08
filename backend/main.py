from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Healthcare Monitoring API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Healthcare Monitoring API"}

@app.post("/api/patients/", response_model=schemas.Patient)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db=db, patient=patient)

@app.get("/api/patients/{patient_id}", response_model=schemas.Patient)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@app.post("/api/glucose/", response_model=schemas.GlucoseRecord)
def create_glucose_record(record: schemas.GlucoseRecordCreate, db: Session = Depends(get_db)):
    # Verify patient exists
    db_patient = crud.get_patient(db, patient_id=record.patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return crud.create_glucose_record(db=db, record=record)

@app.get("/api/patients/{patient_id}/history", response_model=List[schemas.GlucoseRecord])
def read_patient_history(patient_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return crud.get_patient_history(db=db, patient_id=patient_id, skip=skip, limit=limit)
