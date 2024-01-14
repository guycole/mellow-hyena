import math

EPSILON = 1e-6
PI_HALF = math.pi/2.0
PI_TWO = math.pi*2.0

ROE_KILOMETERS = 6371.009
ROE_NAUTICAL_MILES = 3440.065
ROE_STATUTE_MILES = 3958.756

def range_and_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> (float, float):
    """great circle range and bearing between two points"""

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    csn1, csn2, cst1, cst2 = map(math.cos, [lon1, lon2, lat1, lat2])
    snn1, snn2, snt1, snt2 = map(math.sin, [lon1, lon2, lat1, lat2])

    range = csn1*cst1*csn2*cst2 + snn1*cst1*snn2*cst2 + snt1*snt2
    range = math.acos(range)

    xx = -csn1*snt1*csn2*cst2 - snn1*snt1*snn2*cst2 + cst1*snt2
    yy = -snn1*csn2*cst2 + csn1*snn2*cst2
    bearing = math.atan2(yy, xx)
    if bearing < 0.0:
        bearing = bearing + PI_TWO

    return (range * ROE_NAUTICAL_MILES, math.degrees(bearing))
