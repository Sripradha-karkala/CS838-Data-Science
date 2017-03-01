import os 
import fnmatch
import re
import string
import rules
import random
import argparse


def random_pick(inputs, seed):
	random.seed(seed)
	tokens = []
	for i in range(1500):
		rand = random.randint(0, len(inputs)-1)
		tokens.append(inputs[rand])
	return tokens

def appendToArff(data, filename):
        arffFile = open(filename, 'a')
        for i in range(0, len(data)):
                for j in range(0, (len(data[i])-1)):
                        arffFile.write(str(data[i][j]) + ',')
                arffFile.write(str(data[i][j+1]) + '\n')
        arffFile.close()


def generate_neg_tokens(file_path):
	# Parse through each file to generate tokens
	tokens = []
	state_names = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
          'Alabama','Alaska','Arizona','Arkansas','California','Colorado',
         'Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho', 
         'Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana',
         'Maine' 'Maryland','Massachusetts','Michigan','Minnesota',
         'Mississippi', 'Missouri','Montana','Nebraska','Nevada',
         'New Hampshire','New Jersey','New Mexico','New York',
         'North Carolina','North Dakota','Ohio',    
         'Oklahoma','Oregon','Pennsylvania','Rhode Island',
         'South Carolina','South Dakota','Tennessee','Texas','Utah',
         'Vermont','Virginia','Washington','West Virginia',
         'Wisconsin','Wyoming']
	 
	# Get all the words from a file 
	# This basically takes every line in the file 
	# and splits it based on space and gives a single list of words
	with open(file_path) as f:
		lines = f.read().splitlines()
		for line in lines:
			# Now scan the word list to find valid tokens as negative examples
			# Here we are just checking for max 2 word length, hence inspecting 
			# two words at a time
			words = line.split()
			for index in range(len(words)-1):
				# Rule 1: If enclosed by <city></city> discard it 
				if re.search('<city>.*</city>', words[index]):
					continue

				# If the word is completely in upper case, then add it 
				if words[index].isupper():
					tokens.append([line, words[index]])
					continue

				# At this point the word is in camel case
				# Rule 2: Check if the word is united states - country name
				if (words[index]+words[index+1]).lower() == 'unitedstates':
					tokens.append([line, words[index]+' '+words[index+1]])
					continue

				#Rule 4: If the word or the two words are state name, then add it to negative example
				name_1 = words[index].translate(None, string.punctuation+string.whitespace)
				name_2 = words[index+1].translate(None, string.punctuation+string.whitespace)
				if name_1.upper() in (name.upper() for name in state_names):
					tokens.append([line, words[index]])
					continue

				if (name_1+' '+name_2).upper() in (name.upper() for name in state_names):
					tokens.append([line, words[index]+' '+words[index+1]])
					continue

	return tokens

if __name__== '__main__':

	'''
		This script generates the negative tokens for 
		generating the arff file

		Usage: python gen_neg_tokens.py -f path/to/directory/with/data -o path/to/output/file -s seed

		-f : Take the path to the input directory where the training/test data exists
		-o : Path to where the output file must be generated
		-s: Seed for randomly picking a set of negative tokens, set to 34 for now

		Uses the rules.py file to generate the feature vectors
		and append to the arff file.

	'''

	#Parse command line arguments
	parser = argparse.ArgumentParser(description='Generate negative tokens and append the fv to arff')
	parser.add_argument('-f', dest='filePath', help='The full path to the training/test documents')
	parser.add_argument('-o', dest='outputFile', help='Path to the output arff file')
	parser.add_argument('-s', dest='seed', help='Seed for randomly picking negative token')
	args = parser.parse_args()

	if not args.filePath or not args.outputFile or not args.seed:
		parser.print_help()
		exit()

	if not args.outputFile.endswith('.arff'):
		print u'Incompatible format. File must be of type *.arff'
		exit()

	trainDocDir = args.filePath
	inputs = []
	data = []

	for filename in os.listdir(trainDocDir):
		# Iterate over all the text documents in it

		if fnmatch.fnmatch(filename, '*.txt'):
			value = generate_neg_tokens(trainDocDir+filename)
			inputs.extend(value)

	inputs = random_pick(inputs,args.seed)
	for value in inputs:
		nfv = rules.generateFV(value, False)
		data.append(nfv)

	#append to arff file
	if (len(data) == 0):
		print "No text files or tags present"
	else:
		#append to an arff file
		appendToArff(data, args.outputFile)
