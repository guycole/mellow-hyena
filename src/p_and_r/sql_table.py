"""mellow hyena database table definitions"""

from datetime import datetime, timezone

from typing import Dict

from sqlalchemy import Column

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Float,
    Integer,
    SmallInteger,
    String,
)

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
    device = Column(String)
    file_name = Column(String)
    file_type = Column(String)
    load_time = Column(DateTime)
    obs_time = Column(DateTime)
    population = Column(SmallInteger)

    def __init__(self, args: Dict[str, str]):
        self.device = args["device"]
        self.file_name = args["file_name"]
        self.file_type = args["file_type"]
        self.load_time = datetime.now(timezone.utc)
        self.obs_time = args["obs_time"]
        self.population = args["population"]

    def __repr__(self):
        if self.id is None:
            self.id = 0

        return f"load_log({self.id}, {self.file_name}, {self.file_type})"


class Aircraft(Base):
    """aircraft table definition"""

    __tablename__ = "aircraft"

    id = Column(Integer, primary_key=True)
    adsb_hex = Column(String)
    category = Column(String)
    emergency = Column(String)
    flight = Column(String)
    model = Column(String)
    registration = Column(String)
    ladd_flag = Column(Boolean)
    military_flag = Column(Boolean)
    pia_flag = Column(Boolean)
    wierdo_flag = Column(Boolean)
    version = Column(Integer)

    def __init__(self, args: Dict[str, str]):
        self.adsb_hex = args["adsb_hex"]
        self.category = args["category"]
        self.emergency = args["emergency"]
        self.flight = args["flight"]
        self.model = args["model"]
        self.registration = args["registration"]
        self.ladd_flag = args["ladd_flag"]
        self.military_flag = args["military_flag"]
        self.pia_flag = args["pia_flag"]
        self.wierdo_flag = args["wierdo_flag"]
        self.version = args["version"]

    def __repr__(self):
        if self.id is None:
            self.id = 0

        return f"aircraft({self.adsb_hex}, {self.registration}, {self.model}, {self.version})"


class Observation(Base):
    """observation table definition"""

    __tablename__ = "observation"

    id = Column(Integer, primary_key=True)

    load_log_id = Column(BigInteger)
    obs_time = Column(DateTime)

    altitude = Column(Integer)
    adsb_hex = Column(String)
    flight = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Integer)
    track = Column(Integer)

    def __init__(self, args: Dict[str, str]):
        self.adsb_hex = args["adsb_hex"]
        self.load_log_id = args["load_log_id"]
        self.obs_time = args["obs_time"]
        self.altitude = args["altitude"]
        self.flight = args["flight"]
        self.latitude = args["latitude"]
        self.longitude = args["longitude"]
        self.speed = args["speed"]
        self.track = args["track"]

    def __repr__(self):
        if self.id is None:
            self.id = 0

        return f"observation({self.id}, {self.adsb_hex}, {self.flight})"
