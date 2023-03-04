import json
import xml.etree.ElementTree as ET
from math import cos, radians, sin
import random
import math


tree = ET.parse('allrelation3.xml')

nodeDB = dict()
wayDB = dict()
relationDB = dict()

for elem in tree.getroot():
	if (elem.tag == "node"):
		node_details = elem.attrib
		nodeDB[node_details['id']] = node_details
	elif (elem.tag == "way"):
		way_id = elem.attrib['id']
		way_user = elem.attrib['user']
		wayDB[way_id] = dict()
		wayDB[way_id]['user'] = way_user
		wayDB[way_id]['coord'] = []
		for i in elem:
			if (i.tag == "nd"):
				nodeID = i.attrib['ref']
				coord = [nodeDB[nodeID]['lon'],nodeDB[nodeID]['lat']]
				wayDB[way_id]['coord'].append(coord)
	elif (elem.tag =="relation"):
		relation_id = elem.attrib['id']
		relation_user = elem.attrib['user'] 
		relationDB[relation_id] = dict()
		relationDB[relation_id]['user'] = relation_user
		relationDB[relation_id]['ways'] = []
		isNamed = False
		for i in elem:
			if ((i.tag == "tag") and (i.attrib['k'] == "name")):
				relationDB[relation_id]['name'] = i.attrib['v']
				isNamed = True
			elif (i.tag == "member") and (i.attrib['type'] == "way"):
				relationDB[relation_id]['ways'].append(wayDB[i.attrib['ref']]['coord'])
		if not isNamed:
			relationDB.pop(relation_id)


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
		