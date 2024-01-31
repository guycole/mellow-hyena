"""mellow hyena adsb collection"""

import json
import datetime
import os
import sys
import typing
import uuid

from datetime import timezone

from typing import Dict

import yaml
from yaml.loader import SafeLoader

from adsb_exchange import AdsbExchange


class Collector:
    """mellow hynena adsb collector"""

    adsb_exchange = None
    device = None
    dump978_filename = None
    export_dir = None

    def __init__(
        self, device: str, dump978_filename: str, export_dir: str, rapid_api_key: str
    ):
        self.adsb_exchange = AdsbExchange(rapid_api_key)
        self.device = device
        self.dump978_filename = dump978_filename
        self.export_dir = export_dir

    def get_filename(self) -> str:
        """return fully qualified filename"""

        return f"{self.export_dir}/{str(uuid.uuid4())}"

    def get_timestamp(self) -> int:
        """return epoch timestamp in UTC"""

        dt = datetime.datetime.now(timezone.utc)
        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()
        return int(utc_timestamp)

    def file_reader(self) -> Dict[str, str]:
        """read a dump978 file into a dictionary"""

        buffer = {}

        with open(self.dump978_filename, "r", encoding="utf-8") as infile:
            try:
                buffer = json.load(infile)
                if len(buffer) < 1:
                    print(f"empty file noted: {self.dump978_filename}")
            except:
                print(f"file read error: {self.dump978_filename}")

        return buffer

    def converter(self, payload: typing.List[typing.Dict]) -> typing.List[typing.Dict]:
        """process payload from dump978"""

        results = []
        current = {}

        for element in payload:
            current.clear()

            current["adsb_hex"] = element["hex"].lower()
            current["flight"] = element["flight"].strip()
            if len(current["flight"]) < 1:
                current["flight"] = "unknown"

            current["altitude"] = element["altitude"]
            current["lat"] = element["lat"]
            current["lon"] = element["lon"]
            current["speed"] = element["speed"]
            current["track"] = element["track"]

            self.adsb_exchange.add_to_queue(current["adsb_hex"])

            results.append(current.copy())

        return results

    def perform_collection(self):
        """read dump978 file"""

        if os.path.isfile(self.dump978_filename) is False:
            print(f"dump978 file not found:{self.dump978_filename}")
            return

        buffer = self.file_reader()

        results = {}
        results["device"] = self.device
        results["project"] = "hyena"
        results["timestamp"] = buffer["now"]
        results["version"] = 1

        timestamp = self.get_timestamp()
        if timestamp - results["timestamp"] > 180:
            print("stale dump978 file")
            return

        results["observation"] = self.converter(buffer["aircraft"])
        if len(results["observation"]) < 1:
            print("no observations")
            return

        self.adsb_exchange.get_aircraft()
        results["adsbex"] = self.adsb_exchange.convert_out_dict()

        out_file_name = self.get_filename()
        with open(out_file_name, "w", encoding="utf-8") as outfile:
            outfile.write(f"{json.dumps(results)}\n")

    def execute(self):
        """drive the collection pass"""

        self.perform_collection()


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
        configuration["device"],
        configuration["dump978out"],
        configuration["exportDir"],
        configuration["rapidApiKey"],
    )
    collector.execute()

print("collection stop")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
