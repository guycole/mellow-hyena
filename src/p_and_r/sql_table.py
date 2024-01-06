"""mellow heeler database table definitions"""

import time

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
    device = Column(String)
    file_name = Column(String)
    file_type = Column(String)
    load_time = Column(DateTime)
    obs_time = Column(DateTime)

    def __init__(self, file_name, file_type, device, obs_time):
        self.device = device
        self.file_name = file_name
        self.file_type = file_type
        self.load_time = datetime.now(timezone.utc)
        self.obs_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(obs_time))

    def __repr__(self):
        if self.id is None:
            self.id = 0

        return f"<load_log({self.id}, {self.file_name}, {self.file_type})>"

class Aircraft(Base):
    """aircraft table definition"""

    __tablename__ = "aircraft"

    id = Column(Integer, primary_key=True)

    aircraft = Column(String)
    callsign = Column(String)
    hex = Column(String)
    version = Column(Integer)

    def __init__(self, aircraft, callsign, hex, version):
        self.aircraft = aircraft
        self.callsign = callsign
        self.hex = hex
        self.version = version

    def __repr__(self):
        if self.id is None:
            self.id = 0

        return f"<aircraft({self.hex}, {self.callsign}, {self.aircraft}, {self.version})>"

class Observation(Base):
    """observation table definition"""

    __tablename__ = "observation"

    id = Column(Integer, primary_key=True)

    aircraft_id = Column(BigInteger)
    load_log_id = Column(BigInteger)

    altitude = Column(Integer)
    hex = Column(String)
    flight = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Integer)
    track = Column(Integer)

    def __init__(self, aircraft_id, load_log_id, altitude, hex, flight, latitude, longitude, speed, track):
        self.aircraft_id = aircraft_id
        self.load_log_id = load_log_id
        self.altitude = altitude
        self.hex = hex
        self.flight = flight
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed
        self.track = track

    def __repr__(self):
        if self.id is None:
            self.id = 0

        return f"<observation({self.id}, {self.aircraft_id}, {self.hex})>"