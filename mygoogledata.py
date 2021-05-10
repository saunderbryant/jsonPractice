import json
from datetime import datetime
from geopy import distance
import matplotlib.pyplot as plt
import ijson
import gmplot

#Declare variables latitude, longitude, distance from home
lat = []
long = []
timestamp = []
dist_from_home = []
loc_point = []
home_location = (-76.738350, 38.972150)
#filename = open('loc1to1000.json')
filename = open('locationdata.json')

def coord_to_float(coordinate: int):
    """Takes a coordinate int as input, converts to string and adds a decimal point and returns a float"""
    coordinate = str(coordinate)
    if coordinate[0] == '-':
        coordinate = coordinate[:3] + '.' + coordinate[3:]
    else:
        coordinate = coordinate[:2] + '.' + coordinate[2:]
    return (float(coordinate))

#Define the Json iterator function using ijson
objects = ijson.items(filename, 'locations.item')
temp_coord = []
last_coord = []
temp_timestamp = []
for o in objects:
    temp_lat = coord_to_float(o["latitudeE7"])
    temp_long = coord_to_float(o["longitudeE7"])
    temp_timestamp = int(o["timestampMs"])


    if abs(temp_lat) > 90.0 or abs(temp_long) > 90.0:
        print(lat[-1], long[-1])
        print(temp_lat,temp_long)
        break
    #print(temp_lat, temp_long)
    if len(lat) == 0:
        lat.append(temp_lat)
        long.append(temp_long)
        timestamp.append(temp_timestamp)
    else:
        temp_coord = [temp_long, temp_lat]
        last_coord = [long[-1], lat[-1]]
        if distance.distance(temp_coord, last_coord).miles > 0.1:
            lat.append(temp_lat)
            long.append(temp_long)
            timestamp.append(temp_timestamp)
        else:
            pass

#Calculate the distance of each data point from home. Store distance values in list
for i in range(0, len(lat)):
    loc_point = [long[i], lat[i]]
    dist_from_home.append(distance.distance(home_location, loc_point).miles)
    #Debug printing statement for distance from home
    print(str(dist_from_home[i]) + ' miles from home.')

# TODO: Convert timestamp to readable date

#Plot list of data points on a graph to see how far I typically travel from home
plt.plot(list(range(0,len(lat))), dist_from_home)
plt.title("Distance From Home", fontsize=24)
plt.xlabel("Location Point", fontsize=12)
plt.ylabel("Miles From Home", fontsize=12)
plt.tick_params(axis='both', labelsize=14)
plt.show()

