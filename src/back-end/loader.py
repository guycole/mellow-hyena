#
# Title: loader.py
# Description: parse mellow hyena files and load to postgresql
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
import json
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import yaml
from yaml.loader import SafeLoader

from converter import Converter
import postgres

class Loader:
    """mellow hyena file parser and database loader"""

    def __init__(self, configuration: dict[str, str]):
        self.db_conn = configuration["dbConn"]
        self.dry_run = configuration["dryRun"]
        self.archive_dir = configuration["archiveDir"]
        self.failure_dir = configuration["failureDir"]
        self.fresh_dir = configuration["freshDir"]
        self.sql_echo = configuration["sqlEchoEnable"]

        connect_dict = {"options": "-csearch_path={}".format("hyena_v1")}
        db_engine = create_engine(
            self.db_conn, echo=self.sql_echo, connect_args=connect_dict
        )

        self.postgres = postgres.PostGres(
            sessionmaker(bind=db_engine, expire_on_commit=False)
        )

        self.failure_counter = 0
        self.success_counter = 0

    def file_failure(self, file_name: str):
        """problem file, retain for review"""

        self.failure_counter += 1

        if self.dry_run is True:
            print(f"skip failure move for {file_name}")
        else:
            print(f"failure move for {file_name}")
            os.rename(file_name, self.failure_dir + "/" + file_name)

    def file_success(self, file_name: str):
        """file was successfully processed"""

        self.success_counter += 1

        if self.dry_run is True:
            print(f"skip archive move for {file_name}")
        else:
            os.rename(file_name, self.archive_dir + "/" + file_name)

    def json_reader(self, file_name: str) -> dict[str, any]:
        results = {}

        try:
            with open(file_name, "r") as in_file:
                results = json.load(in_file)
                results['file_name'] = file_name
        except Exception as error:
            print(error)

        return results

    def payload_insert(self, args: dict[str, any]) -> bool:
        converter = Converter()
        payload = converter.converter(args)
        print(payload['file_name'])

        site = self.postgres.site_select_by_name(payload['site'])
        if site is None:
            print(f"skipping unknown site {payload['site']} {payload['file_name']}")
            return False

        obs_length = len(payload['observation'])
        if obs_length < 1:
            print(f"skipping file without observations {payload['file_name']}")
            return False
        
        load_log = self.postgres.load_log_insert(payload, obs_length, site.id)
        if load_log.id is None:
            print(f"skipping file without load log id {payload['file_name']}")
            return False

        adsbex_list = converter.adsb_processor(payload)
        for adsb in adsbex_list:
            adsb_obj = self.postgres.adsb_exchange_select_or_insert(adsb)
            if adsb_obj.id is None:
                print(f"skipping bad adsb {adsb_obj} {payload['file_name']}")
                return False
            else:
                adsb['pk_id'] = adsb_obj.id

        obs_list = converter.obs_processor(payload)
        for obs in obs_list:
            temp = self.postgres.observation_insert(obs, load_log.id)
            if temp.id is None:
                print(f"skipping bad obs {obs} {payload['file_name']}")
                return False
            
            temp = self.postgres.cooked_update_or_insert(obs)
            if temp.id is None:
                print(f"skipping bad cooked {obs} {payload['file_name']}")
                return False

#        print(candidates)

        return True

    def execute(self) -> None:
        print(f"fresh dir:{self.fresh_dir}")
        os.chdir(self.fresh_dir)
        targets = os.listdir(".")
        print(f"{len(targets)} files noted")

        for target in targets:
            if os.path.isfile(target) is False:
                continue

            # test for duplicate file
            load_log = self.postgres.load_log_select_by_file_name(target)
            if load_log is not None:
                print(f"skip duplicate file:{target}")
                self.file_failure(target)
                continue

            raw_payload = self.json_reader(target)
            if len(raw_payload) < 1:
                print(f"skip empty parse:{target}")
                self.file_failure(target)
                continue

            flag = self.payload_insert(raw_payload)
            if flag is True:
                self.file_success(target)
            else:
                self.file_failure(target)

print("start loader")

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

    loader = Loader(configuration)
    loader.execute()

print("stop loader")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
