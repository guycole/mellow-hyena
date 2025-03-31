#
# Title: postgres.py
# Description: postgresql support
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
# import sqlalchemy
# from sqlalchemy import and_
# from sqlalchemy import select

import datetime
import time

from typing import List, Dict

import sqlalchemy
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import select

from sql_table import AdsbExchange, BoxScore, Cooked, LoadLog, Observation, Site


class PostGres:
    """mellow heeler postgresql support"""

    db_engine = None
    Session = None

    def __init__(self, session: sqlalchemy.orm.session.sessionmaker):
        self.Session = session

    def adsb_exchange_insert(self, args: dict[str, any]) -> AdsbExchange:
        candidate = AdsbExchange(args)

        try:
            with self.Session() as session:
                session.add(candidate)
                session.commit()
        except Exception as error:
            print(error)

        return candidate

    def adsb_exchange_select_or_insert(self, args: dict[str, any]) -> AdsbExchange:

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
            candidate = session.scalars(statement).first()

        if candidate is None:
            return self.adsb_exchange_insert(args)
        else:
            return candidate

    def box_score_insert(self, args: dict[str, any]) -> BoxScore:
        candidate = BoxScore(args)

        try:
            with self.Session() as session:
                session.add(candidate)
                session.commit()
        except Exception as error:
            print(error)

        return candidate
        
    def box_score_update_or_insert(self, args: dict[str, any]) -> BoxScore:
        statement = select(BoxScore).filter_by(
            platform=args["platform"],
            project=args["project"],
            score_date=args["score_date"],
            site_id=args["site_id"],
        )
                
        try:
            with self.Session() as session:
                candidate = session.scalars(statement).first()
                if candidate is None:
                    candidate = self.box_score_insert(args)
                else:
                    candidate.adsb_hex_new = args['adsb_hex_new']
                    candidate.adsb_hex_total = args['adsb_hex_total']
                    candidate.file_quantity = args['file_quantity']
                    
                session.add(candidate)
                session.commit()
        except Exception as error:
            print(error)

        return candidate
        
    def cooked_insert(self, args: dict[str, any]) -> Cooked:
        # expecting obs dictionary
        args['obs_quantity'] = 1
        args['obs_first'] = args['obs_time']
        args['obs_last'] = args['obs_time']
        args['note'] = 'noNote'
        
        candidate = Cooked(args)

        try:
            with self.Session() as session:
                session.add(candidate)
                session.commit()
        except Exception as error:
            print(error)

        return candidate
    
    def cooked_select_by_adsb_hex(self, adsb_hex: str) -> Cooked:
        with self.Session() as session:
            return session.scalars(select(Cooked).filter_by(adsb_hex=adsb_hex)).first()

    def cooked_update_or_insert(self, args: dict[str, any]) -> Cooked:
        # expecting observation
        
        try:
            with self.Session() as session:
                candidate = session.scalars(select(Cooked).filter_by(adsb_hex=args['adsb_hex'])).first()

                if candidate is None:
                    candidate = self.cooked_insert(args)
                else:
                    candidate.obs_quantity += 1

                    if args['obs_time'] < candidate.obs_first:
                        candidate.obs_first = args['obs_time']
                    elif args['obs_time'] > candidate.obs_last:
                        candidate.obs_last = args['obs_time']

                    session.add(candidate)
                    session.commit()
        except Exception as error:
            print(error)

        return candidate

    def load_log_insert(self, args: dict[str, any], obs_quantity: int, site_id: int) -> LoadLog:
        args["obs_quantity"] = obs_quantity
        
        candidate = LoadLog(args, site_id)

        try:
            with self.Session() as session:
                session.add(candidate)
                session.commit()
        except Exception as error:
            print(error)

        return candidate
    
    def load_log_select_all(self) -> list[LoadLog]:
        with self.Session() as session:
            return session.scalars(select(LoadLog)).all()

    def load_log_select_by_file_name(self, file_name: str) -> LoadLog:
        with self.Session() as session:
            return session.scalars(select(LoadLog).filter_by(file_name=file_name)).first()

    def load_log_select_by_obs_date(self, target: datetime) -> list[LoadLog]:
        with self.Session() as session:
            return session.scalars(select(LoadLog).filter_by(obs_date=target)).all()

    def observation_insert(self, args: [str, any], load_log_id: int) -> Observation:
        candidate = Observation(args, load_log_id)

        try:
            with self.Session() as session:
                session.add(candidate)
                session.commit()
        except Exception as error:
            print(error)

        return candidate

    def observation_select_by_load_log_id(self, load_log_id: int) -> list[Observation]:
        with self.Session() as session:
            return session.scalars(select(Observation).filter_by(load_log_id=load_log_id)).all()

    def site_select_by_id(self, id: int) -> Site:
        with self.Session() as session:
            return session.scalars(select(Site).filter_by(id=id)).first()

    def site_select_by_name(self, name: str) -> Site:
        with self.Session() as session:
            return session.scalars(select(Site).filter_by(name=name)).first()

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
