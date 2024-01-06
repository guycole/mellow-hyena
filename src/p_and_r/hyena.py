"""mellow heeler hound file parser and database loader"""

import json

from typing import List

from postgres import PostGres

from sql_table import LoadLog, Observation

from typing import Dict, List

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

    def hound_v1_get_timestamp(self, buffer: List[str]) -> int:
        """return file timestamp"""

        payload = json.loads(buffer[0])
        geoloc = payload["geoLoc"]
        return geoloc['fixTimeMs']

    def hyena_v1(self, buffer: Dict[str, str], load_log: LoadLog) -> int:
        """hyena parser v1"""

        device = buffer['device']
        timestamp = buffer['timestamp']

        observation = buffer['observation']
        for ndx in range(len(observation)):
            temp = observation[ndx]
            obs = Observation(1, load_log.id, temp['altitude'], temp['hex'], temp['flight'], temp['lat'], temp['lon'], temp['speed'], temp['track'])
            self.postgres.observation_insert(obs)
          
#{"device": "rpi4c-anderson1", "project": "hyena", "timestamp": 1703826814, "version": 1, 
# "observation": [
#     {"hex": "80153b", "flight": "AIC180  ", "lat": 40.192318, "lon": -121.393994, "altitude": 28000, "track": 16, "speed": 509}, 
#     {"hex": "acc1eb", "flight": "", "lat": 39.487517, "lon": -122.630188, "altitude": 29000, "track": 175, "speed": 433}, 
#     {"hex": "a1442f", "flight": "", "lat": 39.974965, "lon": -121.679577, "altitude": 16300, "track": 176, "speed": 331}, 
#     {"hex": "ad88ef", "flight": "N971SC  ", "lat": 39.23688, "lon": -122.137817, "altitude": 16800, "track": 174, "speed": 203}, 
#     {"hex": "abf3da", "flight": "SWA3425 ", "lat": 40.49501, "lon": -121.965759, "altitude": 36000, "track": 6, "speed": 463}, 
#     {"hex": "ac13f9", "flight": "SWA2298 ", "lat": 40.024384, "lon": -122.374451, "altitude": 36000, "track": 352, "speed": 452}]}


        return 0

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
