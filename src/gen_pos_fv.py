import os
import rules
import fnmatch
import re
from bs4 import BeautifulSoup
import argparse

def getAttrType(attrName):
	return '{1, 0}'

def writeToArff(data, attributes, filename):
	arffFile = open(filename, 'w')
	arffFile.write('@relation ' + 'cities' + '\n')
	for attr in attributes:
		arffFile.write('@attribute ' + attr + ' ' + str(getAttrType(attr)) + '\n')
	arffFile.write('@data' + '\n')
	for i in range(0, len(data)):
		for j in range(0, (len(data[i])-1)):
			arffFile.write(str(data[i][j]) + ',')
		arffFile.write(str(data[i][j+1]) + '\n')	
	
	arffFile.close()

if __name__ == '__main__':


	#Parse command line arguments
	parser = argparse.ArgumentParser(description='Generate negative tokens and append the fv to arff')
	parser.add_argument('-f', dest='filePath', help='The full path to the training/test documents')
	parser.add_argument('-o', dest='outputFile', help='Path to the output arff file')
	args = parser.parse_args()

	if not args.filePath or not args.outputFile:
		parser.print_help()
		exit()

	if not args.outputFile.endswith('.arff'):
		print u'Incompatible format. File must be of type *.arff'
		exit()


	trainDocDir = args.filePath
	attributes = ['FirstLetterUppercase', 'StateAfter', 'City:',
                    'CommaAfter', 'CommaBefore', 'AfterInkeyword',
                    'CitykeywordAfter', 'AllCapital', 'Class']
	data = []
	for filename in os.listdir(trainDocDir):
		#iterate over labelled txt files
		if fnmatch.fnmatch(filename, '*.txt'):
			with open(trainDocDir+filename, 'r') as f:
					pattern = re.compile(r'<city>(.*?)</city>')
					for line in f:
						sliceLine = line
						for match in re.finditer(pattern, line):
							for item in match.groups():
								keyword = item
								start = match.start()
								end = match.end()
								posExample = [sliceLine, keyword]
								sliceLine = line[end:]
								pfv = rules.generateFV(posExample, True)
								data.append(pfv)
		if (len(data) == 0):
			print "No text files or tags present"
		else:
			#create an arff file
			writeToArff(data, attributes, args.outputFile)
					
