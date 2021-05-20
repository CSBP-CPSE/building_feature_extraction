#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import csv
import matplotlib.pyplot as plt

def get_city():
	#this method currently only returns Ottawa but in future implimentations might get the city based off the address
	return "Ottawa"

def get_province():
	#this method currently only returns Ottawa but in future implimentations might get the city based off the address
	return "Ontario"

def concatenate_address(file):
	d = dict()
	f = open(file)
	next(f)
	for line in f:
		line = line.strip('\n')
		(osm_obj_type, latitude, longitude, addr_unit, addr_house, addr_street, building) = line.split(",")
		addr=""
		if addr_unit:
			addr = addr_unit +" "
		addr = addr+addr_house + " " + addr_street + ", " + get_city() + ", " + get_province()
		if(addr in d and d[addr][0] != building):
			d[addr][0] = d[addr][0] + ", " + building
		else:
			d[addr] = [building, osm_obj_type, latitude, longitude]



	with open('dict.csv', 'w', newline='') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(["building_address", "building_type", "osm_obj_type", "latitude", "longitude"])
		for addr in d:
			writer.writerow([addr, d[addr][0], d[addr][1], d[addr][2], d[addr][3]])

def create_type_files(file):
	with open(file) as fin:    
	    csvin = csv.DictReader(fin)
	    # Category -> open file lookup
	    outputs = {}
	    for row in csvin:
	        cat = row['building_type']
	        # Open a new file and write the header
	        if "," in cat:
	        	cat = "unknown"

	        if cat not in outputs:
	            fout = open('{}.csv'.format(cat), 'w', newline='')
	            dw = csv.DictWriter(fout, fieldnames=csvin.fieldnames)
	            dw.writeheader()
	            outputs[cat] = fout, dw
	        # Always write the row
	        outputs[cat][1].writerow(row)
	    # Close all the files
	    for fout, _ in outputs.values():
	        fout.close()
	    fin.close()

def type_histogram(file):
	df = pd.read_csv(file)
	#data.plot(kind='bar')
	#plt.ylabel('Amount in the Ottawa Region')
	#plt.xlabel('Residential Building Types')
	#plt.title('Residential Buildings in the Ottawa Region per type')

	
	df.loc[df['building_type'].str.contains(','), 'building_type'] = 'unknown'
	df["building_type"].hist()
	plt.show()



concatenate_address("addresses_inside_polygon.csv")
create_type_files("dict.csv")
type_histogram("dict.csv")

