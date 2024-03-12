#
# Title: test_cooked.py
# Description: exercise cooked table ORM
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

class TestCookedTable(TestCase):
    def test_table(self):
        """test cooked"""

        with open("config.test", "r", encoding="utf-8") as stream:
            configuration = yaml.load(stream, Loader=SafeLoader)

        personality = Personality(configuration["djangoFlag"])
        db_engine = create_engine(configuration["dbConn"], echo=False)
        postgres = PostGres(sessionmaker(bind=db_engine, expire_on_commit=False),)

        # select missing row
        result = postgres.cooked_select("bogus")
        assert result is None

        cooked_args = {}
        cooked_args["adsb_hex"] = str(uuid.uuid4())[:6]
        cooked_args["observed_counter"] = 1234
        cooked_args["observed_first"] = datetime.now(timezone.utc)
        cooked_args["observed_last"] = datetime.now(timezone.utc)
        cooked_args["note"] = "note"

        # insert fresh row
        result = postgres.cooked_insert(cooked_args)
        assert result.adsb_hex == cooked_args["adsb_hex"]
        assert result.observed_counter == cooked_args["observed_counter"]
        assert result.observed_first == cooked_args["observed_first"]
        assert result.observed_last == cooked_args["observed_last"]
        assert result.note == cooked_args["note"]

        # select existing row
        result = postgres.cooked_select(cooked_args["adsb_hex"])
        assert result.observed_counter == cooked_args["observed_counter"]
        assert result.observed_first == cooked_args["observed_first"]
        assert result.observed_last == cooked_args["observed_last"]
        assert result.note == cooked_args["note"]

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
