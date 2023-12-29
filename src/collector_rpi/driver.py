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


class Collector:
    """mellow hynena collector"""

    device = None
    dump1090url = None
    export_dir = None

    def __init__(self, device: str, dump1090url: str, export_dir: str):
        self.device = device
        self.dump1090url = dump1090url
        self.export_dir = export_dir

    def get_filename(self) -> str:
        """return fully qualified filename"""

        return "%s/%s" % (self.export_dir, str(uuid.uuid4()))

    def get_timestamp(self) -> int:
        """return epoch timestamp in UTC"""

        dt = datetime.datetime.now(timezone.utc)
        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()
        return int(utc_timestamp)

    def write_payload(self, paylist: typing.List[typing.Dict]):
        """write payload to file"""

        paydict = {}
        paydict["device"] = self.device
        paydict["project"] = "hyena"
        paydict["timestamp"] = self.get_timestamp()
        paydict["version"] = 1
        paydict["observation"] = paylist

        out_file_name = self.get_filename()
        with open(out_file_name, "w", encoding="utf-8") as outfile:
            outfile.write("%s\n" % json.dumps(paydict))

    def perform_collection(self):
        """read from dump1090"""

        try:
            response = requests.get(self.dump1090url, timeout=5.0)
            if response.status_code == 200:
                payload = json.loads(response.text)
                if len(payload) > 1:
                    self.write_payload(payload)
                else:
                    print("empty response")
            else:
                print("error response from dump1090:%d" % response.status_code)
        except:
            print("error reading dump1090")

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
        file_name = sys.argv[1]
    else:
        file_name = "config.yaml"

    with open(file_name, "r", encoding="utf-8") as stream:
        try:
            configuration = yaml.load(stream, Loader=SafeLoader)
        except yaml.YAMLError as exc:
            print(exc)

    collector = Collector(
        configuration["device"],
        configuration["dump1090url"],
        configuration["exportDir"],
    )
    collector.execute(configuration["sampleSleep"])

print("collection stop")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
