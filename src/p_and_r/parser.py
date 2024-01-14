"""mellow hyena processing"""

import json
import os
import sys

from typing import Dict, List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import yaml
from yaml.loader import SafeLoader

from postgres import PostGres

from hyena import Hyena


class Parser:
    """mellow hynena parser"""

    db_conn = None

    def __init__(self, db_conn: str):
        self.db_conn = db_conn

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

    def file_processor(self, file_name: str, postgres: str) -> int:
        """dispatch to approprate file parser/loader"""

        status = 0

        load_log = postgres.load_log_select(file_name)
        if load_log is not None:
            print(f"skipping duplicate file:{file_name}")
            return status

        buffer = self.file_reader(file_name)
        for element in buffer:
            json_dict = json.loads(element)
            json_dict["file_name"] = file_name

            json_dict["file_type"] = self.file_classifier(json_dict)
            print(f"file_name:{file_name} file_type:{json_dict['file_type']}")

            device = postgres.device_select(json_dict['device'])

            if json_dict["file_type"] == "hyena_1":
                hyena = Hyena(device, postgres)
                status = hyena.hyena_v1_loader(json_dict)
            else:
                status = -1

        print(f"status:{status}")
        return status

    def execute(self, import_dir: str, success_dir: str, failure_dir: str):
        """drive processing pass"""

        db_engine = create_engine(self.db_conn, echo=False)
        postgres = PostGres(sessionmaker(bind=db_engine, expire_on_commit=False))

        success_dir = None
        failure_dir = None

        os.chdir(import_dir)
        targets = os.listdir(".")
        print(f"{len(targets)} files noted")

        success_counter = 0
        failure_counter = 0

        for target in targets:
            if os.path.isfile(target) is False:
                continue

            status = -1
            status = self.file_processor(target, postgres)

            if status == 0:
                success_counter += 1
                # self.file_success(target, success_dir)
            else:
                failure_counter += 1
                # self.file_failure(target, failure_dir)

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

    parser = Parser(configuration["dbConn"])
    parser.execute(
        configuration["importDir"],
        configuration["successDir"],
        configuration["failureDir"],
    )

print("parser stop")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
