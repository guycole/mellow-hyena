"""adsb exchange API wrapper"""

from typing import List, Dict

import requests


class AdsbExchange:
    """adsb exchange API wrapper"""

    headers = {}
    in_queue = []
    out_dict = {}

    def __init__(self, api_key: str):
        self.api_key = api_key

        self.headers["X-RapidAPI-Key"] = api_key
        self.headers["X-RapidAPI-Host"] = "adsbexchange-com1.p.rapidapi.com"

    def add_to_queue(self, adsb_hex: str):
        """add adsb hex code to queue for later processing"""

        self.in_queue.append(adsb_hex)

    def convert_out_dict(self) -> List[str]:
        """convert collected ADSB exchange elements to a list for JSON"""

        results = []
        for _, value in self.out_dict.items():
            results.append(value)

        return results

    def janitor(self, value: str) -> str:
        """clean up string values"""

        temp = value.strip()
        if len(temp) < 1:
            return "unknown"

        return temp

    def parse_aircraft(self, args: Dict[str, str]):
        """parse ADSB exchange API response"""

        if args["msg"] != "No error":
            print(f"error: {args['msg']}")
            return

        if len(args["ac"]) < 1:
            print("error: empty aircraft list")
            return

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

            self.out_dict[results["adsb_hex"]] = results

    def get_aircraft(self):
        """process enqueued ADSB hex codes"""

        while len(self.in_queue) > 0:
            target = self.in_queue.pop(0)
            print(f"adsbex:{target}")

            if target not in self.out_dict:
                url = f"https://adsbexchange-com1.p.rapidapi.com/v2/icao/{target}/"
                response = requests.get(url, headers=self.headers, timeout=5.0)
                self.parse_aircraft(response.json())
            else:
                print(f"skipping known hex:{target}")
                continue


# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
