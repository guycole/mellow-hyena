#
# Title: reporter.py
# Description: write markdown reports
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
import datetime
import sys

import yaml
from yaml.loader import SafeLoader

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import postgres

from sql_table import LoadLog


class DailyScores:
    daily_scores = {}

    def __init__(self, configuration: dict[str, str]):
        self.report_dir = configuration["reportDir"]
        self.db_conn = configuration["dbConn"]
        self.sql_echo = configuration["sqlEchoEnable"]

        connect_dict = {"options": "-csearch_path={}".format("hyena_v1")}
        db_engine = create_engine(
            self.db_conn, echo=self.sql_echo, connect_args=connect_dict
        )

        self.postgres = postgres.PostGres(
            sessionmaker(bind=db_engine, expire_on_commit=False)
        )

    def converter(self):
        """convert from postgres daily score to markdown"""

        selected = self.postgres.daily_score_select_all()
        if len(selected) < 1:
            print("empty daily score select")
            return

        for row in selected:
            print(row)
            row_year = row.score_date.year
            if row_year not in self.daily_scores:
                self.daily_scores[row_year] = []

            temp = self.daily_scores[row_year]

            candidate = f"|{row.score_date}|{row.project}|{row.platform}|{row.file_quantity}|{row.adsb_hex_total}|{row.adsb_hex_new}|\n"

            temp.append(candidate)

    def execute(self) -> None:
        self.converter()

        time_now = datetime.datetime.now()
        banner2 = f"created at {time_now}\n\n"
        banner3 = (f"|date|project|platform|file total|adsb total|adsb new|\n")
        banner4 =  f"|--|--|--|--|--|--|\n"

        for key, values in self.daily_scores.items():
            file_name = f"{self.report_dir}/{key}.md"
            print(f"creating file: {file_name}")

            banner1 = f"mellow-hyena collection scores for {key}\n\n"

            try:
                with open(file_name, "w", encoding="utf-8") as out_file:
                    out_file.write(banner1)
                    out_file.write(banner3)
                    out_file.write(banner4)

                    for value in values:
                        out_file.write(value)
            except Exception as error:
                print(error)
                return None

class DailyObservations:
    candidates = {}

    def __init__(self, configuration: dict[str, str]):
        self.report_dir = configuration["reportDir"]
        self.db_conn = configuration["dbConn"]
        self.sql_echo = configuration["sqlEchoEnable"]

        connect_dict = {"options": "-csearch_path={}".format("hyena_v1")}
        db_engine = create_engine(
            self.db_conn, echo=self.sql_echo, connect_args=connect_dict
        )

        self.postgres = postgres.PostGres(
            sessionmaker(bind=db_engine, expire_on_commit=False)
        )

    def pass1(self, row: LoadLog) -> None:
        key = f"{row.obs_date}-{row.site_id}-{row.platform}-{row.project}"

        site = self.postgres.site_select_by_id(row.site_id)

        if key not in self.candidates:
            self.candidates[key] = {
                "adsb": {}, 
                "load_log_id": row.id,
                "platform": row.platform,
                "project": row.project,
                "obs_date": row.obs_date,
                "site_id": site.id,
                "site_name": site.name,
            }

    def pass2(self, key: str) -> None:
        print(key)

        candidate = self.candidates[key]
        adsb = candidate['adsb']

        obs_list = self.postgres.observation_select_by_load_log_id(candidate['load_log_id'])
        for obs in obs_list:
            if obs.adsb_hex not in adsb:
                adsbex = self.postgres.adsb_exchange_select_by_id(obs.adsb_exchange_id)
                mil_flag = "T" if adsbex.military_flag else "F"
                wierdo_flag = "T" if adsbex.wierdo_flag else "F"
                                
                adsb[obs.adsb_hex] = {
                    "adsb_exchange_id": obs.adsb_exchange_id,
                    "adsb_hex": obs.adsb_hex,
                    "emergency": adsbex.emergency,
                    "flight": obs.flight,
                    "model": adsbex.model,
                    "registration": adsbex.registration,
                    "military": mil_flag,
                    "weirdo": wierdo_flag,
                }

    def pass3(self, key: str) -> None:
        candidate = self.candidates[key]
        adsb = candidate['adsb']
        
        file_name = f"{candidate['obs_date']}-{candidate['site_name']}-{candidate['platform']}-{candidate['project']}"
        full_name = f"{self.report_dir}/{file_name}.md"
        print(f"creating file: {file_name}")

        banner1 = f"mellow-hyena daily summary for {file_name}\n\n"
        banner3 = f"|hex|flight|model|reg|emergency|mil|weirdo|\n"
        banner4 = f"|--|--|--|--|--|--|--|\n"

        try:
            with open(full_name, "w", encoding="utf-8") as out_file:
                out_file.write(banner1)
                out_file.write(banner3)
                out_file.write(banner4)

                for key, value in adsb.items():
                    buffer = f"|{value['adsb_hex']}|{value['flight']}|{value['model']}|{value['registration']}|{value['emergency']}|{value['military']}|{value['weirdo']}|\n"
                    out_file.write(buffer)
        except Exception as error:
            print(error)
            return None

    def execute(self) -> None:
        rows = self.postgres.load_log_select_all()

        for row in rows:
            self.pass1(row)

        for key in self.candidates.keys():
            self.pass2(key)

        for key in self.candidates.keys():
            self.pass3(key)

print("start reporter")

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

    reporter = DailyScores(configuration)
#    reporter.execute()

    reporter = DailyObservations(configuration)
    reporter.execute()

print("stop reporter")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
