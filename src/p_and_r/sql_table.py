"""mellow heeler database table definitions"""

import time

from datetime import datetime, timezone

from typing import List, Dict

from sqlalchemy import Column
from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, SmallInteger, String

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
        self.device = args['device']
        self.file_name = args['file_name']
        self.file_type = args['file_type']
        self.load_time = datetime.now(timezone.utc)        
        self.obs_time = args['obs_time']
        self.population = args['population']

    def __repr__(self):
        if self.id is None:
            self.id = 0

        return f"load_log({self.id}, {self.file_name}, {self.file_type})"

class Aircraft(Base):
    """aircraft table definition"""

    __tablename__ = "aircraft"

    id = Column(Integer, primary_key=True)

    air_type = Column(String)
    callsign = Column(String)
    hex = Column(String)
    version = Column(Integer)

    def __init__(self, args: Dict[str, str]):
        self.air_type = args['air_type']
        self.callsign = args['callsign']
        self.hex = args['hex']
        self.version = args['version']

    def __repr__(self):
        if self.id is None:
            self.id = 0

        return f"aircraft({self.hex}, {self.callsign}, {self.aircraft}, {self.version})"

class Observation(Base):
    """observation table definition"""

    __tablename__ = "observation"

    id = Column(Integer, primary_key=True)

    aircraft_id = Column(BigInteger)
    load_log_id = Column(BigInteger)
    obs_time = Column(DateTime)

    altitude = Column(Integer)
    hex = Column(String)
    flight = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Integer)
    track = Column(Integer)

    def __init__(self, args: Dict[str, str]):
        self.aircraft_id = args['aircraft_id']
        self.load_log_id = args['load_log_id']
        self.obs_time = args['obs_time']
        self.altitude = args['altitude']
        self.hex = args['hex']
        self.flight = args['flight']
        self.latitude = args['latitude']
        self.longitude = args['longitude']
        self.speed = args['speed']
        self.track = args['track']

    def __repr__(self):
        if self.id is None:
            self.id = 0

        return f"observation({self.id}, {self.aircraft_id}, {self.hex})"