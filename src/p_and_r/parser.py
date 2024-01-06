"""mellow hyena processing"""

import json
import datetime
import os
import sys
import time
import typing
import uuid

from datetime import timezone

from typing import Dict, List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import requests

import yaml
from yaml.loader import SafeLoader

from postgres import PostGres

from hyena import Hyena

from sql_table import LoadLog

class Parser:
    """mellow hynena parser"""

    db_conn = None
    device = None
    dump1090url = None
    export_dir = None

    def __init__(self, db_conn: str, device: str, dump1090url: str, export_dir: str):
        self.db_conn = db_conn
        self.device = device
        self.dump1090url = dump1090url
        self.export_dir = export_dir
  
    def file_classifier(self, buffer: Dict[str, str]) -> str:
        """discover file format, i.e. hyena_v1, etc"""

        file_type = "unknown"

        project = buffer['project']
        version = buffer['version']

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
        for ndx in range(len(buffer)):
            json_dict = json.loads(buffer[ndx])
            json_dict['file_name'] = file_name

            json_dict['file_type'] = self.file_classifier(json_dict)
            print(f"file_name:{file_name} file_type:{json_dict['file_type']}")

            if json_dict['file_type'] == "hyena_1":
                hyena = Hyena(postgres)
                status = hyena.hyena_v1_loader(json_dict)
            else:
                status = -1
       
        return status

    def execute(self, sample_sleep: int):
        """drive processing pass"""

        import_dir = "/Users/gsc/Documents/github/mellow-hyena/samples"

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
        file_name = sys.argv[1]
    else:
        file_name = "config.yaml"

    with open(file_name, "r", encoding="utf-8") as stream:
        try:
            configuration = yaml.load(stream, Loader=SafeLoader)
        except yaml.YAMLError as exc:
            print(exc)

    parser = Parser(
        configuration["dbConn"],
        configuration["device"],
        configuration["dump1090url"],
        configuration["exportDir"],
    )
    parser.execute(configuration["sampleSleep"])

print("parser stop")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
