"""mellow heeler postgresql support"""

from typing import Dict


import sqlalchemy
from sqlalchemy import select, update

from sql_table import AdsbExchange, Cooked, Device, LoadLog, Observation


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

    def adsb_exchange_select_or_insert(self, args: Dict[str, str]) -> AdsbExchange:
        """select or insert adsb_exchange row"""

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

    def cooked_insert(self, args: Dict[str, str]) -> Cooked:
        """cooked insert row"""

        cooked = Cooked(args)

        session = self.Session()
        session.add(cooked)
        session.commit()
        session.close()

        return cooked

    def cooked_select(self, adsb_hex:str) -> Cooked:
        """cooked select row"""
        
        statement = (select(Cooked).filter_by(adsb_hex=adsb_hex))

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
        session.add(observation)
        session.commit()
        session.close()

        return observation


# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
