#
# Title: test_pg_observation.py
# Description: exercise observation table ORM
# Development Environment: OS X 12.6.9/Python 3.11.5
# Author: G.S. Cole (guycole at gmail dot com)
#
from datetime import datetime, timezone
import uuid

from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import yaml
from yaml.loader import SafeLoader

from personality import Personality

from postgres import PostGres

class TestObservationTable(TestCase):
    def test_table(self):
        """test device"""

        with open("config.test", "r", encoding="utf-8") as stream:
            configuration = yaml.load(stream, Loader=SafeLoader)

        personality = Personality(configuration["djangoFlag"])
        db_engine = create_engine(configuration["dbConn"], echo=False)
        postgres = PostGres(sessionmaker(bind=db_engine, expire_on_commit=False),)


        args = {}
        args["adsb_hex"] = str(uuid.uuid4())[:6]
        args["adsb_exchange_id"] = 3
        args["altitude"] = 500
        args["bearing"] = 180
        args["flight"] = "flight"
        args["latitude"] = 40.416668
        args["load_log_id"] = 8
        args["longitude"] = -122.24167
        args["obs_time"] = datetime.now(timezone.utc)
        args["range"] = 123
        args["speed"] = 321
        args["track"] = 270

        # insert fresh row
        # TODO: need valid adsb_exchange_id and load_log_id
        result = postgres.observation_insert(args)

        # test select or insert
        result = postgres.observation_select_or_insert(args)
        assert result.adsb_hex == args["adsb_hex"]
        assert result.adsb_exchange_id == args["adsb_exchange_id"]
        assert result.altitude == args["altitude"]
        assert result.bearing == args["bearing"]
        assert result.flight == args["flight"]
        assert result.latitude == args["latitude"]
        assert result.load_log_id == args["load_log_id"]
        assert result.longitude == args["longitude"]
        assert result.obs_time == args["obs_time"]
        assert result.range == args["range"]
        assert result.speed == args["speed"]
        assert result.track == args["track"]


# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
