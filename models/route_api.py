__author__='jx'
from geopy.distance import great_circle

def isWithNKilometers(src_lat,src_lng,kilo,lat,lng):
    src_destination = (float(src_lat),float(src_lng))
    destination = (float(lat),float(lng))
    #print "&&&&&&&&&"
    #print kilo
    distance = great_circle(src_destination, destination).kilometers
    #print distance
    if distance >= float(kilo):
        return False
    else:
        print "&&&&&&&&&"
        print distance
        return True


src_lat=41.49008
src_lng=-71.312796

lat=41.499498
lng=-81.695391

kilo=3000

print isWithNKilometers(src_lat,src_lng,kilo,lat,lng)

