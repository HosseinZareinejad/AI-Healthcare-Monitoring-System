import requests
import time
import random
from datetime import datetime

import os

# Assuming FastAPI runs locally on port 8000 by default
base_url = os.getenv("API_URL", "http://localhost:8000")
API_URL = f"{base_url.rstrip('/')}/api/glucose/"
PATIENT_ID = 1

def simulate_real_time_data():
    print(f"Starting real-time data simulator for patient {PATIENT_ID}...")
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
                print("Connection error. Make sure the FastAPI server is running on http://localhost:8000")
            
            # Wait for 10 seconds before sending the next reading
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nSimulator stopped.")

if __name__ == "__main__":
    simulate_real_time_data()
