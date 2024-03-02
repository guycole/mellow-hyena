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

from sqlalchemy.orm import DeclarativeBase

mapper_registry = registry()


class Base(DeclarativeBase):
    pass


class AdsbExchange(Base):
    """adsb_exchange table definition"""

    __tablename__ = "hyena_adsbexchange"
    #__tablename__ = "adsb_exchange"

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

    def __repr__(self):
        return f"adsb_exchange({self.adsb_hex}, {self.registration}, {self.model})"


class AdsbRanking(Base):
    """adsb_ranking table definition"""

    __tablename__ = "adsb_ranking"

    id = Column(Integer, primary_key=True)
    adsb_hex = Column(String)
    model = Column(String)
    population = Column(Integer)
    rank = Column(SmallInteger)
    registration = Column(String)
    score_date = Column(Date)

    def __init__(self, args: Dict[str, str]):
        self.adsb_hex = args["adsb_hex"]
        self.model = args["model"]
        self.population = args["population"]
        self.rank = args["rank"]
        self.registration = args["registration"]
        self.score_date = args["score_date"]

    def __repr__(self):
        return f"adsb_ranking({self.score_date} {self.rank} {self.adsb_hex} {self.registration} {self.model})"


class BoxScore(Base):
    """box_score table definition"""

    __tablename__ = "box_score"

    id = Column(Integer, primary_key=True)
    adsb_hex_total = Column(Integer)
    adsb_hex_new = Column(Integer)
    device = Column(String)
    file_population = Column(SmallInteger)
    refresh_flag = Column(Boolean)
    score_date = Column(Date)

    def __init__(self, args: Dict[str, str]):
        self.adsb_hex_total = args["adsb_hex_total"]
        self.adsb_hex_new = args["adsb_hex_new"]
        self.device = args["device"]
        self.file_population = args["file_population"]
        self.refresh_flag = args["refresh_flag"]
        self.score_date = args["score_date"]

    def __repr__(self):
        return f"box_score({self.score_date})"


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
        self.adsb_hex = args["adsb_hex"]
        self.observed_counter = args["observed_counter"]
        self.observed_first = args["observed_first"]
        self.observed_last = args["observed_last"]
        self.note = args["note"]

    def __repr__(self):
        return f"cooked({self.adsb_hex})"


class Device(Base):
    """device table definition"""

    __tablename__ = "hyena_device"

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
        return f"device({self.name})"


class LoadLog(Base):
    """load_log table definition"""

    #__tablename__ = "load_log"
    __tablename__ = "hyena_loadlog"

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
        return f"load_log({self.file_name}, {self.file_type})"


class Observation(Base):
    """observation table definition"""

    __tablename__ = "hyena_observation"
    #__tablename__ = "observation"

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
        self.adsb_hex = args["adsb_hex"]
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
