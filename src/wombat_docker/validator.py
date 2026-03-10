
#
# Title: validator.py
# Description: validate observation and collect basic stats
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
from asyncio.log import logger
import datetime
import json
import os
import requests

from postgres import PostGres

class Validator:

    def __init__(self, postgres: PostGres):
        self.postgres = postgres

        # path is from inside docker container
        self.failure_dir = "/mnt/wombat/hyena/failure/"
        self.fresh_dir = "/mnt/wombat/fresh/hyena"
        self.success_dir = "/mnt/wombat/hyena/success/"

        self.failure = 0
        self.success = 0

        self.api_key = "bogus"

        self.headers = {}
        self.headers["X-RapidAPI-Key"] = self.api_key
        self.headers["X-RapidAPI-Host"] = "adsbexchange-com1.p.rapidapi.com"

    
    def file_failure(self, file_name: str):
        logger.info(f"file failure:{file_name}")

        self.failure += 1
        os.rename(file_name, self.failure_dir + file_name)

    def file_success(self, file_name: str):
#        logger.info(f"file success:{file_name}")

        self.success += 1
        os.rename(file_name, self.success_dir + "/" + file_name)

    def json_reader(self, file_name: str) -> dict[str, any]:
        results = {}

        try:
            with open(file_name, "r") as in_file:
                results = json.load(in_file)
        except Exception as error:
            logger.error(f"json read error for {file_name}: {error}")

        return results

    def json_writer(self, file_name, payload: dict[str, any]) -> None:
        print(f"json_writer:{file_name}")

        try:
            with open(file_name, "w") as out_file:
                json.dump(payload, out_file, indent=4)
        except Exception as error:
            print(error)

    def get_aircraft_from_hex(self, hex_code: str) -> dict[str, any]:
        result = {}

        url = f"https://adsbexchange-com1.p.rapidapi.com/v2/icao/{hex_code}/"
        response = requests.get(url, headers=self.headers, timeout=5.0)
        if response.status_code == 200:
            result = response.json()
        else:
            logger.error(f"adsbex query failed for hex:{hex_code} code:{response.status_code}")

        return result

    def get_adsbex_list(self, json_payload: dict[str, any]) -> list[dict[str, any]]:
        results = []

        if "adsbex" in json_payload:
            return results

        candidates = json_payload['payload']['raw']
        for candidate in candidates:
            response_json = self.get_aircraft_from_hex(candidate['hex'])
            if "ac" in response_json and len(response_json['ac']) > 0:
                results.append(response_json)

        return results

    def file_processor(self, file_name: str) -> None:
        if os.path.isfile(file_name) is False:
            logger.warning(f"skipping non-file:{file_name}")
            return

        json_payload = self.json_reader(file_name)
        if len(json_payload) < 1:
            self.file_failure(file_name)
            return

        adsbex_list = self.get_adsbex_list(json_payload)
        if len(adsbex_list) > 0:
            # print(f"adsbex_list count:{len(adsbex_list)}")
            json_payload['payload']['adsbex'] = adsbex_list
            self.json_writer(file_name, json_payload)
            self.file_success(file_name)

#        if self.converter(file_name):
#            db_args = self.load_log()
#            if len(db_args) > 0:
#                try:
#                    candidate = self.postgres.load_log_select_by_file_name(file_name)
#                    if candidate is not None:
#                        logger.info(f"skippping already processed:{file_name}")
#                    else:
#                        self.postgres.load_log_insert(db_args)
#                    self.file_success(file_name)
#                except Exception as error:
#                    logger.error(f"postgres insert failed for {file_name}: {error}")
#                    self.file_failure(file_name)
#            else:
#                logger.error(f"invalid db_args for file:{file_name}")
#                self.file_failure(file_name)
#        else:
#            self.file_failure(file_name)

    def validate(self) -> None:
        logger.info("validator")
        logger.info(f"fresh dir:{self.fresh_dir}")

        os.chdir(self.fresh_dir)
        targets = os.listdir(".")
        logger.info(f"{len(targets)} files noted")

        for target in targets:
            self.file_processor(target)

        logger.info(f"success:{self.success} failure:{self.failure}")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
