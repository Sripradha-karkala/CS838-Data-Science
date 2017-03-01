import sys
import scipy.io.arff as arff
import itertools

def getAttrType(attrName):
		return '{1,0}'

def writeToArff(data, columns):
	arffFile = open('./train_data/city_no_dup.arff', 'w')
	arffFile.write('@relation ' + 'cities' + '\n')
	for col in columns:
		arffFile.write('@attribute ' + col + ' ' + str(getAttrType(col)) + '\n')
	arffFile.write('@data' + '\n')
	for i in range(0, len(data)):
		for j in range(0, (len(data[i])-1)):
			arffFile.write(str(data[i][j]) + ',')
		arffFile.write(str(data[i][j+1]) + '\n')	
	
	arffFile.close()

def remove_duplicates(data):
	data.sort()
	print data
	data_no_dup =  list(data for data,_ in itertools.groupby(data))
	return data_no_dup


if __name__=='__main__':
	filename = sys.argv[1]
	dataset = arff.loadarff(open(filename))

	data, meta = dataset
	#print len(data)

	data_no_dup = remove_duplicates(data)
	#print len(data_no_dup)

	print data_no_dup

	writeToArff(data_no_dup, meta.names())