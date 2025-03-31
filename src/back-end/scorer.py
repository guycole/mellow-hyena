#
# Title: scorer.py
# Description: calculate daily box score
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
import datetime
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import yaml
from yaml.loader import SafeLoader

from converter import Converter
import postgres

class Scorer:
    # key = date_platform_project_site
    scores = {}

    def __init__(self, configuration: dict[str, str]):
        self.db_conn = configuration["dbConn"]
        self.sql_echo = configuration["sqlEchoEnable"]

        connect_dict = {"options": "-csearch_path={}".format("hyena_v1")}
        db_engine = create_engine(
            self.db_conn, echo=self.sql_echo, connect_args=connect_dict
        )

        self.postgres = postgres.PostGres(
            sessionmaker(bind=db_engine, expire_on_commit=False)
        )

    def fresh_score(self, platform: str, project: str, score_date: datetime.date, site_id: int) -> dict[str, any]:
        return {
            "adsb_hex_new": 0,
            "adsb_hex_total": 0,
            "file_quantity": 1,
            "platform": platform,
            "project": project,
            "score_date": score_date,
            "site_id": site_id
        }

    def pass1(self, current_day: datetime.date) -> None:
        load_log_rows = self.postgres.load_log_select_by_obs_date(current_day)
        print(f"load log quantity {len(load_log_rows)} for {current_day}")

        # discover platform and sites for today
        for row in load_log_rows:
            scores_key = f"{row.obs_date}-{row.platform}-{row.project}-{row.site_id}"
            print(scores_key)

            if scores_key in self.scores:
                print(f"existing key {scores_key}")
                self.scores[scores_key]['file_quantity'] += 1
            else:
                print(f"fresh key {scores_key}")
                self.scores[scores_key] = self.fresh_score(row.platform, row.project, row.obs_date, row.site_id)

            obs_list = self.postgres.observation_select_by_load_log_id(row.id)
            
            if len(obs_list) != row.obs_quantity:
                print(f"mistmatch {row.id} {row.obs_quantity} {len(obs_list)}")

            self.scores[scores_key]['adsb_hex_total'] += len(obs_list)

            for obs in obs_list:
                cooked = self.postgres.cooked_select_by_adsb_hex(obs.adsb_hex)
                if cooked.obs_first.date() == current_day:
                    self.scores[scores_key]['adsb_hex_new'] += 1

    def pass2(self) -> None:
        for key, value in self.scores.items():
            self.postgres.box_score_update_or_insert(value)
    
    def execute(self) -> None:
        current_day = datetime.date(2023, 12, 25)
        limit_day = datetime.date(2024, 1, 1)
        limit_day = datetime.datetime.now().date()

        while current_day <= limit_day:
            self.pass1(current_day)
            current_day = current_day + datetime.timedelta(days=1)

        self.pass2()

print("start scorer")

#
# argv[1] = configuration filename
#
if __name__ == "__main__":
    if len(sys.argv) > 1:
        config_name = sys.argv[1]
    else:
        config_name = "config.yaml"

    with open(config_name, "r", encoding="utf-8") as in_file:
        try:
            configuration = yaml.load(in_file, Loader=SafeLoader)
        except yaml.YAMLError as error:
            print(error)

    scorer = Scorer(configuration)
    scorer.execute()

print("stop scorer")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
