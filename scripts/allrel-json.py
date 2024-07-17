import json
from math import cos, radians, sin
import random
import math


# Load the data from the JSON file
with open('osm_data2.json', encoding='utf-8') as f:
    data = json.load(f)


nodeDB = dict()
wayDB = dict()
relationDB = dict()



for i in data['elements']:
    tt = i['type']
    if tt == "node":
        nodeDB[i['id']] = i

for i in data['elements']:
    tt = i['type']
    if tt == "way":
        wayDB[i['id']] = dict()
        wayDB[i['id']]['coord'] = []
        for j in i['nodes']:
            nodeID = j
            coord = [nodeDB[nodeID]['lon'],nodeDB[nodeID]['lat']]
            wayDB[i['id']]['coord'].append(coord)
for i in data['elements']:
    tt = i['type']
    if tt == "relation":
        name = i['tags'].get('name')
        if name:
            relationDB[i['id']] = dict()
            relationDB[i['id']]['ways'] = []
            relationDB[i['id']]['name'] = name
            for j in i['members']:
                if j['type'] == "way":
                    relationDB[i['id']]['ways'].append(wayDB[j['ref']]['coord'])



def meters_to_lat_lon_displacement(m, origin_latitude):
    lat = m/111111
    lon = m/(111111 * cos(radians(origin_latitude)))
    return [lat, lon]


dis = meters_to_lat_lon_displacement(8,-6.7427408)

def jitter(coord,rand):
    lon = float(coord[0])
    lat = float(coord[1])
    rand_ang = int(360 * rand)
    new_lon = lon + (dis[1] * rand) * cos(rand_ang * math.pi/180)
    new_lat = lat + (dis[0] * rand) * sin(rand_ang * math.pi/180)
    return [new_lon,new_lat]



jitRoute = dict()
for i in relationDB:
    jitRoute[i] = []
    r_factor = random.random()
    if (r_factor < 0.4):
        r_factor = r_factor + 0.4
    newlines = []
    #line level
    for j in relationDB[i]['ways']:
        new = []
        # Coordinate level
        for k in j:
            newy = jitter(k,r_factor)
            new.append(newy)
        newlines.append(new)
    jitRoute[i] = newlines



        
print("var a =")
newdata = {}
newdata['type'] = "FeatureCollection"
newdata['generator'] = "rtnf"
newdata['features'] = []
for i in jitRoute:
    newy = {}
    newy['type'] = "Feature"
    newy['properties'] = {} 
    newy['properties']['name'] = relationDB[i]['name']
    newy['properties']['id'] = i
    newy['geometry'] = {}
    newy['geometry']['type'] = "MultiLineString"
    newy['geometry']['coordinates'] = jitRoute[i]
    newdata['features'].append(newy)

print(json.dumps(newdata))