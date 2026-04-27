"""adsb exchange API wrapper"""

import requests
import sys

import yaml
from yaml.loader import SafeLoader


class AdsbExchange:
    """adsb exchange API wrapper"""

    headers = {}

    def __init__(self, api_key: str):
        self.api_key = api_key

        self.headers["X-RapidAPI-Key"] = api_key
        self.headers["X-RapidAPI-Host"] = "adsbexchange-com1.p.rapidapi.com"
        self.headers["Content-Type"] = "application/json"

    def janitor(self, value: str) -> str:
        """clean up string values"""

        temp = value.strip()
        if len(temp) < 1:
            return "unknown"

        return temp

    def parse_aircraft(self, args: dict[str, str]) -> list[dict[str, any]]:
        """parse ADSB exchange API response"""

        if args["msg"] != "No error":
            print(f"error: {args['msg']}")
            return []

        if len(args["ac"]) < 1:
            print("error: empty aircraft list")
            return []

        retlist = []
        unwrapped = args["ac"]
        for ndx, _ in enumerate(unwrapped):
            results = {}

            temp = unwrapped[ndx]

            results["adsb_hex"] = temp["hex"].strip().lower()

            if "category" in temp:
                results["category"] = self.janitor(temp["category"])
            else:
                results["category"] = "none"

            if "emergency" in temp:
                results["emergency"] = self.janitor(temp["emergency"])
            else:
                results["emergency"] = "none"

            if "flight" in temp:
                results["flight"] = self.janitor(temp["flight"])
            else:
                results["flight"] = "unknown"

            if "r" in temp:
                results["registration"] = self.janitor(temp["r"])
            else:
                results["registration"] = "unknown"

            if "t" in temp:
                results["model"] = self.janitor(temp["t"])
            else:
                results["model"] = "unknown"

            results["ladd_flag"] = False
            results["military_flag"] = False
            results["pia_flag"] = False
            results["wierdo_flag"] = False

            if "dbFlags" in temp:
                db_flag = temp["dbFlags"]

                if db_flag & 1:
                    results["military_flag"] = True

                if db_flag & 2:
                    results["wierdo_flag"] = True

                if db_flag & 4:
                    results["pia_flag"] = True

                if db_flag & 8:
                    results["ladd_flag"] = True

            retlist.append(results)

        return retlist

    def fetch(self, adsb_hex: str) -> dict[str, any]:
        try:
            url = f"https://adsbexchange-com1.p.rapidapi.com/v2/icao/{adsb_hex}/"
            response = requests.get(url, headers=self.headers, timeout=5.0)
            if response.status_code != 200:
                print(f"skipping {adsb_hex} bad response {response.status_code}")
                return {}

            return response.json()
        except Exception as error:
            print(error)

    def execute(self, adsb_hex: str) -> list[dict[str, any]]:
        retlist = []

        raw = self.fetch(adsb_hex)
        if len(raw) < 1:
            return retlist

        retlist = self.parse_aircraft(raw)
        return retlist


print("adsb start")

#
# argv[1] = configuration filename
#
if __name__ == "__main__":
    if len(sys.argv) > 1:
        config_file_name = sys.argv[1]
    else:
        config_file_name = "config.yaml"

    api_key = None
    with open(config_file_name, "r", encoding="utf-8") as stream:
        try:
            configuration = yaml.load(stream, Loader=SafeLoader)
            api_key = configuration["rapidApiKey"]
        except yaml.YAMLError as exc:
            print(exc)

    adsbex = AdsbExchange(api_key)
    adsbex.execute("a4caaa")

print("adsb stop")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
