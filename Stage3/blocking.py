import pandas as pd
import os, sys
import logging
from os.path import expanduser
import argparse
import py_entitymatching as em

'''
The program takes as input the two structured dataset 
path_A and path_B .

The datasets are down sampled and blocking methods are used 
for reducing the size of the datasets.

Input
===================
path_A : path to the first structured dataset
path_B : path to the second structured dataset

Output
============================
Generates a downsized blocked sample dataset

'''

  # Add command line arguments for path to files
parser = argparse.ArgumentParser()
parser.add_argument('path_A', help='Path to the left table', type=str)
parser.add_argument('path_B', help='Path to the right table', type = str)
args = parser.parse_args()

# Set up logger
logging.basicConfig()

# Set paths
path_A = args.path_A
path_B = args.path_B

A = em.read_csv_metadata(path_A)

em.set_key(A, 'id')

# Read and set metadata for table B
B = em.read_csv_metadata(path_B, key='id')

print('Number of tuples in A: ' + str(len(A)))
print('Number of tuples in B: ' + str(len(B)))
print('Number of tuples in A X B (i.e the cartesian product): ' + str(len(A)*len(B)))

ob = em.OverlapBlocker()

tup1 = A.ix[76687]

tup2 = B.ix[232514]

# Apply blocking to a tuple pair from the input tables on artists name and get blocking status
status = ob.block_tuples(tup1, tup2, 'artist_name', 'artists')
print(status)

# Apply blocking to a tuple pair from the input tables on artists and get blocking status
status = ob.block_tuples(A.ix[0], B.ix[0], 'artist_name', 'artists')
print(status)

sample_A, sample_B = em.down_sample(A, B, 15000, 1.5, show_progress=True, verbose=True)


stop = ['de', 'del', 'du', 'of', 'la', 'le']

for word in stop:
    ob.stop_words.append(word)

ob.stop_words


C1 = ob.block_tables(sample_A, sample_B, 'artist_name', 'artists', rem_stop_words=True, word_level=True, overlap_size=2, l_output_attrs=['id', 'title', 'artist_name', 'year'], r_output_attrs=['id', 'title', 'year', 'episode', 'song', 'artists'], show_progress=True)

print ('Number of tupes of blocking tables:' + str(len(C1)))

S = em.sample_table(C1, 450)

# Set path for sampled data to label
path_label = 'sample.csv'

S.to_csv(path_label)

D = ob.block_candset(C1, 'title', 'song', rem_stop_words=True, verbose=True)

G = em.label_table(D, 'gold')

