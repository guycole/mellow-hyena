#
# Title: test_pg_adsb_ex.py
# Description: exercise box score table ORM
# Development Environment: OS X 12.6.9/Python 3.11.5
# Author: G.S. Cole (guycole at gmail dot com)
#
import datetime
import uuid

from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import yaml
from yaml.loader import SafeLoader

from personality import Personality

from postgres import PostGres

class TestBoxScoreTable(TestCase):
    def test_table(self):
        """test box score"""

        with open("config.test", "r", encoding="utf-8") as stream:
            configuration = yaml.load(stream, Loader=SafeLoader)

        personality = Personality(configuration["djangoFlag"])
        db_engine = create_engine(configuration["dbConn"], echo=False)
        postgres = PostGres(sessionmaker(bind=db_engine, expire_on_commit=False),)

        results = postgres.box_score_select_daily(datetime.date.today())
        assert len(results) == 0
        


# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
