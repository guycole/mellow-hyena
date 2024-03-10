#
# Title: test_pg_loadlog.py
# Description: exercise load_log table ORM
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


class TestLoadLogTable(TestCase):
    def test_select(self):
        """test load_log selection"""

        with open("config.test", "r", encoding="utf-8") as stream:
            configuration = yaml.load(stream, Loader=SafeLoader)

        personality = Personality(configuration["djangoFlag"],)

        db_engine = create_engine(configuration["dbConn"], echo=False)
        postgres = PostGres(sessionmaker(bind=db_engine, expire_on_commit=False),)

        result = postgres.load_log_select("bogus")
        assert result is None

#                select * from load_log;
# id | device | file_name | file_type | load_time | obs_time | population 

#        result = postgres.device_select("rpi4c-adsb-anderson1")
#        assert result.altitude == 500
#        assert result.latitude == 40.416668
#        assert result.longitude == -122.24167
#        assert result.name == "rpi4c-adsb-anderson1"
#        assert result.note == "no note"
#        print(type(result.retired_date))
#        assert result.retired_date == datetime.date(2023, 12, 28)
#        assert result.start_date == datetime.date(2023, 12, 28)


# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
