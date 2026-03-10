#
# Title: postgres.py
# Description: postgresql support
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
import datetime
import time

from typing import List, Dict


import sqlalchemy
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

class PostGres:
    db_engine = None
    Session = None

    def __init__(self, session: sessionmaker):
        self.Session = session

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***