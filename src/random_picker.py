import random
import shutil
if __name__=='__main__':
	trainDocDir = './train_data/training_docs/'

	test_docs = './test_data/test_docs/'

	i = 100

	while i > 0:  #pick a 100 documents randomly
		rand = random.randint(1, 300)
		try:
			shutil.move(trainDocDir+"textDoc"+str(rand)+".txt", test_docs+"textDoc"+str(rand)+".txt")
		except IOError:
			continue
		i = i-1