"""mellow heeler postgresql support"""

from typing import Dict


import sqlalchemy
from sqlalchemy import select

from sql_table import Aircraft, LoadLog, Observation


class PostGres:
    """mellow heeler postgresql support"""

    Session = None

    def __init__(self, session: sqlalchemy.orm.session.sessionmaker):
        self.Session = session

    def aircraft_insert(self, args: Dict[str, str]) -> Aircraft:
        """aircraft insert row"""

        aircraft = Aircraft(args)

        session = self.Session()
        session.add(aircraft)
        session.commit()
        session.close()

        return aircraft

    def aircraft_select(self, adsb_hex: str, flight: str) -> Aircraft:
        """aircraft select row"""

        statement = (
            select(Aircraft)
            .filter_by(adsb_hex=adsb_hex, flight=flight)
            .order_by(Aircraft.version)
        )

        row = None
        with self.Session() as session:
            rows = session.scalars(statement).all()
            for row in rows:
                continue

        return row

    def aircraft_select_or_insert(self, args: Dict[str, str]) -> Aircraft:
        """discover if aircraft exists or if not, max version for insert"""

        statement = (
            select(Aircraft)
            .filter_by(adsb_hex=args["adsb_hex"])
            .order_by(Aircraft.version)
        )

        row = None
        with self.Session() as session:
            rows = session.scalars(statement).all()
            for row in rows:
                if (
                    row.adsb_hex == args["adsb_hex"]
                    and row.category == args["category"]
                    and row.emergency == args["emergency"]
                    and row.flight == args["flight"]
                    and row.model == args["model"]
                    and row.registration == args["registration"]
                    and row.ladd_flag == args["ladd_flag"]
                    and row.military_flag == args["military_flag"]
                    and row.pia_flag == args["pia_flag"]
                    and row.wierdo_flag == args["wierdo_flag"]
                ):
                    return row

        if row is None:
            args["version"] = 1
        else:
            args["version"] = row.version + 1

        return self.aircraft_insert(args)

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
