from sqlalchemy import Column, String, DateTime, Integer, Boolean, Float

from .database import Base

class KeyValue(Base):
    __tablename__ = "keyvalue"

    key = Column(String, primary_key=True)
    value = Column(String)


class SensorData(Base):
    __tablename__ = "sensors_data"
    id = Column(Integer, primary_key=True, index=True)
    type_ = Column(Integer)
    date_time = Column(String)
    value = Column(Float)
    sent = Column(Integer)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}