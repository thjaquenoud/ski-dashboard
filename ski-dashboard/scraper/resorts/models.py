# scraper/resorts/models.py
from pydantic import BaseModel
from typing import Literal

StatusType = Literal["OPEN", "CLOSED", "PREPARING", None]

class Installation(BaseModel):
    domain: str
    name: str
    lift_type: str
    status: StatusType

class Slope(BaseModel):
    domain: str
    name: str
    difficulty: str
    status: StatusType
