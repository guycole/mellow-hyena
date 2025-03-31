#
# Title: converter.py
# Description: parse mellow hyena files and load to postgresql
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
import datetime 
import os
import sys

class Converter:

    def adsb_processor(self, args: dict[str, any]) -> list[dict[str, any]]:
        adsb_list = args['adsbex']

        for adsb in adsb_list:
            if 'hex' in adsb:
                adsb['adsb_hex'] = adsb['hex']
        
        return adsb_list


    def find_adsbex_id(self, arg_list: list[dict[str, any]], target: str) -> int:
        for arg in arg_list:
            if arg['adsb_hex'] == target:
                return(arg['pk_id'])

        return 1

    def obs_processor(self, args: dict[str, any]) -> list[dict[str, any]]:
        adsb_list = args['adsbex']
        
        obs_list = args['observation']
        for obs in obs_list:
            if 'hex' in obs:
                obs['adsb_hex'] = obs['hex']

            obs['adsb_exchange_id'] = self.find_adsbex_id(adsb_list, obs['adsb_hex'])
            obs['bearing'] = -1.0
            obs['range'] = -1.0
            obs['obs_time'] = args['obs_datetime']

        return obs_list

    def fresh_payload(self, args: dict[str, any]) -> dict[str, any]:
        tokens = args['device'].split('-')

        if "adsb-1090" in args['device']:
            project = "adsb-1090";
        else:
            project = "unknown"

        return {
            "adsbex": [],
            "file_name": args['file_name'],
            "file_type": args['project'] + "_" + str(args['version']),
            "observation": [],
            "obs_quantity": 0,
            "obs_datetime": datetime.datetime.fromtimestamp(args['timestamp']),
            "obs_time_seconds": args['timestamp'],
            "platform": tokens[0],
            "project": project,
            "site": tokens[-1]
        }

    def converter(self, args: dict[str, any]) -> dict[str, any]:
        payload = self.fresh_payload(args)

        if 'adsbex' in args:
            payload['adsbex'] = args['adsbex']
        else:
            payload['adsbex'] = []

        payload['observation'] = args['observation']

        return payload

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
