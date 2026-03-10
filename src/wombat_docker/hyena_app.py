#
# Title: hyena_app.py
# Description: driver for hyenea application
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
import logging
import os

from postgres import PostGres
from validator import Validator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("hyena")


class HyenaApp:

    def __init__(self, score_limit, stunt_box: str):
        self.score_limit = score_limit
        self.stunt_box = stunt_box

#        self.db_conn = "postgresql+psycopg2://wombat_client:batabat@host.docker.internal:5432/wombat"
        self.db_conn = "postgresql+psycopg2://wombat_client:batabat@172.17.0.1:5432/wombat"
        db_engine = create_engine(self.db_conn, echo=False)
        self.postgres = PostGres(sessionmaker(bind=db_engine, expire_on_commit=False))

    def execute(self) -> None:
        logger.info(f"hyena execute:{self.stunt_box}")

        validator = Validator(self.postgres)
        validator.validate()

if __name__ == "__main__":
    score_limit = os.environ.get("limit", -1)
    stunt_box = os.environ.get("stuntbox", "validate")

    app = HyenaApp(int(score_limit), stunt_box)
    app.execute()

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
