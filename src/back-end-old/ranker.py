"""mellow hyena ranker"""

import datetime
import sys

import pytz

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import yaml
from yaml.loader import SafeLoader

from postgres import PostGres

MAX_RANK_LIST = 25


class Ranker:
    """mellow hynena ranker"""

    db_conn = None

    def __init__(self, db_conn: str):
        self.db_conn = db_conn

    def write_rank(
        self,
        adsb_hex: str,
        population: int,
        rank: int,
        score_date: datetime.date,
        postgres: PostGres,
    ):
        """write a adsb rank row"""
        # print(f"{adsb_hex} {population} {rank}. {score_date}")

        args = {}
        args["adsb_hex"] = adsb_hex
        args["population"] = population
        args["rank"] = rank
        args["score_date"] = score_date

        adsb_exchange = postgres.adsb_exchange_select(adsb_hex)
        if adsb_exchange is None:
            args["model"] = "unknown"
            args["registration"] = "unknown"
        else:
            args["model"] = adsb_exchange.model
            args["registration"] = adsb_exchange.registration

        postgres.adsb_ranking_insert(args)

    def daily_ranker(self, score_date: datetime.date, postgres: PostGres):
        """discover who is the most common beacon for a day"""

        postgres.adsb_ranking_delete(score_date)

        start_time = datetime.datetime(
            score_date.year,
            score_date.month,
            score_date.day,
            0,
            0,
            0,
            0,
            pytz.utc,
        )

        stop_time = datetime.datetime(
            score_date.year,
            score_date.month,
            score_date.day,
            23,
            59,
            59,
            999999,
            pytz.utc,
        )

        candidates = postgres.observation_counter(start_time, stop_time)

        tweaked = dict(
            sorted(candidates.items(), key=lambda item: item[1], reverse=True)
        )

        rank = 0
        for key in tweaked:
            rank = 1 + rank
            if rank > MAX_RANK_LIST:
                break

            self.write_rank(key, tweaked[key], rank, score_date, postgres)

    def execute(self):
        """drive processing pass"""

        db_engine = create_engine(self.db_conn, echo=False)
        postgres = PostGres(sessionmaker(bind=db_engine, expire_on_commit=False))

        duplicate_list = []

        targets = postgres.box_score_select_refresh()
        print(f"box_score targets: {len(targets)}")
        for target in targets:
            target.refresh_flag = False
            postgres.box_score_update(target)

            if target.score_date in duplicate_list:
                print(f"skipping date: {target.score_date}")
            else:
                self.daily_ranker(target.score_date, postgres)
                duplicate_list.append(target.score_date)


print("ranker start")

#
# argv[1] = configuration filename
#
if __name__ == "__main__":
    if len(sys.argv) > 1:
        config_file_name = sys.argv[1]
    else:
        config_file_name = "config.yaml"

    with open(config_file_name, "r", encoding="utf-8") as stream:
        try:
            configuration = yaml.load(stream, Loader=SafeLoader)
        except yaml.YAMLError as exc:
            print(exc)

    ranker = Ranker(configuration["dbConn"])
    ranker.execute()

print("ranker stop")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
