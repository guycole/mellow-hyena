"""mellow hyena postgresql support"""
import datetime

from typing import Dict, List

import sqlalchemy
from sqlalchemy import delete, select

from sql_table import (
    AdsbExchange,
    AdsbRanking,
    BoxScore,
    Cooked,
    Device,
    LoadLog,
    Observation,
)


class PostGres:
    """mellow hyena postgresql support"""

    Session = None

    def __init__(self, session: sqlalchemy.orm.session.sessionmaker):
        self.Session = session

    def adsb_exchange_insert(self, args: Dict[str, str]) -> AdsbExchange:
        """adsb_exchange insert row"""

        adsb_exchange = AdsbExchange(args)

        session = self.Session()
        session.add(adsb_exchange)
        session.commit()
        session.close()

        return adsb_exchange

    def adsb_exchange_select_or_insert(self, args: Dict[str, str]) -> AdsbExchange:
        """select or insert adsb_exchange row"""

        args["adsb_hex"] = args["adsb_hex"].lower()  # normalize

        statement = select(AdsbExchange).filter_by(
            adsb_hex=args["adsb_hex"],
            category=args["category"],
            emergency=args["emergency"],
            flight=args["flight"],
            model=args["model"],
            registration=args["registration"],
            ladd_flag=args["ladd_flag"],
            military_flag=args["military_flag"],
            pia_flag=args["pia_flag"],
            wierdo_flag=args["wierdo_flag"],
        )

        with self.Session() as session:
            rows = session.scalars(statement).all()
            for row in rows:
                return row

        return self.adsb_exchange_insert(args)

    def adsb_exchange_select(self, adsb_hex: str) -> AdsbExchange:
        """select adsb exchange row, note some adsb hex have multiple rows"""

        statement = select(AdsbExchange).filter_by(adsb_hex=adsb_hex)

        with self.Session() as session:
            rows = session.scalars(statement).all()
            for row in rows:
                return row

        return None

    def adsb_ranking_delete(self, score_date: datetime.date):
        """delete all rows for a specific date"""

        statement = delete(AdsbRanking).where(AdsbRanking.score_date == score_date)

        with self.Session() as session:
            session.query(AdsbRanking).filter(
                AdsbRanking.score_date == score_date
            ).delete()
            session.commit()
            session.close()

    def adsb_ranking_insert(self, args: Dict[str, str]) -> AdsbRanking:
        """adsb_ranking insert row"""

        adsb_ranking = AdsbRanking(args)

        session = self.Session()
        session.add(adsb_ranking)
        session.commit()
        session.close()

        return adsb_ranking

    def box_score_insert(self, device: str, timestampz: str) -> BoxScore:
        """box_score insert row"""

        args = {}
        args["adsb_hex_total"] = 0
        args["adsb_hex_new"] = 0
        args["device"] = device
        args["file_population"] = 0
        args["refresh_flag"] = True
        args["score_date"] = timestampz

        box_score = BoxScore(args)

        session = self.Session()
        session.add(box_score)
        session.commit()
        session.close()

        return box_score

    def box_score_select_daily(self, target_date: datetime.date) -> List[BoxScore]:
        """return all rows for a specific date"""

        statement = (
            select(BoxScore).filter_by(score_date=target_date).order_by(BoxScore.device)
        )

        results = []

        with self.Session() as session:
            rows = session.scalars(statement).all()
            for row in rows:
                results.append(row)

        return results

    def box_score_select_or_insert(self, device: str, timestampz: str) -> BoxScore:
        """select or insert box_score row"""

        statement = select(BoxScore).filter_by(device=device, score_date=timestampz)

        with self.Session() as session:
            rows = session.scalars(statement).all()
            for row in rows:
                return row

        print("must insert boxscore")
        return self.box_score_insert(device, timestampz)

    def box_score_select_refresh(self) -> List[BoxScore]:
        """select box score rows with refresh flag true"""

        statement = select(BoxScore).filter_by(refresh_flag=True)

        results = []

        with self.Session() as session:
            rows = session.scalars(statement).all()
            for row in rows:
                results.append(row)

        return results

    def box_score_update(self, box_score: BoxScore):
        """update box_score row"""

        session = self.Session()
        session.add(box_score)
        session.commit()
        session.close()

    def cooked_insert(self, args: Dict[str, str]) -> Cooked:
        """cooked insert row"""

        cooked = Cooked(args)

        session = self.Session()
        session.add(cooked)
        session.commit()
        session.close()

        return cooked

    def cooked_select(self, adsb_hex: str) -> Cooked:
        """cooked select row"""

        statement = select(Cooked).filter_by(adsb_hex=adsb_hex)

        with self.Session() as session:
            rows = session.scalars(statement).all()
            for row in rows:
                return row

        return None

    def cooked_update(self, cooked: Cooked):
        """update cooked row"""

        session = self.Session()
        session.add(cooked)
        session.commit()
        session.close()

    def device_select(self, name: str) -> Device:
        """device select row"""

        if name.endswith("anderson1"):
            name = "rpi4c-anderson1"
        elif name.endswith("vallejo1"):
            name = "rpi4a-vallejo1"
        else:
            print(f"error unknown device: {name}")
            return None

        statement = select(Device).filter_by(name=name)

        with self.Session() as session:
            rows = session.scalars(statement).all()
            for row in rows:
                return row

        return None

    def load_log_insert(self, args: Dict[str, str]) -> LoadLog:
        """load_log insert row"""

        load_log = LoadLog(args)

        session = self.Session()
        session.add(load_log)
        session.commit()
        session.close()

        return load_log

    def load_log_select(self, file_name: str) -> LoadLog:
        """load_log select row"""

        statement = select(LoadLog).filter_by(file_name=file_name)

        with self.Session() as session:
            rows = session.scalars(statement).all()
            for row in rows:
                return row

        return None

    def observation_counter(
        self, start_time: datetime.datetime, stop_time: datetime.datetime
    ) -> Dict[str, int]:
        """return a dictionary of adsb key and count of observations for one day"""

        results = {}

        with self.Session() as session:
            for row in (
                session.query(Observation).filter(
                    Observation.obs_time >= start_time,
                    Observation.obs_time <= stop_time,
                )
            ).all():
                if row.adsb_hex in results:
                    results[row.adsb_hex] = 1 + results[row.adsb_hex]
                else:
                    results[row.adsb_hex] = 1

        return results

    def observation_insert(self, args: Dict[str, str]) -> Observation:
        """observation insert row"""

        observation = Observation(args)

        session = self.Session()
        session.add(observation)
        session.commit()
        session.close()

        return observation


# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
