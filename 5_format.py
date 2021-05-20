#!/usr/bin/env python
# coding: utf-8

import csv


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
		(addr_house, addr_street, building) = line.split(",")
		addr = addr_house + " " + addr_street + ", " + get_city() + ", " + get_province()
		if(addr in d):
			d[addr] = d[addr] + ", " + building
		else:
			d[addr] = building

	with open('dict.csv', 'w', newline='') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(["building_address", "building_type"])
		for addr, building in d.items():
			writer.writerow([addr, building])

concatenate_address("addresses_inside_polygon.csv")


with open('dict.csv') as fin:    
    csvin = csv.DictReader(fin)
    # Category -> open file lookup
    outputs = {}
    for row in csvin:
        cat = row['building_type']
        # Open a new file and write the header
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
