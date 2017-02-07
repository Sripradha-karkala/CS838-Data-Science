import csv
import argparse
import os
import datetime

# Generated a directory called text 
# and adds all the documents in it
# the 0th document is just the header of the CSV

#usage: textDocGen.py [-h] [-f FILEPATH [FILEPATH ...]]
#                     [-D DIRECTORY [DIRECTORY ...]]

#Convert CSV to text docs

#optional arguments:
#  -h, --help            show this help message and exit
#  -f FILEPATH [FILEPATH ...]
#                        Provide the filename - full path
#  -D DIRECTORY [DIRECTORY ...]
#                        Directory Name for output files

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Convert CSV to text docs')
	parser.add_argument('-f', dest='filePath', help='Provide the filename - full path')
	parser.add_argument('-D', dest='directory', help='Directory Name for output files')
	args = parser.parse_args()

	if not args.filePath or not args.directory:
		parser.print_help()
		exit()

	reader = csv.reader(open(args.filePath))
	directoryName = args.directory+'-'+str(datetime.datetime.now())
	# Create a directory named text for storing all docs
	os.makedirs(directoryName)
	# counter for autogenerating sequence of file
	counter = 0;
	for line in reader:
		f = open(directoryName+'/textDoc'+str(counter)+'.txt', 'a+')
		for feature in line:
			f.write(feature+'\n');
		counter = counter +1
