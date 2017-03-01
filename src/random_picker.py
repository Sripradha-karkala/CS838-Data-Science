import random
import shutil
import argparse

if __name__=='__main__':

	parser = argparse.ArgumentParser(description='Generate random set of training and testing documents')
	parser.add_argument('-t', dest='trainPath', help='The full path to the training directory')
	parser.add_argument('-te', dest='testPath', help='The full path to the testing directory')
	trainDocDir = trainPath

	test_docs = testPath

	i = 100

	while i > 0:  #pick a 100 documents randomly
		rand = random.randint(1, 300)
		try:
			shutil.move(trainDocDir+"textDoc"+str(rand)+".txt", test_docs+"textDoc"+str(rand)+".txt")
		except IOError:
			continue
		i = i-1