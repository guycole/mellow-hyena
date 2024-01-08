"""mellow hyena collection"""

import json
import datetime
import sys
import time
import typing
import uuid

from datetime import timezone

import requests

import yaml
from yaml.loader import SafeLoader

from adsb_exchange import AdsbExchange


class Collector:
    """mellow hynena collector"""

    adsb_exchange = None
    device = None
    dump1090url = None
    export_dir = None

    def __init__(
        self, device: str, dump1090url: str, export_dir: str, rapid_api_key: str
    ):
        self.adsb_exchange = AdsbExchange(rapid_api_key)
        self.device = device
        self.dump1090url = dump1090url
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

    def process_payload(self, payload: typing.List[typing.Dict]):
        """process payload from dump1090"""

        for element in payload:
            element["hex"] = element["hex"].lower()

            element["flight"] = element["flight"].strip()
            if len(element["flight"]) < 1:
                element["flight"] = "unknown"

            print(f"{element['hex']}:{element['flight']}")
            
            self.adsb_exchange.add_to_queue(element["hex"])

    def write_payload(self, paylist: typing.List[typing.Dict]):
        """write payload to file"""

        self.adsb_exchange.get_aircraft()

        paydict = {}
        paydict["device"] = self.device
        paydict["project"] = "hyena"
        paydict["timestamp"] = self.get_timestamp()
        paydict["version"] = 1
        paydict["observation"] = paylist
        paydict["adsbex"] = self.adsb_exchange.convert_out_dict()

        out_file_name = self.get_filename()
        with open(out_file_name, "w", encoding="utf-8") as outfile:
            outfile.write(f"{json.dumps(paydict)}\n")

    def perform_collection(self):
        """read from dump1090"""

        try:
            response = requests.get(self.dump1090url, timeout=5.0)
            if response.status_code == 200:
                payload = json.loads(response.text)
                if len(payload) > 1:
                    self.process_payload(payload)
                    self.write_payload(payload)
                else:
                    print("empty response from dump1090")
            else:
                print(f"error reading dump1090:{response.status_code}")
        except:
            print("error processing dump1090")

    def execute(self, sample_sleep: int):
        """drive the collection pass"""

        limit = int(60 / sample_sleep)
        for ndx in range(int(60 / sample_sleep)):
            self.perform_collection()
            if ndx < limit - 1:
                time.sleep(sample_sleep)


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
        configuration["dump1090url"],
        configuration["exportDir"],
        configuration["rapidApiKey"],
    )
    collector.execute(configuration["sampleSleep"])

print("collection stop")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
