from crewai.tools import tool
from backend.database import SessionLocal
from backend import crud

@tool
def fetch_patient_history(patient_id: str) -> str:
    """
    Fetches the historical glucose records for a given patient_id.
    Input should be the patient_id (e.g. '1').
    Returns a formatted string of the patient's glucose readings.
    """
    try:
        pid = int(patient_id)
        db = SessionLocal()
        records = crud.get_patient_history(db, patient_id=pid, limit=14) # Get last 14 records
        db.close()
        
        if not records:
            return f"No glucose records found for patient ID {pid}."
        
        formatted_records = []
        for r in records:
            formatted_records.append(
                f"Date: {r.timestamp.strftime('%Y-%m-%d %H:%M')}, "
                f"Glucose: {r.glucose_level} mg/dL, "
                f"Meal Status: {r.meal_status}"
            )
        
        return "\n".join(formatted_records)
    except Exception as e:
        return f"Error fetching data: {str(e)}"
