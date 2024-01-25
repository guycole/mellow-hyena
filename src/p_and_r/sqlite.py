"""mellow hyena sqlite3 support"""

import sqlite3
from sqlite3 import Error

from typing import Dict


class SqlLite:
    """mellow hyena sqlite3 support"""

    db_connection = None

    def __init__(self, db_connection: sqlite3.Connection):
        self.db_connection = db_connection
        print(self.db_connection)

    def adsb_exchange_insert(self, args: Dict[str, str]):
        """adsb insert row"""

        sql = "insert into hyena_adsbexchange (adsb_hex, category, emergency, flight, model, registration, ladd_flag, military_flag, pia_flag, wierdo_flag) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        values = (
            args["adsb_hex"],
            args["category"],
            args["emergency"],
            args["flight"],
            args["model"],
            args["registration"],
            args["ladd_flag"],
            args["military_flag"],
            args["pia_flag"],
            args["wierdo_flag"],
        )

        cursor = self.db_connection.cursor()
        cursor.execute(sql, values)
        self.db_connection.commit()

    def adsb_exchange_select(self, args: Dict[str, str]) -> Dict[str, str]:
        """adsb select row"""

        cursor = self.db_connection.cursor()
        rows = cursor.execute(
            "select id, adsb_hex, category, emergency, flight, model, registration, ladd_flag, military_flag, pia_flag, wierdo_flag from hyena_adsbexchange where adsb_hex = ?",
            (args["adsb_hex"],),
        ).fetchall()

        results = {}

        for row in rows:
            if (
                row[2] == args["category"]
                and row[3] == args["emergency"]
                and row[4] == args["flight"]
                and row[5] == args["model"]
                and row[6] == args["registration"]
                and row[7] == args["ladd_flag"]
                and row[8] == args["military_flag"]
                and row[9] == args["pia_flag"]
                and row[10] == args["wierdo_flag"]
            ):
                results["id"] = row[0]
                results["adsb_hex"] = row[1]
                results["category"] = row[2]
                results["emergency"] = row[3]
                results["flight"] = row[4]
                results["model"] = row[5]
                results["registration"] = row[6]
                results["ladd_flag"] = row[7]
                results["military_flag"] = row[8]
                results["pia_flag"] = row[9]
                results["wierdo_flag"] = row[10]
                break

        return results

    def load_log_insert(self, args: Dict[str, str]):
        """load_log insert row"""

        sql = "insert into hyena_loadlog (file_name, load_time, obs_time, population) values (?, ?, ?, ?)"
        values = (
            args["file_name"],
            args["load_time"],
            args["obs_time"],
            args["population"],
        )

        cursor = self.db_connection.cursor()
        cursor.execute(sql, values)
        self.db_connection.commit()

    def load_log_select(self, file_name: str) -> Dict[str, str]:
        """load_log select row"""

        cursor = self.db_connection.cursor()
        rows = cursor.execute(
            "select id, file_name, load_time, obs_time, population from hyena_loadlog where file_name = ?",
            (file_name,),
        ).fetchall()

        results = {}
        if len(rows) > 0:
            results["id"] = rows[0][0]
            results["file_name"] = rows[0][1]
            results["load_time"] = rows[0][2]
            results["obs_time"] = rows[0][3]
            results["population"] = rows[0][4]

        return results

    def observation_insert(self, obs_time: str, args: Dict[str, str]):
        """observation insert row"""

        sql = "insert into hyena_observation (adsb_hex, altitude, bearing, flight, latitude, longitude, obs_time, range, speed, track) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        values = (
            args["adsb_hex"],
            args["altitude"],
            args["bearing"],
            args["flight"],
            args["lat"],
            args["lon"],
            obs_time,
            args["range"],
            args["speed"],
            args["track"],
        )

        cursor = self.db_connection.cursor()
        cursor.execute(sql, values)
        self.db_connection.commit()

    def observation_select(self, adsb_hex: str, obs_time: str) -> Dict[str, str]:
        """observation select row"""

        cursor = self.db_connection.cursor()
        rows = cursor.execute(
            "select id, adsb_hex, altitude, bearing, flight, latitude, longitude, obs_time, range, speed, track from hyena_observation where adsb_hex = ? and obs_time = ?",
            (adsb_hex, obs_time),
        ).fetchall()

        results = {}

        if len(rows) > 0:
            results["id"] = rows[0][0]
            results["adsb_hex"] = rows[0][1]
            results["altitude"] = rows[0][2]
            results["bearing"] = rows[0][3]
            results["flight"] = rows[0][4]
            results["latitude"] = rows[0][5]
            results["longitude"] = rows[0][6]
            results["obs_time"] = rows[0][7]
            results["range"] = rows[0][8]
            results["speed"] = rows[0][9]
            results["track"] = rows[0][10]

        return results
