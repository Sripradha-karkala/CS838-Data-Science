import os
import rules
import fnmatch
import re
from bs4 import BeautifulSoup

def getAttrType(attrName):
	'''if attrName == 'NumOfWords' or attrName == 'AvgWordLength':
		return 'numeric'
	if attrName == 'FirstLetterUppercase' or attrName == 'class':'''
	return '{1, 0}'

def writeToArff(data, attributes):
	arffFile = open('./train_data/city.arff', 'w')
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
	trainDocDir = './train_data/training_docs/'
	attributes = ['FirstLetterUppercase', 'City:',
                    'CommaAfter', 'CommaBefore', 'AfterInkeyword',
                    'CitykeywordAfter', 'AllCapital', 'Class']
	data = []
	for filename in os.listdir(trainDocDir):
		#iterate over labelled txt files
		if fnmatch.fnmatch(filename, '*.txt'):
			print 'working on filename: ', filename
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
								#print 'sliceLine: '
								#print sliceLine
								pfv = rules.generateFV(posExample, True)
								data.append(pfv)
					
					#print pfv
					#data.append(pfv)
		if (len(data) == 0):
			print "No text files or tags present"
		else:
			#create an arff file
			writeToArff(data, attributes)
					
