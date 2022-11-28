import geopy
from geopy.distance import distance


# given: lat1, lon1, b = bearing in degrees, d = distance in kilometers
def coord_calc_lat(lat1, lon1, d, b):
    lat2, lon2, _ = distance(kilometers=d).destination((lat1, lon1), b)
    return lat2, lon2


def coord_calc_lon(lat1, lon1, d, b):
    lat2, lon2, _ = distance(kilometers=d).destination((lat1, lon1), b)
    return lat2, lon2


def box_handle(initlat, initlon, filter, distance):
    if filter[0] != 0 or filter[1] != 0:
        if filter[0] < 0:
            b = 270
            latx, lonx = coord_calc_lat(initlat, initlon, abs(filter[0]) * distance, b)
        elif filter[0] > 0:
            b = 90
            latx, lonx = coord_calc_lat(initlat, initlon, abs(filter[0]) * distance, b)
        else:
            latx, lonx =initlat, initlon


        if filter[1] < 0:
            b = 180
            laty, lony = coord_calc_lat(latx, lonx, abs(filter[1]) * distance, b)
        elif filter[1] > 0:
            b = 0
            laty, lony = coord_calc_lat(latx, lonx, abs(filter[1]) * distance, b)
        else:
            laty, lony =latx, lonx

        return laty, lony
    return initlat, initlon
