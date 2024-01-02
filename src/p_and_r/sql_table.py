"""mellow heeler database table definitions"""

from datetime import datetime, timezone

from sqlalchemy import Column
from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, String

from sqlalchemy.orm import registry
from sqlalchemy.ext.declarative import declared_attr

mapper_registry = registry()

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class LoadLog(Base):
    """load_log table definition"""

    __tablename__ = "load_log"

    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_type = Column(String)
    time_stamp = Column(DateTime)

    def __init__(self, file_name, file_type):
        self.file_name = file_name
        self.file_type = file_type
        self.time_stamp = datetime.now(timezone.utc)

    def __repr__(self):
        if self.id is None:
            self.id = 0

        return f"<load_log({self.id}, {self.file_name}, {self.file_type})>"

class Observation(Base):
    """xxxx"""

    __tablename__ = "observation"

    id = Column(Integer, primary_key=True)

    device = Column(String)
    time_stamp = Column(DateTime)

    altitude = Column(Integer)
    hex = Column(String)
    flight = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Integer)
    track = Column(Integer)
#