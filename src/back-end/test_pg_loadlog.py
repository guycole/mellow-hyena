#
# Title: test_pg_loadlog.py
# Description: exercise load_log table ORM
# Development Environment: OS X 12.6.9/Python 3.11.5
# Author: G.S. Cole (guycole at gmail dot com)
#
import uuid

from datetime import datetime, timezone

from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import yaml
from yaml.loader import SafeLoader

from personality import Personality

from postgres import PostGres


class TestLoadLogTable(TestCase):
    def test_table(self):
        """test load_log"""

        with open("config.test", "r", encoding="utf-8") as stream:
            configuration = yaml.load(stream, Loader=SafeLoader)

        personality = Personality(configuration["djangoFlag"],)

        db_engine = create_engine(configuration["dbConn"], echo=False)
        postgres = PostGres(sessionmaker(bind=db_engine, expire_on_commit=False),)

        # select missing row
        result = postgres.load_log_select("bogus")
        assert result is None

        loadlog_args = {}
        loadlog_args["device"] = "rpi4c-adsb-anderson1"
        loadlog_args["file_name"] = str(uuid.uuid4())
        loadlog_args["file_type"] = "fileType"
        loadlog_args["obs_time"] = datetime.now(timezone.utc)
        loadlog_args["population"] = 1234

        # insert fresh row
        result = postgres.load_log_insert(loadlog_args)
        assert result.device == loadlog_args["device"]
        assert result.file_name == loadlog_args["file_name"]
        assert result.file_type == loadlog_args["file_type"]
        assert result.obs_time == loadlog_args["obs_time"]
        assert result.population == loadlog_args["population"]

        # select existing row
        result = postgres.load_log_select(loadlog_args["file_name"])
        assert result.device == loadlog_args["device"]
        assert result.file_name == loadlog_args["file_name"]
        assert result.file_type == loadlog_args["file_type"]
        assert result.obs_time == loadlog_args["obs_time"]
        assert result.population == loadlog_args["population"]

        # select or insert existing row
        result = postgres.load_log_select_or_insert(loadlog_args)
        assert result.device == loadlog_args["device"]
        assert result.file_name == loadlog_args["file_name"]
        assert result.file_type == loadlog_args["file_type"]
        assert result.obs_time == loadlog_args["obs_time"]
        assert result.population == loadlog_args["population"]

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
