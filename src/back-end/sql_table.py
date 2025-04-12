#
# Title: sql_table.py
# Description: database table definitions
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
# import sqlalchemy
# from sqlalchemy import and_
# from sqlalchemy import select

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, String

from sqlalchemy.orm import registry
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr

mapper_registry = registry()


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

    def __init__(self, args: dict[str, str]):
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

class Cooked(Base):
    """cooked table definition"""

    __tablename__ = "cooked"

    id = Column(BigInteger, primary_key=True)
    adsb_hex = Column(String)
    obs_quantity = Column(Integer)
    obs_first = Column(DateTime)
    obs_last = Column(DateTime)
    note = Column(String)

    def __init__(self, args: dict[str, any]):
        self.adsb_hex = args["adsb_hex"]
        self.obs_quantity = args["obs_quantity"]
        self.obs_first = args["obs_first"]
        self.obs_last = args["obs_last"]
        self.note = args["note"]

    def __repr__(self):
        return f"cooked({self.adsb_hex})"

class DailyScore(Base):
    """daily_score table definition"""

    __tablename__ = "daily_score"

    id = Column(Integer, primary_key=True)
    adsb_hex_new = Column(Integer)
    adsb_hex_total = Column(Integer)
    file_quantity = Column(Integer)
    platform = Column(String)
    project = Column(String)
    score_date = Column(Date)
    site_id = Column(BigInteger)

    def __init__(self, args: dict[str, any]):
        self.adsb_hex_new = args["adsb_hex_new"]
        self.adsb_hex_total = args["adsb_hex_total"]
        self.file_quantity = args["file_quantity"]
        self.platform = args["platform"]
        self.project = args["project"]
        self.score_date = args["score_date"]        
        self.site_id = args['site_id']

    def __repr__(self):
        return f"daily_score({self.score_date} {self.site_id} {self.platform} {self.project})"

class LoadLog(Base):
    """load_log table definition"""

    __tablename__ = "load_log"

    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_type = Column(String)
    obs_date = Column(Date)
    obs_quantity = Column(Integer)
    obs_time = Column(DateTime)
    platform = Column(String)
    project = Column(String)
    site_id = Column(BigInteger)

    def __init__(self, args: dict[str, any], site_id: int):
        self.file_name = args["file_name"]
        self.file_type = args["file_type"]
        self.obs_date = args["obs_datetime"].date()
        self.obs_quantity = args["obs_quantity"]
        self.obs_time = args["obs_datetime"]
        self.platform = args["platform"]
        self.project = args["project"]
        self.site_id = site_id

    def __repr__(self):
        return f"load_log({self.file_name} {self.obs_time})"

class Observation(Base):

    __tablename__ = "observation"

    id = Column(Integer, primary_key=True)
    adsb_exchange_id = Column(BigInteger)
    adsb_hex = Column(String)
    altitude = Column(Integer)
    bearing = Column(Float)
    flight = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    load_log_id = Column(BigInteger)
    obs_time = Column(DateTime)
    range = Column(Float)
    speed = Column(Integer)
    track = Column(Integer)

    def __init__(self, args: dict[str, str], load_log_id: int):
        self.adsb_exchange_id = args["adsb_exchange_id"]
        self.adsb_hex = args["adsb_hex"]
        self.altitude = args["altitude"]
        self.bearing = args["bearing"]
        self.flight = args["flight"]
        self.latitude = args["lat"]
        self.longitude = args["lon"]
        self.load_log_id = load_log_id
        self.obs_time = args["obs_time"]
        self.range = args["range"]
        self.speed = args["speed"]
        self.track = args["track"]

    def __repr__(self):
        return f"observation({self.adsb_hex} {self.flight})"

class Site(Base):

    __tablename__ = "site"

    id = Column(Integer, primary_key=True)
    altitude = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    name = Column(String)
    note = Column(String)

    def __init__(self, args: dict[str, any]):
        self.altitude = args["altitude"]
        self.latitude = args["latitude"]
        self.longitude = args["longitude"]
        self.name = args["name"]
        self.note = args["name"]

    def __repr__(self):
        return f"site({self.name})"
    
# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
