"""mellow heeler hound file parser and database loader"""

import time

from typing import Dict

from postgres import PostGres

from sql_table import Aircraft, LoadLog


class Hyena:
    """mellow hyena file parser and database loader"""

    postgres = None
    run_stats = {}

    def __init__(self, postgres: PostGres):
        self.postgres = postgres

        self.run_stats["fresh_cooked"] = 0
        self.run_stats["fresh_observation"] = 0
        self.run_stats["fresh_wap"] = 0
        self.run_stats["update_wap"] = 0

    def run_stat_bump(self, key: str):
        """increment a run_stat"""

        if key in self.run_stats:
            self.run_stats[key] = self.run_stats[key] + 1
        else:
            print(f"unknown run_stats key: {key}")

    def run_stat_dump(self):
        """print run_stats summary"""

        print(
            f"cooked: {self.run_stats['fresh_cooked']} observation: {self.run_stats['fresh_observation']} wap: {self.run_stats['fresh_wap']}"
        )

    def discover_aircraft(self, args: Dict[str, str]) -> Aircraft:
        """hyena_v1 discover if known aircraft, or create new"""

        print("-x-x-x-")
        print(args)
        print("-x-x-x-")

        # stub for now

        air_dict = {}
        air_dict["air_type"] = "unknown"
        air_dict["callsign"] = "unknown"
        air_dict["hex"] = "0000"
        air_dict["version"] = 1

        aircraft = Aircraft(air_dict)
        aircraft.id = 1

        return aircraft

    def hyena_v1_load_log(self, buffer: Dict[str, str]) -> LoadLog:
        """hyena_v1 load_log"""

        load_dict = {}
        load_dict["device"] = buffer["device"]
        load_dict["file_name"] = buffer["file_name"]
        load_dict["file_type"] = buffer["file_type"]
        load_dict["obs_time"] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.gmtime(buffer["timestamp"])
        )
        load_dict["population"] = len(buffer["observation"])

        return self.postgres.load_log_insert(load_dict)

    def hyena_v1_load_aircraft(self, buffer: Dict[str, str]):
        """hyena_v1 load_aircraft"""

        for element in buffer:
            self.postgres.aircraft_select_or_insert(element)

    def hyena_v1_load_observation(self, buffer: Dict[str, str], load_log: LoadLog):
        """hyena_v1 load_observation"""

        obs_dict = {}
        obs_dict["adsb_hex"] = buffer["hex"].lower()
        obs_dict["altitude"] = buffer["altitude"]

        obs_dict["flight"] = buffer["flight"].strip()
        if len(obs_dict["flight"]) < 1:
            obs_dict["flight"] = "unknown"

        obs_dict["latitude"] = buffer["lat"]
        obs_dict["longitude"] = buffer["lon"]
        obs_dict["speed"] = buffer["speed"]
        obs_dict["track"] = buffer["track"]

        obs_dict["load_log_id"] = load_log.id
        obs_dict["obs_time"] = load_log.obs_time

        self.postgres.observation_insert(obs_dict)

    def hyena_v1_loader(self, buffer: Dict[str, str]) -> int:
        """hyena_v1 loader"""

        load_log = self.hyena_v1_load_log(buffer)

        if "adsbex" in buffer:
            self.hyena_v1_load_aircraft(buffer["adsbex"])

        observation = buffer["observation"]
        for element in observation:
            self.hyena_v1_load_observation(element, load_log)

        return 0


# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
