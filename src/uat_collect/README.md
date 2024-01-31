mellow-hyena/uat_collect
=========================

## Introduction
Python script to read json from [dump978](https://github.com/mutability/dump978) and produce a json formatted file.  Runs from cron every minute and exits.  Eventually the output files will be moved to AWS S3 for later processing.


## Bill Of Materials
1. Raspberry Pi 3 w/power supply
1. RTL-SDR w/antenna

## dump1090
stuff

### dump978 installation

https://github.com/mutability/dump978.git

rtl_sdr -f 978000000 -s 2083334 -g 48 - | ./dump978 | ./uat2text



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
