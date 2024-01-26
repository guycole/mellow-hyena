"""mellow heeler hound file parser and database loader, runs for each file"""

from datetime import datetime, timezone

from typing import Dict

from postgres import PostGres

from sql_table import Device, LoadLog

from great_circle import range_and_bearing


class Hyena:
    """mellow hyena file parser and database loader"""

    device = None
    postgres = None
    run_stats = {}

    def __init__(self, device: Device, postgres: PostGres):
        self.device = device
        self.postgres = postgres

        self.run_stats["hex_new"] = 0
        self.run_stats["hex_total"] = 0

    def run_stat_bump(self, key: str):
        """increment a run_stat"""

        if key in self.run_stats:
            self.run_stats[key] = self.run_stats[key] + 1
        else:
            print(f"unknown run_stats key: {key}")

    def run_stat_dump(self):
        """print run_stats summary"""

        print(f"total: {self.run_stats['hex_total']} new: {self.run_stats['hex_new']}")

    def hyena_v1_load_adsb_exchange(self, buffer: Dict[str, str]) -> Dict[str, str]:
        """hyena_v1 load_adsb_exchange"""

        results = {}

        for element in buffer:
            if "hex" in element:
                element["adsb_hex"] = element["hex"]

            results[element["adsb_hex"]] = self.postgres.adsb_exchange_select_or_insert(
                element
            ).id

        return results

    def hyena_v1_load_boxscore(self, device: str, obs_time: str):
        """hyena_v1 load_boxscore"""

        box_score = self.postgres.box_score_select_or_insert(device, obs_time)
        box_score.adsb_hex_new = box_score.adsb_hex_new + self.run_stats["hex_new"]
        box_score.adsb_hex_total = (
            box_score.adsb_hex_total + self.run_stats["hex_total"]
        )
        box_score.file_population = box_score.file_population + 1
        box_score.refresh_flag = True

        self.postgres.box_score_update(box_score)

    def hyena_v1_load_log(self, buffer: Dict[str, str]) -> LoadLog:
        """hyena_v1 load_log"""

        load_dict = {}
        load_dict["device"] = self.device.name
        load_dict["file_name"] = buffer["file_name"]
        load_dict["file_type"] = buffer["file_type"]
        load_dict["obs_time"] = datetime.fromtimestamp(buffer["timestamp"], timezone.utc)
        load_dict["population"] = len(buffer["observation"])

        return self.postgres.load_log_insert(load_dict)

    def hyena_v1_load_cooked(self, buffer: Dict[str, str], timestamp: str):
        """hyena_v1 load_cooked"""

        timestampz = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)

        cooked_dict = {}

        if "hex" in buffer:
            cooked_dict["adsb_hex"] = buffer["hex"].lower()
        else:
            cooked_dict["adsb_hex"] = buffer["adsb_hex"].lower()

        cooked_dict["note"] = "no note"
        cooked_dict["observed_counter"] = 1
        cooked_dict["observed_first"] = timestampz
        cooked_dict["observed_last"] = timestampz

        cooked = self.postgres.cooked_select(cooked_dict["adsb_hex"])
        if cooked is None:
            # fresh first entry
            cooked = self.postgres.cooked_insert(cooked_dict)
            self.run_stat_bump("hex_new")
        else:
            # update existing entry
            cooked.observed_counter = cooked.observed_counter + 1

            if timestampz < cooked.observed_first:
                cooked.observed_first = timestampz

            if timestampz > cooked.observed_last:
                cooked.observed_last = timestampz

            self.postgres.cooked_update(cooked)

    def hyena_v1_load_observation(
        self, buffer: Dict[str, str], adsb_keys: Dict[str, str], load_log: LoadLog
    ):
        """hyena_v1 load_observation"""

        obs_dict = {}
        obs_dict["altitude"] = buffer["altitude"]
        obs_dict["latitude"] = buffer["lat"]
        obs_dict["longitude"] = buffer["lon"]
        obs_dict["load_log_id"] = load_log.id
        obs_dict["obs_time"] = load_log.obs_time
        obs_dict["speed"] = buffer["speed"]
        obs_dict["track"] = buffer["track"]

        if len(buffer["flight"]) < 1:
            obs_dict["flight"] = "unknown"
        else:
            obs_dict["flight"] = buffer["flight"].strip()

        (range2, bearing) = range_and_bearing(
            self.device.latitude, self.device.longitude, buffer["lat"], buffer["lon"]
        )
        obs_dict["bearing"] = round(bearing, 2)
        obs_dict["range"] = round(range2, 2)

        if "hex" in buffer:
            obs_dict["adsb_hex"] = buffer["hex"].lower()
        else:
            obs_dict["adsb_hex"] = buffer["adsb_hex"].lower()

        if obs_dict["adsb_hex"] in adsb_keys:
            obs_dict["adsb_exchange_id"] = adsb_keys[obs_dict["adsb_hex"]]
        else:
            obs_dict["adsb_exchange_id"] = 1

        self.postgres.observation_select_or_insert(obs_dict)

    def hyena_v1_loader(self, buffer: Dict[str, str]) -> int:
        """hyena_v1 loader"""

        load_log = self.hyena_v1_load_log(buffer)

        adsb_keys = {}
        if "adsbex" in buffer:
            try:
                adsb_keys = self.hyena_v1_load_adsb_exchange(buffer["adsbex"])
            except:
                print("adsbex parse error")

        observation = buffer["observation"]
        for element in observation:
            try:
                self.hyena_v1_load_observation(element, adsb_keys, load_log)
                self.hyena_v1_load_cooked(element, buffer["timestamp"])
                self.run_stat_bump("hex_total")
            except:
                print("observation parse error")
                return -1

        self.run_stat_dump()
        self.hyena_v1_load_boxscore(load_log.device, load_log.obs_time)

        return 0


# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
