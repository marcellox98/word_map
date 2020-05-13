import csv
import sys
import json



def checkKey(dict, key): 
      
    if key in dict.keys(): 
        return True 
    else: 
        return False 

with open('countryrelations.csv', mode='r') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	args = []
	last = 'none'
	_all = {}
	for row in csv_reader:
		if line_count == 0:
			args = row
			line_count += 1
		else:
			i = 0
			relation = {}
			for a in args:
				itm = row[i]
				if itm.replace('.','',1).isdigit():
					itm = float(itm)
				if itm == "NA":
					itm = False
				relation[a] = itm
				i += 1
			if not checkKey(_all, relation['repifs']):
				_all[ relation['repifs'] ] = {}
			_all[ relation['repifs'] ][ relation['parifs'] ] = relation
			print("\r parsedline %i" % line_count, end='\r', flush=True)
			line_count += 1
	print("Processed %i lines. writing now" % line_count)

	for name in _all:
		f = open("relations/%s.json" % name , "w+")
		print("\r new item %s" % name, end='\r', flush=True)
		f.write(json.dumps(_all[name]))

	