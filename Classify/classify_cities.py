"""Compare classifiers that classify strings as city or non-cities 

Sklearn classifiers used: Decision trees, random forest, support vector machine, 
logistic regression, linear regression
"""

# TODO: Debug linear regression--currently using ridge regression

import argparse
import numpy as np
import pandas as pd
from scipy.io import arff
from sklearn import tree, svm, linear_model 
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle

# Set number of folds for cross-validation
N_FOLDS = 10

# Name of output file
fout = 'city_classification_report.txt'


def reportScores(precision, recall, fscore, support):
	# Modification of sklearn's classification report:
	# https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/metrics/classification.py
	"""
	Calculate StratifiedKFold averages

	Parameters
	----------
	precision, recall, fscore, support: list of lists 

	Returns
	-------
	string
		Text summary of the precision, recall, F1 score for each class
	"""
	# Calculate mean for each metric and store as list of lists
	results = []
	for measure in [precision, recall, fscore, support]:
		mean = np.average(measure, axis=0, weights=support)
		results.append(mean)

	p, r, f1, s = results

	# Row and column labels
	headers = ["Precision", "Recall", "F1", "Support"]
	labels = ["Not City", "City", "Avg/Total"]
	
	# Precision for formatting results
	digits = 3

	# Format columns
	width = max(len(label) for label in labels)
	head_fmt = u'{:<{width}s} ' + u' {:<9}' * len(headers)
	report = head_fmt.format(u'', *headers, width=width)
	report += u'\n'

	# Format rows
	row_fmt = u'{:<{width}s} ' + u' {:<9.{digits}f}' * 3 + u' {:<9.0f}\n'
	rows = zip(labels, p, r, f1, s)
	for row in rows:
		report += row_fmt.format(*row, width=width, digits=digits)

	# Add averages for all classes
	report += row_fmt.format(labels[-1],
                             np.average(p, weights=s),
                             np.average(r, weights=s),
                             np.average(f1, weights=s),
                             np.sum(s),
                             width=width, digits=digits)
	
	report += u'\n'
	return report


def crossValidate(model, x, y):
	"""
	Trains models and runs StratifiedKFold cross validation

	Parameters
	----------
	model
		classifier to train
	x
		feature vectors
	y
		labels

	Returns
	-------
	string
		Text summary of the precision, recall, F1 score for each class
	"""
	# Create lists to store results from each fold
	precision, recall, fscore, support = ([] for i in range(4))

	kf = StratifiedKFold(N_FOLDS)
	for k, (train, test) in enumerate(kf.split(x, y)):
		model.fit(x[train], y[train])
		prediction = model.predict(x[test])

		p, r, f1, s = score(y[test], prediction)
		precision.append(p)
		recall.append(r)
		fscore.append(f1)
		support.append(s)

	# Return metric report for average of folds
	return reportScores(precision, recall, fscore, support)
		

def evaluateModels(x, y):
	"""
	Setup classifiers to train and compare

	Parameters
	----------
	x
		feature vectors
	y
		labels

	Returns
	-------
	string
		Report of average precision, recall, F1 score for each classifier trained
	"""
	names = ['Decision Tree', 
			'Random Forest Classifier',
			'SVM',
			'Logistic Regression',
			'Linear (Ridge) Regression'
			]

	models = [tree.DecisionTreeClassifier(),
			 RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
			 svm.SVC(),
			 linear_model.LogisticRegression(),
			 linear_model.RidgeClassifier(alpha=0)
			 ]

	output = ''
	for name, model in zip(names, models):
		output += name + u'\n' 
		output += crossValidate(model, x, y)
	
	return output

# Main Program
if __name__ == '__main__':
	"""
	Compare classifiers for sorting strings into city/non-city classes

	Input
	-----
	arff file
		Feature vectors with labels

	Output
	-------
	text file
		Summary of precision, recall, f1, and support for each classifier

	Example Usage
	-------------
	>>> python classify_cities.py -f 'city.arff'

	"""
	# Parse command line arguments
	parser = argparse.ArgumentParser(description='Classify citys from an arff file')
	parser.add_argument('-f', dest='filePath', help='The full path of the arff')
	args = parser.parse_args()

	if not args.filePath:
		parser.print_help()
		exit()

	if not args.filePath.endswith('.arff'):
		print u'Incompatible format. File must be of type *.arff'
		exit()

	# Convert arff to numpy array
	data, meta = arff.loadarff(args.filePath)

	# Convert numpy list of tuples to pandas
	dataFrame = pd.DataFrame(data).astype(int)

	# Shuffle data
	dataFrame = shuffle(dataFrame)

	# Separate features and labels
	features = list(dataFrame.columns[:-1])

	x = dataFrame[features].values
	y = dataFrame['Class'].values

	# Train on dev set
	output = evaluateModels(x, y)
	
	# Write results to fout
	f = open(fout, 'w')
	f.write(output)
	f.close()




