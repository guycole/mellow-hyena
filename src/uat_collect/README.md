mellow-hyena/uat_collect
=========================

## Introduction
Python script to read json from [dump978](https://github.com/mutability/dump978) and produce a json formatted file.  Runs from cron every minute and exits.  Eventually the output files are moved to AWS S3 for later processing.  There is a data flow diagram at the bottom of this file.

## Bill Of Materials
1. Raspberry Pi 3 w/power supply
1. RTL-SDR w/antenna

## dump978 
[dump978](https://github.com/mutability/dump978) reads from rtl-sdr and writes a json formatted file with a summary of any observed beacons.  There is a file sample later in this README.

### dump978 installation
You will need a working copy of [rtl-sdr](https://github.com/osmocom/rtl-sdr.git)

Then build dump978 and test, the aircraft.json file should appear in /tmp

```
rtl_sdr -f 978000000 -s 2083334 -g 48 - | ./dump978 | ./uat2json /tmp
```

### also needs AWS if copying files to S3
https://stackoverflow.com/questions/63030641/how-to-install-awscli-version-2-on-raspberry-pi

### dump978 aircraft.json example
```
{
  "now" : 1706656092,
  "messages" : 947,
  "aircraft" : [
    {"hex":"a1c0de","squawk":"1200","flight":"N2119T","lat":38.195772,"lon":-122.280171,"seen_pos":48,"altitude":900,"vert_rate":128,"track":115,"speed":89,"messages":8,"seen":48,"rssi":0},
    {"hex":"a51612","squawk":"1200","flight":"N427EP","lat":38.122108,"lon":-122.208652,"seen_pos":2,"altitude":3600,"vert_rate":-192,"track":138,"speed":96,"messages":219,"seen":2,"rssi":0},
    {"hex":"a8f523","squawk":"1200","flight":"N67651","lat":38.103075,"lon":-122.260151,"seen_pos":0,"altitude":3000,"vert_rate":0,"track":143,"speed":73,"messages":652,"seen":0,"rssi":0}
  ]
}
```

### output file example
```
{
    "device": "rpi3b-uat-anderson1", 
    "project": "hyena", 
    "timestamp": 1706499497, 
    "version": 1, 
    "observation": [
        {
            "adsb_hex":"a1c0de",
            "flight":"N2119T",
            "lat":38.195772,
            "lon":-122.280171,
            "altitude":900,
            "track":115,
            "speed":89,
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
![Data Flow](https://github.com/guycole/mellow-hyena/blob/main/src/uat_collect/uat_data_flow.png)