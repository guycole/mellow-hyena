#
# Title: test_pg_adsbex.py
# Description: exercise adsb exchange table ORM
# Development Environment: OS X 12.6.9/Python 3.11.5
# Author: G.S. Cole (guycole at gmail dot com)
#
import datetime

from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import yaml
from yaml.loader import SafeLoader

from personality import Personality

from postgres import PostGres

class TestAdsbExchangeTable(TestCase):
    def test_select(self):
        """test adsb exchange selection"""

        with open("config.test", "r", encoding="utf-8") as stream:
            configuration = yaml.load(stream, Loader=SafeLoader)

        personality = Personality(configuration["djangoFlag"])
        db_engine = create_engine(configuration["dbConn"], echo=False)
        postgres = PostGres(sessionmaker(bind=db_engine, expire_on_commit=False),)

        result = postgres.adsb_exchange_select("bogus")
        assert result is None



# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
