from langdetect import detect
import argparse
import csv
import re

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Input the merged csv file')
	parser.add_argument('input_file', metavar='N', type=str, nargs='+',
                   help='Merged input file')
	args = parser.parse_args();
	language_counts = {}
	# open a file
	print args.input_file
	#print args
	with open(args.input_file[0], 'r') as csvfile:
		merged_reader = csv.reader(csvfile, delimiter=',')
		for row in merged_reader:
			#replace all the punctuation and special characters
			song_name = re.sub('[^A-Za-z]+', ' ', row[4])
			song_name = song_name.strip(' ')
			if len(song_name) != 0:
				language = detect(song_name)
				if language_counts.has_key(language):
					language_counts[language] = language_counts.get(language) +1
				else:
					language_counts[language] = 1
				#if language != 'en':
					#print song_name, ",", language
			#print song_name, language
	for value in language_counts.items():
		print value[0], value[1]

