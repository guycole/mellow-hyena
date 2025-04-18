#
# Title: test_pg_adsb_ex.py
# Description: exercise adsb exchange table ORM
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

class TestAdsbExchangeTable(TestCase):
    def test_table(self):
        """test adsb exchange"""

        with open("config.test", "r", encoding="utf-8") as stream:
            configuration = yaml.load(stream, Loader=SafeLoader)

        personality = Personality(configuration["djangoFlag"])
        db_engine = create_engine(configuration["dbConn"], echo=False)
        postgres = PostGres(sessionmaker(bind=db_engine, expire_on_commit=False),)

        # select missing row
        result = postgres.adsb_exchange_select("bogus")
        assert result is None

        adsbex_args = {}
        adsbex_args["adsb_hex"] = str(uuid.uuid4())[:6]
        adsbex_args["category"] = "aaa"
        adsbex_args["emergency"] = "bbb"
        adsbex_args["flight"] = "flight"
        adsbex_args["model"] = "model"
        adsbex_args["registration"] = "ccc"
        adsbex_args["ladd_flag"] = False
        adsbex_args["military_flag"] = False
        adsbex_args["pia_flag"] = False
        adsbex_args["wierdo_flag"] = False

        # insert fresh row
        result = postgres.adsb_exchange_insert(adsbex_args)
        assert result.adsb_hex == adsbex_args["adsb_hex"]
        assert result.category == adsbex_args["category"]
        assert result.emergency == adsbex_args["emergency"]
        assert result.flight == adsbex_args["flight"]
        assert result.model == adsbex_args["model"]
        assert result.registration == adsbex_args["registration"]
        assert result.ladd_flag == adsbex_args["ladd_flag"]
        assert result.military_flag == adsbex_args["military_flag"]
        assert result.pia_flag == adsbex_args["pia_flag"]
        assert result.wierdo_flag == adsbex_args["wierdo_flag"]

        # select existing row
        result = postgres.adsb_exchange_select(adsbex_args["adsb_hex"])
        assert result.adsb_hex == adsbex_args["adsb_hex"]
        assert result.category == adsbex_args["category"]
        assert result.emergency == adsbex_args["emergency"]
        assert result.flight == adsbex_args["flight"]
        assert result.model == adsbex_args["model"]
        assert result.registration == adsbex_args["registration"]
        assert result.ladd_flag == adsbex_args["ladd_flag"]
        assert result.military_flag == adsbex_args["military_flag"]
        assert result.pia_flag == adsbex_args["pia_flag"]
        assert result.wierdo_flag == adsbex_args["wierdo_flag"]

        # select or insert existing row
        result = postgres.adsb_exchange_select_or_insert(adsbex_args)
        assert result.adsb_hex == adsbex_args["adsb_hex"]
        assert result.category == adsbex_args["category"]
        assert result.emergency == adsbex_args["emergency"]
        assert result.flight == adsbex_args["flight"]
        assert result.model == adsbex_args["model"]
        assert result.registration == adsbex_args["registration"]
        assert result.ladd_flag == adsbex_args["ladd_flag"]
        assert result.military_flag == adsbex_args["military_flag"]
        assert result.pia_flag == adsbex_args["pia_flag"]
        assert result.wierdo_flag == adsbex_args["wierdo_flag"]

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
