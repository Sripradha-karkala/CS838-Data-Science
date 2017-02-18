# posExExtractor.py
# Extracts feature vectors from *.txt files in cwd
# Use with Python3

# TODO: save features as numpy array/spicy sparse matrix
# TODO: add beforeState and other important feature vectors
# TODO: add directory path arg to commandline prompt
import os
import re

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
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

# Feature 1: Is Capitalized
def isCapitalized(str):
	return 1 if str[0].isupper() else 0

# Feature 2: Is followed by State
def isState(str):
	return 1 if str in states else 0

# Feature 3: Is followed by a comma
def commaAfter(str, i):
	nextChar = str[i:i+1]
	return 1 if nextChar == ',' else 0

# Feature 4: Is preceded by a comma and space
def commaBefore(str, i):
	prevChars = str[i-2:i]	
	return 1 if prevChars == ', ' else 0

# Feature 5: Is preceded by "City:" with any amount of whitespace
def cityBefore(str, i, item):
	words = str.split()
	prevChars = str[:i]
	#print(prevChars)
	pattern = re.compile(r'City:\s*<city>%s'%item)
	return 1 if re.search(pattern, str) else 0

# Extract feature vectors from one file
def extractFeatures(filename):
	f = open(filename, 'r')

	pattern = re.compile(r'<city>(.*?)</city>')

	for line in f:
		for match in re.finditer(pattern, line):
			for item in match.groups():
				start = match.start()
				end = match.end()

				print(filename,
					item, 
					isCapitalized(item), 
					isState(item), 
					commaAfter(line, end), 
					commaBefore(line, start),
					cityBefore(line, start, item))
				
	f.close()

# Main program: Extract feature vectors from text files 
# in current working directory
if __name__ == '__main__':
	for filename in os.listdir(os.getcwd()):
		if filename.endswith('.txt'):
			extractFeatures(filename)
