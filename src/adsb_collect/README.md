mellow-hyena/adsb_collect
=========================

## Introduction
Python script to read json from [dump1090](https://github.com/antirez/dump1090) and produce a json formatted file.  Runs from cron every minute and exits.  Eventually the output files are moved to AWS S3 for later processing.  There is a data flow diagram at the bottom of this file.

[ADSB Exchange]("https://www.adsbexchange.com/data/") offers an API to collect aircraft information.  Results are best when requesting while the flight is active, so I make the API requests each collection cycle.  The results are stored in the output file along with the raw observation.

## Bill Of Materials
1. Raspberry Pi 3 w/power supply
1. RTL-SDR w/antenna

### collector.py
cron(8) will invoke [adsb-collector.sh](https://github.com/guycole/mellow-hyena/blob/main/bin/adsb-collector.sh) to run [collector.py](https://github.com/guycole/mellow-hyena/blob/main/src/adsb_collect/collector.py) and produce an observation file.  

### collector.py installation
1. Run virtualenv within the adsb_collect directory 
1. import requirements.txt 
1. tweak config.yaml
1. run python collector.py to verify output files are produced and there are no error messages.
1. edit crontab(5) if you want automated collection, there is a sample crontab in the bin directory.

## dump1090
[dump1090](https://github.com/antirez/dump1090.git) reads from rtl-sdr and exposes a web endpoint that provides a jason formatted report of all ADSB emitters observed.  There is a curl example near the bottom of the file.

### dump1090 installation
1. This link was a big help [vortac.io](https://vortac.io/2020/06/02/installing-dump1090-on-raspberrypi/)
    1. use https://github.com/osmocom/rtl-sdr.git
    1. LD_LIBRARY_PATH=/usr/local/lib/arm-linux-gnueabihf; export LD_LIBRARY_PATH
    1. I start dump1090 within rc.local so it starts at boot, example within infra directory

### also needs AWS if copying files to S3
https://stackoverflow.com/questions/63030641/how-to-install-awscli-version-2-on-raspberry-pi

### curl dump1090 example
```
curl -v http://127.0.0.1:8080/data.json
*   Trying 127.0.0.1:8080...
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> GET /data.json HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.74.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: Dump1090
< Content-Type: application/json;charset=utf-8
< Connection: keep-alive
< Content-Length: 119
< Access-Control-Allow-Origin: *
<
[
{"hex":"a89d0a", "flight":"QXE2335 ", "lat":40.431564, "lon":-122.294434, "altitude":1650, "track":2, "speed":137}
]
* Connection #0 to host 127.0.0.1 left intact
```

### output file example
```
{
    "device": "rpi4c-adsb-anderson1", 
    "project": "hyena", 
    "timestamp": 1706499497, 
    "version": 1, 
    "observation": [
        {
            "adsb_hex": "a68e4c", 
            "flight": "SKW4846", 
            "lat": 38.447354, 
            "lon": -120.296875, 
            "altitude": 24700, 
            "track": 100, 
            "speed": 382
        }
    ],
    "adsbex": [
        {
            "adsb_hex": "a68e4c", 
            "category": "A3", 
            "emergency": "none", 
            "flight": "SKW4846", 
            "registration": "N521SY", 
            "model": "E75L", 
            "ladd_flag": false, 
            "military_flag": false, 
            "pia_flag": false, 
            "wierdo_flag": false}
    ]
}
```

## Data Flow Diagram
![Data Flow](https://github.com/guycole/mellow-hyena/blob/main/src/adsb_collect/adsb_data_flow.png)