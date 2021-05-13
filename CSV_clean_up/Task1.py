#Task 1
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
		writer.writerow(["Building_Address", "Building_type"])
		for addr, building in d.items():
			writer.writerow([addr, building])

concatenate_address("script_1_input.csv")