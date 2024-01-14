"""mellow heeler hound file parser and database loader, runs for each file"""

import time

from geopy import distance
from typing import Dict

from postgres import PostGres

from sql_table import AdsbExchange, Device, LoadLog


class Hyena:
    """mellow hyena file parser and database loader"""

    device = None
    postgres = None
    run_stats = {}

    def __init__(self, device: Device, postgres: PostGres):
        self.device = device
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

    def discover_aircraft(self, args: Dict[str, str]) -> AdsbExchange:
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

    def hyena_v1_range_and_bearing(self, latitude: float, longitude: float) -> (float, float):
        """hyena_v1 range and bearing"""

        origin = (self.device.latitude, self.device.longitude)
        destination = (latitude, longitude)

        distance2 = distance.distance(origin, destination).miles
        print(distance2)
        bearing2 = distance.bearing(origin, destination)
        print(bearing2)

        return (distance2, bearing2)

    #    return (0.0, 0.0)

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

    def hyena_v1_load_adsb_exchange(self, buffer: Dict[str, str]) -> Dict[str, str]:
        """hyena_v1 load_adsb_exchange"""

        results = {}

        for element in buffer:
            if "hex" in element:
                element['adsb_hex'] = element['hex']

            results[element['adsb_hex']] = self.postgres.adsb_exchange_select_or_insert(element).id

        return(results)

    def hyena_v1_load_observation(self, buffer: Dict[str, str], adsb_keys: Dict[str, str], load_log: LoadLog):
        """hyena_v1 load_observation"""
     
        obs_dict = {}
        obs_dict["altitude"] = buffer["altitude"]
        obs_dict["latitude"] = buffer["lat"]
        obs_dict["longitude"] = buffer["lon"]
#        obs_dict["load_log_id"] = load_log.id
#        obs_dict["obs_time"] = load_log.obs_time
        obs_dict["load_log_id"] = 1
        obs_dict["obs_time"] = 12345
        obs_dict["speed"] = buffer["speed"]
        obs_dict["track"] = buffer["track"]

        if len(buffer["flight"]) < 1:
            obs_dict["flight"] = "unknown"
        else:
            obs_dict["flight"] = buffer["flight"].strip()

        (obs_dict['range'], obs_dict['bearing']) = self.hyena_v1_range_and_bearing(buffer["lat"], buffer["lon"])
        
        if "hex" in buffer:
            obs_dict["adsb_hex"] = buffer["hex"].lower()
        else:
            obs_dict["adsb_hex"] = buffer["adsb_hex"].lower()

        if obs_dict["adsb_hex"] in adsb_keys:
            obs_dict["adsb_exchange_id"] = adsb_keys[obs_dict["adsb_hex"]]
        else:
            obs_dict["adsb_exchange_id"] = 1

        self.postgres.observation_insert(obs_dict)

    def hyena_v1_loader(self, buffer: Dict[str, str]) -> int:
        """hyena_v1 loader"""

#        load_log = self.hyena_v1_load_log(buffer)
        load_log = None

        adsb_keys = {}
        if "adsbex" in buffer:
            adsb_keys = self.hyena_v1_load_adsb_exchange(buffer["adsbex"])

        observation = buffer["observation"]
        for element in observation:
            self.hyena_v1_load_observation(element, adsb_keys, load_log)

        return -1

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
