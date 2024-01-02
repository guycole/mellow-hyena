"""mellow hyena processing"""

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

class Processing:
    """mellow hynena collector"""

    device = None
    dump1090url = None
    export_dir = None

    def __init__(self, device: str, dump1090url: str, export_dir: str):
        self.device = device
        self.dump1090url = dump1090url
        self.export_dir = export_dir

    def execute2(self, sample_sleep: int):
        """drive processing pass"""

        url = "https://adsbexchange-com1.p.rapidapi.com/v2/registration/N8737L/"
        url = "https://adsbexchange-com1.p.rapidapi.com/v2/icao/aa94bf/"

        headers = {
	        "X-RapidAPI-Key": "430f31d221msh509486783ac5c1fp198a6bjsn2588078c1869",
	        "X-RapidAPI-Host": "adsbexchange-com1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        print(response.json())

#        response = requests.get('https://adsbexchange.com1.p.rapidapi.com', headers = headers)
#        print(response)
#        #data = response.text


print("processing start")

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

    processor = Processing(
        configuration["device"],
        configuration["dump1090url"],
        configuration["exportDir"],
    )
    processor.execute(configuration["sampleSleep"])

print("processing stop")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
