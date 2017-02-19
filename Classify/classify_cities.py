# Classification of city names given an *.arff using cross-validation 
# (kfolds) in sci-kit learn
# Classifiers: Decision trees, random forest, support vector machine, 
# logistic regression, linear regression
# TODO: Debug linear regression
# TODO: Aggregate results of cross validation splits
# TODO: Write ouputs to file
# TODO: Consider adding city names to arff for debugging
# TODO: Create visualization for decision tree

import argparse
import scipy as sp
import numpy as np
import pandas as pd
from scipy.io import arff
from sklearn import preprocessing
from sklearn import tree, svm, linear_model 
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split, KFold
from sklearn.ensemble import RandomForestClassifier

# Set number of features
N_FEATURES = 8

# String symbols for formatting
dashes = '-'*25
stars = '*'*30

# Run cross validation on models and print the 
# precision, recall, f1, and support for each fold
def crossValidate(model):
	kf = KFold(4)
	for k, (train, test) in enumerate(kf.split(x, y)):
		model.fit(x[train], y[train])
		prediction = model.predict(x[test])

		# Write results to file
		print(dashes + 'Fold' + str(k) + dashes)
		target_names = ['Not City', 'City']
		print(classification_report(prediction, y[test], target_names=target_names))

# Setup the classifiers 
def evaluateModels(x, y):
	names = ['Decision Tree', 
			'Random Forest Classifier',
			'SVM',
			'Logistic Regression',
			#'Linear Regression'
			]

	models = [tree.DecisionTreeClassifier(),
			 RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
			 svm.SVC(),
			 linear_model.LogisticRegression(),
			 #linear_model.LinearRegression()
			 ]

	for name, model in zip(names, models):
		print(stars + name + stars)
		crossValidate(model)

# Main Program
if __name__ == '__main__':
	# Parse command line arguments
	parser = argparse.ArgumentParser(description='Classify citys from an arff file')
	parser.add_argument('-f', dest='filePath', help='The full path of the arff')
	args = parser.parse_args()

	if not args.filePath:
		parser.print_help()
		exit()

	if not args.filePath.endswith('.arff'):
		print("Incompatible format. File must be of type *.arff")
		exit()

	# Convert arff to numpy array
	data, meta = arff.loadarff(args.filePath)

	# Convert numpy list of tuples to pandas
	dataFrame = pd.DataFrame(data).astype(int)

	# Randomly split data into train and final test
	dev, finalTest = train_test_split(dataFrame, test_size = 0.33)

	# Separate features and labels for development set
	features = list(dev.columns[:N_FEATURES])
	x = dev[features].values
	y = dev['Class'].values

	# Train on dev set
	evaluateModels(x,y)
	


