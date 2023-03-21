import os
import sys
import json

import xmltodict

CWD = os.getcwd()
INPUT_FILE_LOCATION = "data/collections.xml"
OUTPUT_FILE_LOCATION = "data/collections.xml"

def runner(infile, outfile):
	"""
	Run this script from the project root directory.
	Example: python parser/parse.py data/collections.xml data/collections.json
	"""
	with open(os.path.join(CWD, infile), 'r') as xml:
		xml_as_dict = xmltodict.parse(xml.read())
		xml_as_json = json.dumps(xml_as_dict)
		with open(os.path.join(CWD, outfile), 'w') as f:
			f.write(xml_as_json)
			f.close()
		xml.close()

if __name__ == '__main__':
	if len(sys.argv) > 2:
		INPUT_FILE_LOCATION = sys.argv[1]
		OUTPUT_FILE_LOCATION = sys.argv[2]

	runner(INPUT_FILE_LOCATION, OUTPUT_FILE_LOCATION)
