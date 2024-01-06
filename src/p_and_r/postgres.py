"""mellow heeler postgresql support"""

import datetime
import time

from typing import List, Dict

# import pytz

import sqlalchemy
from sqlalchemy import and_
from sqlalchemy import select

from sql_table import LoadLog, Observation

class PostGres:
    """mellow heeler postgresql support"""

    Session = None

    def __init__(self, session: str):
        pass

    def __init__(self, session: sqlalchemy.orm.session.sessionmaker):
        self.Session = session

    def load_log_insert(self, load_log: LoadLog) -> LoadLog:
        """load_log insert row"""

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

    def observation_insert(self, observation: Observation) -> Observation:
        """observation insert row"""

        session = self.Session()
        session.add(observation)
        session.commit()
        session.close()

        return observation

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
