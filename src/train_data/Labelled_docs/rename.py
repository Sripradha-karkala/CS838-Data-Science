import os
import sys
import fnmatch

if __name__ == '__main__':
	start = sys.argv[1]
	print "start label number" + start
	for filename in os.listdir('.'):
		#iterate over labelled txt files
		if fnmatch.fnmatch(filename, '*.txt'):
			os.rename(filename, 'textDoc'+str(start)+'.txt')
			start = int(start)+1	
