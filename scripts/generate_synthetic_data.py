import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from datetime import datetime, timedelta
from backend.database import SessionLocal, engine
from backend import models, crud, schemas

# Initialize DB tables
models.Base.metadata.create_all(bind=engine)

def generate_data():
    db = SessionLocal()
    
    # 1. Create a synthetic patient
    patient_data = schemas.PatientCreate(
        name="Ali",
        age=45,
        gender="Male",
        diabetes_type="Type 2",
        medication="Metformin"
    )
    
    # Check if patient exists
    existing_patient = crud.get_patient(db, patient_id=1)
    if not existing_patient:
        patient = crud.create_patient(db, patient_data)
        patient_id = patient.id
        print(f"Created patient: {patient.name} (ID: {patient_id})")
    else:
        patient_id = existing_patient.id
        print(f"Patient already exists (ID: {patient_id})")
    
    # 2. Generate 30 days of data
    start_date = datetime.now() - timedelta(days=30)
    
    for day in range(30):
        current_date = start_date + timedelta(days=day)
        
        # Fasting glucose (Morning)
        fasting_glucose = int(np.random.normal(110, 15))
        crud.create_glucose_record(db, schemas.GlucoseRecordCreate(
            patient_id=patient_id,
            glucose_level=fasting_glucose,
            meal_status="Fasting",
            timestamp=current_date.replace(hour=8, minute=0, second=0, microsecond=0)
        ))
        
        # Post-lunch
        post_lunch = int(np.random.normal(160, 20))
        crud.create_glucose_record(db, schemas.GlucoseRecordCreate(
            patient_id=patient_id,
            glucose_level=post_lunch,
            meal_status="Post-Meal",
            timestamp=current_date.replace(hour=14, minute=0, second=0, microsecond=0)
        ))
        
        # Post-dinner (10% chance of a high spike)
        if np.random.rand() > 0.9:
            post_dinner = int(np.random.normal(260, 15)) # Alert trigger!
        else:
            post_dinner = int(np.random.normal(150, 15))
            
        crud.create_glucose_record(db, schemas.GlucoseRecordCreate(
            patient_id=patient_id,
            glucose_level=post_dinner,
            meal_status="Post-Meal",
            timestamp=current_date.replace(hour=20, minute=0, second=0, microsecond=0)
        ))
        
    print("Successfully generated 30 days of synthetic glucose data!")
    db.close()

if __name__ == "__main__":
    generate_data()
