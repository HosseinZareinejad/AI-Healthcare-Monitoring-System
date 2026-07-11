import requests
import time
import random
from datetime import datetime

import os

# Assuming FastAPI runs locally on port 8000 by default
base_url = os.getenv("API_URL", "http://localhost:8000")
API_URL = f"{base_url.rstrip('/')}/api/glucose/"
PATIENT_ID = 1

def ensure_patient_exists():
    # Check if patient exists
    res = requests.get(f"{base_url.rstrip('/')}/api/patients/{PATIENT_ID}")
    if res.status_code == 404:
        print(f"Patient {PATIENT_ID} not found. Creating default patient...")
        patient_data = {
            "name": "Sarah Connor",
            "age": 45,
            "gender": "Female",
            "diabetes_type": "Type 2",
            "medication": "Metformin 500mg"
        }
        create_res = requests.post(f"{base_url.rstrip('/')}/api/patients/", json=patient_data)
        if create_res.status_code == 200:
            print("Patient created successfully!")
        else:
            print("Failed to create patient:", create_res.text)

def simulate_real_time_data():
    print(f"Starting real-time data simulator for patient {PATIENT_ID}...")
    
    # Wait a few seconds for the backend to start up
    time.sleep(5)
    try:
        ensure_patient_exists()
    except Exception as e:
        print("Could not connect to API for initial check:", e)
        
    try:
        while True:
            # Generate a realistic random glucose level
            new_glucose = int(random.gauss(140, 30))
            # Ensure it's not negative
            new_glucose = max(40, new_glucose)
            
            payload = {
                "patient_id": PATIENT_ID,
                "glucose_level": new_glucose,
                "meal_status": random.choice(["Fasting", "Post-Meal", "Random"]),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent new glucose data: {new_glucose} mg/dL")
                else:
                    print(f"Failed to send data: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                print("Connection error. Make sure the FastAPI server is running.")
            
            # Wait for 10 seconds before sending the next reading
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nSimulator stopped.")

if __name__ == "__main__":
    simulate_real_time_data()
