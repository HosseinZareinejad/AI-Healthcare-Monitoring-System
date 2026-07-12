from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict

from . import crud, models, schemas
from .database import SessionLocal, engine
from ai.crew import run_analysis_crew, run_chat_crew

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Healthcare Monitoring API")

class ConnectionManager:
    def __init__(self):
        # Maps patient_id to a list of active websocket connections
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, patient_id: int):
        await websocket.accept()
        if patient_id not in self.active_connections:
            self.active_connections[patient_id] = []
        self.active_connections[patient_id].append(websocket)

    def disconnect(self, websocket: WebSocket, patient_id: int):
        if patient_id in self.active_connections:
            self.active_connections[patient_id].remove(websocket)

    async def broadcast_to_patient(self, message: dict, patient_id: int):
        if patient_id in self.active_connections:
            for connection in self.active_connections[patient_id]:
                try:
                    await connection.send_json(message)
                except:
                    pass

manager = ConnectionManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
async def create_glucose_record(record: schemas.GlucoseRecordCreate, db: Session = Depends(get_db)):
    # Verify patient exists
    db_patient = crud.get_patient(db, patient_id=record.patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    new_record = crud.create_glucose_record(db=db, record=record)
    
    # Broadcast to websockets
    record_dict = {
        "id": new_record.id,
        "patient_id": new_record.patient_id,
        "timestamp": new_record.timestamp.isoformat(),
        "glucose_level": new_record.glucose_level,
        "meal_status": new_record.meal_status
    }
    await manager.broadcast_to_patient(record_dict, record.patient_id)
    
    return new_record

@app.get("/api/patients/{patient_id}/history", response_model=List[schemas.GlucoseRecord])
def read_patient_history(patient_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return crud.get_patient_history(db=db, patient_id=patient_id, skip=skip, limit=limit)

@app.websocket("/api/patients/{patient_id}/ws")
async def websocket_endpoint(websocket: WebSocket, patient_id: int):
    await manager.connect(websocket, patient_id)
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, patient_id)

@app.post("/api/patients/{patient_id}/analyze")
def analyze_patient(patient_id: int, db: Session = Depends(get_db)):
    # Check if patient exists
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    try:
        # Fetch history to inject into prompt
        records = crud.get_patient_history(db, patient_id=patient_id, limit=20)
        formatted_data = "\n".join([f"Date: {r.timestamp.strftime('%Y-%m-%d %H:%M')}, Glucose: {r.glucose_level} mg/dL, Meal Status: {r.meal_status}" for r in records]) if records else "No records found."
        
        # Run CrewAI analysis
        report = run_analysis_crew(str(patient_id), formatted_data)
        return {"patient_id": patient_id, "analysis_report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/patients/{patient_id}/chat")
def chat_with_ai(patient_id: int, request: schemas.ChatRequest, db: Session = Depends(get_db)):
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    try:
        # Fetch history to inject into prompt
        records = crud.get_patient_history(db, patient_id=patient_id, limit=20)
        formatted_data = "\n".join([f"Date: {r.timestamp.strftime('%Y-%m-%d %H:%M')}, Glucose: {r.glucose_level} mg/dL, Meal Status: {r.meal_status}" for r in records]) if records else "No records found."
        
        response = run_chat_crew(str(patient_id), formatted_data, request.message)
        return {"patient_id": patient_id, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")
