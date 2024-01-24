"""mellow hyena loader for mellow wombat"""

import json
import os
import sys

from sqlite import SqlLite

from typing import Dict, List

import sqlite3
from sqlite3 import Error

import yaml
from yaml.loader import SafeLoader



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

    def file_processor(self, file_name: str, sqlite:SqlLite) -> int:
        """dispatch to approprate file parser/loader"""

        status = 0
        print(sqlite)
        print(type(sqlite))

        sqlite.load_log_select(file_name)

        args = {}
        args["file_name"] = file_name   
        args["load_time"] = "2021-01-01 00:00:00"
        args["obs_time"] = "2021-01-01 00:00:00"
        args["population"] = 1
#        sqlite.load_log_insert(args)

#        print(f"load_log:{load_log}")

#        if load_log is not None:
#            print(f"skipping duplicate file:{file_name}")
#            return status

#        buffer = self.file_reader(file_name)
#        for element in buffer:
#            json_dict = json.loads(element)
#            json_dict["file_name"] = file_name

#            json_dict["file_type"] = self.file_classifier(json_dict)
#            print(f"file_name:{file_name} file_type:{json_dict['file_type']}")

#            device = postgres.device_select(json_dict['device'])

#            if json_dict["file_type"] == "hyena_1":
#                hyena = Hyena(device, postgres)
#                status = hyena.hyena_v1_loader(json_dict)
#            else:
#                status = -1

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

            print(type(sqlite))
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
