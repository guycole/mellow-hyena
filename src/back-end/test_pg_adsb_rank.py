#
# Title: test_pg_adsb_rank.py
# Description: exercise adsb ranking table ORM
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

class TestAdsbRankTable(TestCase):
    def test_table(self):
        """test adsb rank"""

        with open("config.test", "r", encoding="utf-8") as stream:
            configuration = yaml.load(stream, Loader=SafeLoader)

        personality = Personality(configuration["djangoFlag"])
        db_engine = create_engine(configuration["dbConn"], echo=False)
        postgres = PostGres(sessionmaker(bind=db_engine, expire_on_commit=False),)

        postgres.adsb_ranking_delete(datetime.date.today())

        args = {}
        args["adsb_hex"] = str(uuid.uuid4())[:6]
        args["model"] = "model"
        args["population"] = 1234
        args["rank"] = 1
        args["registration"] = "reg"
        args["score_date"] = datetime.date.today()

        # insert fresh row
        postgres.adsb_ranking_insert(args)


# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
