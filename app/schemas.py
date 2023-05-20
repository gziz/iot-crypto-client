from typing import List, Optional, Tuple
from pydantic import BaseModel
from datetime import datetime


class KeyValue(BaseModel):
    key: str
    value: str


class SensorData(BaseModel):
    created: Optional[str]
    value : float = 10.0
    type_ : str = "Temperature"
    sensor_id : int = 1


class Variables(BaseModel):
    url: str
    client_path: Tuple[str, str]
    d: int
    ca_cert_path: str
