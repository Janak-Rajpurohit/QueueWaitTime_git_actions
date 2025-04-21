from fastapi import APIRouter
import pandas as pd
from app.schemas import PredictionInput
from app.model import model

router = APIRouter()

@router.post("/predict")
def predict_wait_time(input_data: PredictionInput):
    model_input = pd.DataFrame([{
        "estimated_wait_time": input_data.estimated_wait_time,
        "join_method": input_data.join_method,
        "special_note": input_data.special_note,
        "join_hour": input_data.join_hour,
        "join_dayofweek": input_data.join_dayofweek,
    }])
    
    base_prediction = model.predict(model_input)[0]

    if input_data.time_taken_by_prev is not None:
        base_prediction = (base_prediction + input_data.time_taken_by_prev) / 2
    
    final_prediction = base_prediction * input_data.index

    return {
        "predicted_wait_time": round(final_prediction, 2),
        "unit": "minutes"
    }
