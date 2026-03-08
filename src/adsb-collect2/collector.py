#
# Title: collector.py
# Description: read dump1090 json report and save
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
import json
import datetime
import socket
import sys
import time
import uuid
import zoneinfo

from datetime import timezone

import requests

import yaml
from yaml.loader import SafeLoader

class Collector:

    def __init__(self, args:dict[str, any]):
        self.application = args["application"]
        self.crate = args["crate"]
        self.dump1090url = "http://localhost:8080/data.json"
        self.fresh_dir = args["fresh_dir"]
        self.host_name = args["host_name"]
        self.site_name = args["site_name"]
        self.site_lat = args["site_lat"]
        self.site_lng = args["site_lng"]

    def get_filename(self) -> str:
        """return fully qualified filename"""

        return f"{self.fresh_dir}/{str(uuid.uuid4())}"

    def get_timestamp(self) -> int:
        epoch_seconds = int(time.time())
        dt_object_utc = datetime.datetime.fromtimestamp(
            epoch_seconds, tz=zoneinfo.ZoneInfo("UTC")
        )
        iso8601_timestamp = dt_object_utc.isoformat()
        
        return(epoch_seconds, iso8601_timestamp)
    
    def json_writer(self, file_name, payload: dict[str, any]) -> None:
        try:
            with open(file_name, "w") as out_file:
                json.dump(payload, out_file, indent=4)
        except Exception as error:
            print(error)

    def write_payload(self, payload: dict[str, any]):
        timestamp_tuple = self.get_timestamp()

        result = {
            "meta": {
                "application": self.application,
                "crate": self.crate,
                "hostName": self.host_name,
                "schemaVersion": 2,
                "timeStampEpoch": timestamp_tuple[0],
                "timeStampIso8601": timestamp_tuple[1]
            },
            "geoLoc": {
                "site": self.site_name,
                "latitude": self.site_lat,
                "longitude": self.site_lng
            },
            "payload": {
                "raw": payload
            }
        }

        try:
            with open(self.get_filename(), "w") as out_file:
                json.dump(result, out_file, indent=4)
        except Exception as error:
            print(error)

    def execute(self) -> int:
        timestamp = self.get_timestamp()

        fake1 = "[{\"hex\":\"ab77d5\", \"flight\":\"UAL2262 \", \"lat\":40.293365, \"lon\":-122.189575, \"altitude\":33050, \"track\":191, \"speed\":463}]"
        fake2 = json.loads(fake1)
        self.write_payload(fake2)
        
        try:
            response = fake2
#            response = requests.get(self.dump1090url, timeout=5.0)
#            if response.status_code == 200:
#                payload = json.loads(response.text)
#                if len(payload) > 0:
#                    self.process_payload(payload)
#                    self.write_payload(payload, timestamp)
#                else:
#                    print("empty response from dump1090")
#            else:
#                print(f"error reading dump1090:{response.status_code}")
#                return -1
        except Exception as error:
            print(f"dump1090 error: {error}")
            return -1

        return 0

print("collection start")

#
# argv[1] = configuration filename
#
if __name__ == "__main__":
    if len(sys.argv) > 1:
        config_file_name = sys.argv[1]
    else:
        config_file_name = "config.yaml"

    args = {}
    with open(config_file_name, "r", encoding="utf-8") as stream:
        try:
            configuration = yaml.load(stream, Loader=SafeLoader)

            args = {
                "application": configuration["application"],
                "crate": configuration["crate"],
                "fresh_dir": configuration["freshDir"],
                "host_name": socket.gethostname(),
                "site_name": configuration["siteName"],
                "site_lat": configuration["siteLatitude"],
                "site_lng": configuration["siteLongitude"],
            }
        except yaml.YAMLError as exc:
            print(exc)

    collector = Collector(args)
    sys.exit(collector.execute())

print("collection stop")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
