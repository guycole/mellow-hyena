"""mellow hyena database table definitions"""

from datetime import datetime, timezone

from typing import Dict

from sqlalchemy import Column

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
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

class AdsbExchange(Base):
    """adsb_exchange table definition"""

    __tablename__ = "adsb_exchange"

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

    def __init__(self, args: Dict[str, str]):
        self.adsb_hex = args["adsb_hex"].lower()
        self.category = args["category"]
        self.emergency = args["emergency"]
        self.flight = args["flight"]
        self.model = args["model"]
        self.registration = args["registration"]
        self.ladd_flag = args["ladd_flag"]
        self.military_flag = args["military_flag"]
        self.pia_flag = args["pia_flag"]
        self.wierdo_flag = args["wierdo_flag"]

    def __repr__(self):
        if self.id is None:
            self.id = 0

        return f"aircraft({self.adsb_hex}, {self.registration}, {self.model})"


class Cooked(Base):
    """cooked table definition"""

    __tablename__ = "cooked"

    id = Column(BigInteger, primary_key=True)
    adsb_hex = Column(String)
    observed_counter = Column(BigInteger)
    observed_first = Column(DateTime)
    observed_last = Column(DateTime)
    note = Column(String)

    def __init__(self, args: Dict[str, str]):
        self.adsb_hex = args["adsb_hex"].lower()
        self.observed_counter = args["observed_counter"]
        self.observed_first = args["observed_first"]
        self.observed_last = args["observed_last"]
        self.note = args["note"]

    def __repr__(self):
        if self.id is None:
            self.id = 0

        return f"cooked({self.id}, {self.adsb_hex})"

class Device(Base):
    """device table definition"""

    __tablename__ = "device"

    id = Column(BigInteger, primary_key=True)
    altitude = Column(SmallInteger)
    latitude = Column(Float)
    longitude = Column(Float)
    name = Column(String)
    note = Column(String)
    retired_date = Column(Date)
    start_date = Column(Date)

    def __init__(self, args: Dict[str, str]):
        self.altitude = args["altitude"]
        self.latitude = args["latitude"]
        self.longitude = args["longitude"]
        self.name = args["name"]
        self.note = args["note"]
        self.retired_date = args["retired_date"]
        self.start_date = args["start_date"]

    def __repr__(self):
        if self.id is None:
            self.id = 0

        return f"device({self.id}, {self.name})"

class LoadLog(Base):
    """load_log table definition"""

    __tablename__ = "load_log"

    id = Column(BigInteger, primary_key=True)
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

class Observation(Base):
    """observation table definition"""

    __tablename__ = "observation"

    id = Column(BigInteger, primary_key=True)

    adsb_exchange_id = Column(BigInteger)
    load_log_id = Column(BigInteger)

    adsb_hex = Column(String)
    altitude = Column(Integer)
    bearing = Column(Float)
    flight = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    obs_time = Column(DateTime)
    range = Column(Float)
    speed = Column(Integer)
    track = Column(Integer)

    def __init__(self, args: Dict[str, str]):
        print(args)

        self.adsb_hex = args["adsb_hex"].lower()
        self.adsb_exchange_id = args["adsb_exchange_id"]
        self.altitude = args["altitude"]
        self.bearing = args["bearing"]
        self.flight = args["flight"]
        self.latitude = args["latitude"]
        self.load_log_id = args["load_log_id"]
        self.longitude = args["longitude"]
        self.obs_time = args["obs_time"]
        self.range = args["range"]
        self.speed = args["speed"]
        self.track = args["track"]

    def __repr__(self):
        if self.id is None:
            self.id = 0

        return f"observation({self.id}, {self.adsb_hex}, {self.flight})"
