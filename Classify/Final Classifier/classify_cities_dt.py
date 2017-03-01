"""
Decision Tree for classify strings as city/non-cities

"""

import argparse
import numpy as np
import pandas as pd
from scipy.io import arff
from sklearn import tree, svm
from sklearn.metrics import classification_report
from sklearn.utils import shuffle

# Class labels
labels = ['Not City', 'City']

# Output filename
fout = 'decision_tree_report.txt'
dotFile = 'tree.dot'

def separateFeaturesClass(filePath):
	"""
	Extract the features and classes from an *.arff file

	Input
	------
	filePath
		string path of *.arff file

	Output
	-------
	list in format [x, y, features] where
		x is a list of feature tuples
		y is a list of class labels
		features is a list of the names of the features
	"""
	# Convert arff to numpy array
	data, meta = arff.loadarff(filePath)

	# Convert numpy list of tuples to pandas
	dataFrame = pd.DataFrame(data).astype(int)

	# Shuffle data
	dataFrame = shuffle(dataFrame)

	# Separate features and labels
	features = list(dataFrame.columns[:-1])

	x = dataFrame[features].values
	y = dataFrame['Class'].values

	return [x, y, features]

# Main Program
if __name__ == '__main__':
	"""
	Compare classifiers for sorting strings into city/non-city classes

	Input
	-----
	trainPath
		Path to training data in *.arff format

	testPath
		Path to test data in *.arff format

	Output
	-------
	text file
		Summary of precision, recall, f1, and support for each classifier

	dot file
		Graphic of decision tree

	Example Usage
	-------------
	>>> python classify_cities.py -train cityTrain.arff -test cityTest.arff

	"""
	# Parse command line arguments
	parser = argparse.ArgumentParser(description='Classify citys from an arff file')
	parser.add_argument('-train', dest='trainPath', help='The full path of the training data arff')
	parser.add_argument('-test', dest='testPath', help='The full path of the test data arff')
	args = parser.parse_args()

	if not (args.trainPath and args.testPath):
		parser.print_help()
		exit()

	if not (args.trainPath.endswith('.arff') and args.testPath.endswith('.arff')):
		print u'Incompatible format. File must be of type *.arff'
		exit()

	xDev, yDev, features = separateFeaturesClass(args.trainPath)
	xTest, yTest, features = separateFeaturesClass(args.testPath)
	
	# Train decision tree on dev set
	dt = tree.DecisionTreeClassifier()

	dt.fit(xDev, yDev)

	prediction = dt.predict(xTest)
	
	# Write results to fout
	f = open(fout, 'w')
	f.write(classification_report(yTest, prediction, target_names=labels))
	f.close()

	# Make a pretty decision tree graphic
	# Convert *.dot to *.png using the following command
	# (must have pydot package installed)
	# >>> dot -Tpng tree.dot -o tree.png
	dot_data = tree.export_graphviz(dt, out_file=dotFile,
	feature_names=features,
	class_names=labels)

