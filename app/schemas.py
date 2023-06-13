from typing import List, Optional, Tuple
from pydantic import BaseModel
from datetime import datetime


class KeyValue(BaseModel):
    key: str
    value: str


class SensorData(BaseModel):
    date_time: Optional[str]
    value : float
    type_ : str
    sensor_id : int = 1


class Variables(BaseModel):
    url: str
    client_key_path: str
    client_cert_path: str
    d: int
    ca_cert_path: str
