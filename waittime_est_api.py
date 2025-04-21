from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
import joblib
import pandas as pd
from typing import Optional

import redis
cache = redis.Redis(host="localhost",)
# Load the trained model
model = joblib.load("fine_tuned_queue_wait_model.pkl")

# Define the FastAPI app
app = FastAPI(title="Queue Wait Time Predictor")

# CORS setup
origins = [
    "http://localhost:5173",  # Allow your React frontend in dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input schema with additional fields
class PredictionInput(BaseModel):
    estimated_wait_time: int  
    join_method: Literal["QR Join", "Walk-in Join", "Schedule Join", "Token", "Token Based Join", "STAFF_ADDED"]
    special_note: Literal["None", "Elderly", "Disabled", "VIP", "Emergency"]
    join_hour: int  # hour of day (0–23)
    join_dayofweek: int  # day of week (0=Monday, 6=Sunday)
    time_taken_by_prev: Optional[float] = None  # New field: previous user's actual time
    index: int  # New field: position in the queue

# Prediction endpoint
@app.post("/predict")
def predict_wait_time(input_data: PredictionInput):
    # Extract data for model input
    model_input = pd.DataFrame([{
        "estimated_wait_time": input_data.estimated_wait_time,
        "join_method": input_data.join_method,
        "special_note": input_data.special_note,
        "join_hour": input_data.join_hour,
        "join_dayofweek": input_data.join_dayofweek,
    }])
    
    print(model_input.values)
    # Predict base wait time
    base_prediction = model.predict(model_input)[0]
    
    # Adjust prediction using time_taken_by_prev and index

    if input_data.time_taken_by_prev!=None:
        base_prediction = (base_prediction + input_data.time_taken_by_prev) / 2
    final_prediction = base_prediction * input_data.index
    print(input_data.time_taken_by_prev)
    print(input_data.index)

    return {
        "predicted_wait_time": round(final_prediction, 2),
        "unit": "minutes"
    }
