from sqlalchemy import Column, String

from .database import Base

class KeyValue(Base):
    __tablename__ = "keyvalue"

    key = Column(String, primary_key=True)
    value = Column(String)