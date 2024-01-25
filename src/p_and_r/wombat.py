"""mellow hyena loader for mellow wombat"""

import json
import os
import sys

from datetime import datetime, timezone

from typing import Dict, List

import sqlite3
from sqlite3 import Error

import yaml
from yaml.loader import SafeLoader

from great_circle import range_and_bearing

from sqlite import SqlLite

class Wombat:
    """mellow hynena parser/loader for mellow wombat"""

    db_filename = None

    def __init__(self, db_filename: str):
        self.db_filename = db_filename

    def file_classifier(self, buffer: Dict[str, str]) -> str:
        """discover file format, i.e. hyena_v1, etc"""

        project = buffer["project"]
        version = buffer["version"]

        return f"{project}_{version}"

    def file_reader(self, file_name: str) -> List[str]:
        """read a mellow hyena file into a buffer"""

        buffer = []

        with open(file_name, "r", encoding="utf-8") as infile:
            try:
                buffer = infile.readlines()
                if len(buffer) < 1:
                    print(f"empty file noted: {file_name}")
            except:
                print(f"file read error: {file_name}")

        return buffer

    def v1_loader(self, args: Dict[str, str], sqlite: SqlLite) -> int:
        status = 0

        device_lat = 38.106389
        device_lon = -122.272778

        if "adsbex" in args:
            for element in args["adsbex"]:
                adsbex_dict = sqlite.adsb_exchange_select(element)
                if len(adsbex_dict) < 1:
                    sqlite.adsb_exchange_insert(element)

        for element in args["observation"]:
            if "hex" in element:
                element["adsb_hex"] = element["hex"]
            else:
                element["adsb_hex"] = element["adsb_hex"].strip()

            if len(element["flight"]) < 1:
                element["flight"] = "unknown"
            else:
                element["flight"] = element["flight"].strip()

            (range2, bearing) = range_and_bearing(
                device_lat, device_lon, element["lat"], element["lon"]
            )
            element["bearing"] = round(bearing, 2)
            element["range"] = round(range2, 2)

            selected_obs = sqlite.observation_select(
                element["adsb_hex"], args["obs_time"]
            )
            if len(selected_obs) > 0:
                print(
                    f"skipping observation adsb_hex:{element['adsb_hex']} obs_time:{args['obs_time']}"
                )
            else:
                sqlite.observation_insert(args["obs_time"], element)

        return status

    def file_processor(self, file_name: str, sqlite: SqlLite) -> int:
        """dispatch to approprate file parser/loader"""

        status = 0

        result = sqlite.load_log_select(file_name)
        if len(result) > 1:
            print(f"skipping duplicate file {file_name}")
            return status

        buffer = self.file_reader(file_name)
        for element in buffer:
            json_dict = json.loads(element)

            json_dict["file_name"] = file_name
            json_dict["file_type"] = self.file_classifier(json_dict)
            json_dict["load_time"] = datetime.now(timezone.utc)
            json_dict["obs_time"] = datetime.fromtimestamp(
                json_dict["timestamp"], timezone.utc
            )
            json_dict["population"] = len(json_dict["observation"])

            print(f"file_name:{file_name} file_type:{json_dict['file_type']}")

            if json_dict["file_type"] == "hyena_1":
                status = self.v1_loader(json_dict, sqlite)
            else:
                status = -1

            sqlite.load_log_insert(json_dict)

        print(f"status:{status}")
        return status

    def execute(self, import_dir: str):
        """drive processing pass"""

        sqlite = None

        try:
            sqlite = SqlLite(sqlite3.connect(self.db_filename))
        except Error as error:
            print(error)
            return

        os.chdir(import_dir)
        targets = os.listdir(".")
        print(f"{len(targets)} files noted")

        success_counter = 0
        failure_counter = 0

        for target in targets:
            if os.path.isfile(target) is False:
                continue

            status = self.file_processor(target, sqlite)

            if status == 0:
                success_counter += 1
            else:
                failure_counter += 1

        print(f"success:{success_counter} failure:{failure_counter}")


print("parser start")

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

    wombat = Wombat(configuration["sqliteDb"])
    wombat.execute(configuration["importDir"])

print("parser stop")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
