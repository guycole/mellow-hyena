"""mellow heeler postgresql support"""

from typing import Dict


import sqlalchemy
from sqlalchemy import select

from sql_table import AdsbExchange, Device, LoadLog, Observation


class PostGres:
    """mellow heeler postgresql support"""

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

#    def adsb_exchanget_select(self, adsb_hex: str, flight: str) -> AdsbExchange:
#        """aircraft select row"""
#
#        statement = (
#            select(Aircraft)
#            .filter_by(adsb_hex=adsb_hex, flight=flight)
#            .order_by(Aircraft.version)
#        )

#        row = None
#        with self.Session() as session:
#            rows = session.scalars(statement).all()
#            for row in rows:
#                continue
#
#        return row

    def adsb_exchange_select_or_insert(self, args: Dict[str, str]) -> AdsbExchange:
        """discover if adsb row exists or if not, max version for insert"""

        args['adsb_hex'] = args['adsb_hex'].lower() # normalize

        statement = (
            select(AdsbExchange)
            .filter_by(adsb_hex=args["adsb_hex"], category=args['category'], emergency=args['emergency'], flight=args['flight'], model=args['model'], registration=args['registration'], ladd_flag=args['ladd_flag'], military_flag=args['military_flag'], pia_flag=args['pia_flag'], wierdo_flag=args['wierdo_flag'])
        )

        with self.Session() as session:
            rows = session.scalars(statement).all()
            for row in rows:
                return row

        return self.adsb_exchange_insert(args)

    def device_select(self, name: str) -> Device:
        """device select row"""

        if name.endswith("anderson1"):
            name = 'rpi4c-anderson1'
        elif name.endswith("vallejo1"):
            name = 'rpi4a-vallejo1'
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

    def observation_insert(self, args: Dict[str, str]) -> Observation:
        """observation insert row"""

        observation = Observation(args)

        session = self.Session()
#        session.add(observation)
#        session.commit()
        session.close()

        return observation


# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
