import requests

class Aircraft:
    headers = {}
    in_queue = []
    out_queue = []

    def __init__(self, api_key:str):
        self.api_key = api_key

        self.headers['X-RapidAPI-Key'] = api_key
        self.headers['X-RapidAPI-Host'] = 'adsbexchange-com1.p.rapidapi.com'

    def add_to_queue(self, hex:str):
        self.in_queue.append(hex)

    def parse_aircraft(self, args:dict[str, str]):
        if args['msg'] != 'No error':
            print(f"error: {args['msg']}")
            return

        if len(args['ac']) < 1:
            print("error: empty aircraft list")
            return

        unwrapped = args['ac']
        for ndx in range(len(unwrapped)):
            temp = unwrapped[0]

            results = {}

            results['flight'] = temp['flight'].strip()
            if len(results['flight']) < 1:
                results['flight'] = "unknown"

            results['hex'] = temp['hex'].strip().lower()

            results['model'] = temp['t'].strip()
            if len(results['model']) < 1:
                results['model'] = "unknown"

            results['registration'] = temp['r'].strip()
            if len(results['registration']) < 1:
                results['registration'] = "unknown"
           
            results['ladd_flag'] = False
            results['military_flag'] = False
            results['pia_flag'] = False
            results['wierdo_flag'] = False

            if 'dbFlags' in temp:
                db_flag = temp['dbFlags']

                if db_flag & 1:
                    results['military_flag'] = True

                if db_flag & 2:
                    results['wierdo_flag'] = True

                if db_flag & 4:
                    results['pia_flag'] = True

                if db_flag & 8:
                    results['ladd_flag'] = True

            self.out_queue.append(results)
      
    def get_aircraft(self):
        for ndx in range(len(self.in_queue)):
            target = self.in_queue.pop(0)
            url = f"https://adsbexchange-com1.p.rapidapi.com/v2/icao/{target}/"
            response = requests.get(url, headers=self.headers)
            self.parse_aircraft(response.json())

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
