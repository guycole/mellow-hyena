"""mellow hyena adsb collection"""

import json
import datetime
import sys
import uuid

from datetime import timezone

import requests

import yaml
from yaml.loader import SafeLoader

class Collector:
    """mellow hynena adsb collector"""

    dump1090url = None
    export_dir = None
    platform = None

    def __init__(self, dump1090url: str, fresh_dir: str, platform: str):
        self.dump1090url = dump1090url
        self.fresh_dir = fresh_dir
        self.platform = platform

    def get_filename(self) -> str:
        """return fully qualified filename"""

        return f"{self.fresh_dir}/{str(uuid.uuid4())}"

    def get_timestamp(self) -> int:
        """return epoch timestamp in UTC"""

        dt = datetime.datetime.now(timezone.utc)
        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()
        return int(utc_timestamp)
    
    def json_writer(self, file_name, payload: dict[str, any]) -> None:
        try:
            with open(file_name, "w") as out_file:
                json.dump(payload, out_file, indent=4)
        except Exception as error:
            print(error)

    def write_payload(self, payload: dict[str, any], timestamp: int):
        result = {
            "platform": self.platform,
            "project": "hyena-adsb",
            "version": 1,
            "geoLoc": {"site": "vallejo", "latitude": 38.1085, "longitude": -122.268},
            "payload": payload,
            "timeStamp": self.get_timestamp()
            # zTimeMs?
        }

        out_file_name = self.get_filename()
        with open(out_file_name, "w", encoding="utf-8") as outfile:
            outfile.write(f"{json.dumps(paydict)}\n")

    def execute(self) -> int:
        timestamp = self.get_timestamp()

        try:
            response = requests.get(self.dump1090url, timeout=5.0)
            if response.status_code == 200:
                payload = json.loads(response.text)
                if len(payload) > 0:
                    self.process_payload(payload)
                    self.write_payload(payload, timestamp)
                else:
                    print("empty response from dump1090")
            else:
                print(f"error reading dump1090:{response.status_code}")
        except:
            print("error processing dump1090")

print("collection start")

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

    collector = Collector(
        configuration["dump1090url"],
        configuration["freshDir"],
        configuration["platform"],
    )
    retstatus = collector.execute()

    # TODO return retstatus    

print("collection stop")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
