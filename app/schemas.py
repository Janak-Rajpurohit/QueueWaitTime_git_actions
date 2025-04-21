from pydantic import BaseModel
from typing import Literal, Optional

class PredictionInput(BaseModel):
    estimated_wait_time: int  
    join_method: Literal["QR Join", "Walk-in Join", "Schedule Join", "Token", "Token Based Join", "STAFF_ADDED"]
    special_note: Literal["None", "Elderly", "Disabled", "VIP", "Emergency"]
    join_hour: int
    join_dayofweek: int
    time_taken_by_prev: Optional[float] = None
    index: int
