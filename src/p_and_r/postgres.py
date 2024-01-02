"""mellow heeler postgresql support"""

import datetime
import time

from typing import List, Dict

# import pytz

import sqlalchemy
from sqlalchemy import and_
from sqlalchemy import select

from sql_table import LoadLog

class PostGres:
    """mellow heeler postgresql support"""

    db_engine = None
    Session = None

    def __init__(self, session: str):
        pass

#    def __init__(self, session: sqlalchemy.orm.session.sessionmaker):
#        self.Session = session

    def load_log_insert(self, file_name: str, file_type: str) -> LoadLog:
        """load_log insert row"""

        candidate = LoadLog(file_name, file_type)

        session = self.Session()
        session.add(candidate)
        session.commit()
        session.close()

        return candidate

    def load_log_select(self, file_name: str) -> LoadLog:
        """load_log select row"""

        statement = select(LoadLog).filter_by(file_name=file_name)

        with self.Session() as session:
            rows = session.scalars(statement).all()
            for row in rows:
                return row

        return None

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
