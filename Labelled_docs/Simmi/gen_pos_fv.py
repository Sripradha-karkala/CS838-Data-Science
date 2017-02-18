import os
import fnmatch
from bs4 import BeautifulSoup

def getAttrType(attrName):
	if attrName == 'NumOfWords' or attrName == 'AvgWordLength':
		return 'numeric'
	if attrName == 'FirstLetterUppercase' or attrName == 'class':
		return '{True, False}'

def writeToArff(data, columns):
	arffFile = open('./train_data/city.arff', 'w')
	arffFile.write('@relation ' + 'cities' + '\n')
	for col in columns:
		arffFile.write('@attribute ' + col + ' ' + str(getAttrType(col)) + '\n')
	arffFile.write('@data' + '\n')
	for i in range(0, len(data)):
		for j in range(0, (len(data[i])-1)):
			arffFile.write(str(data[i][j]) + ',')
		arffFile.write(str(data[i][j+1]) + '\n')	
	
	arffFile.close()


def applyRules(ruleName, cityName):
	if ruleName == 'NumOfWords':
		#print 'first rule'
		return len(cityName.split())
	if ruleName == 'FirstLetterUppercase':
		#print 'second rule'
		return cityName[0].isupper()
	if ruleName == 'AvgWordLength':
		#print 'third rule'
		return len(cityName)
	if ruleName == 'class':
		#print 'class rule'
		return True

def createPositiveFeatureVector(cityName, columns):
	fv = []
	for cols in columns:
		fv.append(applyRules(cols, cityName))
	#print fv
	return fv
	

if __name__ == '__main__':
	trainDocDir = './train_data/training_docs/'
	columns = ['NumOfWords', 'FirstLetterUppercase', 'AvgWordLength', 'class']
	data = []
	for filename in os.listdir(trainDocDir):
		#iterate over labelled txt files
		if fnmatch.fnmatch(filename, '*.txt'):
			with open(trainDocDir+filename) as markup:
				soup = BeautifulSoup(markup.read())
				for cityName in soup.find_all('city'):
					#print cityName.text
					pfv = createPositiveFeatureVector(cityName.text, columns)
					data.append(pfv)
		if (len(data) == 0):
			print "No text files or tags present"
		else:
			#create an arff file
			writeToArff(data, columns)
					
