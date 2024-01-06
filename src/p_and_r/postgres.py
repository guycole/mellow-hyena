"""mellow heeler postgresql support"""

import datetime
import time

from typing import List, Dict

# import pytz

import sqlalchemy
from sqlalchemy import and_
from sqlalchemy import select

from sql_table import Aircraft, LoadLog, Observation

class PostGres:
    """mellow heeler postgresql support"""

    Session = None

    def __init__(self, session: str):
        pass

    def __init__(self, session: sqlalchemy.orm.session.sessionmaker):
        self.Session = session

    def aircraft_insert(self, aircraft: Aircraft) -> Aircraft:
        """aircraft insert row"""

        aircraft.hex = aircraft.hex.lower()

        if len(aircraft.callsign) < 1:
            aircraft.callsign = "unknown"

        session = self.Session()
        session.add(aircraft)
        session.commit()
        session.close()

        return aircraft
    
    def aircraft_select(self, hex: str, flight:str) -> Aircraft:
        """aircraft select row"""

        statement = (select(Aircraft).filter_by(hex=hex.lower()).order_by(Aircraft.version))

        with self.Session() as session:
            rows = session.scalars(statement).all()
            for row in rows:
                if row.callsign == flight:
                    return row

        return None
    
    def aircraft_select_or_insert(self, hex: str, flight: str) -> Aircraft:
        """discover if aircraft exists or if not, max version for insert"""

        hex = hex.lower()

        if len(flight) < 1:
            flight = "unknown"

        statement = (select(Aircraft).filter_by(hex=hex).order_by(Aircraft.version))

        row = None
        with self.Session() as session:
            rows = session.scalars(statement).all()
            for row in rows:
                if row.callsign == flight:
                    return row

        if row is None:
            aircraft = Aircraft("unknown", flight, hex, version=1)
        else:
            aircraft = Aircraft("unknown", flight, hex, row.version + 1)

        return self.aircraft_insert(aircraft)
       
    def load_log_insert(self, args: Dict[str, str]) -> LoadLog:
        """load_log insert row"""

        load_log = LoadLog(args)

        session = self.Session()
        session.add(load_log)
        session.commit()
        session.close()

        return load_log

    def load_log_select(self, file_name: str) -> LoadLog:
        """load_log select row"""

        statement = select(LoadLog).filter_by(file_name=file_name)

        with self.Session() as session:
            rows = session.scalars(statement).all()
            for row in rows:
                return row

        return None

    def observation_insert(self, args: Dict[str, str]) -> Observation:
        """observation insert row"""

        observation = Observation(args)
      
        session = self.Session()
        session.add(observation)
        session.commit()
        session.close()

        return observation

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
