
import py_entitymatching as em
import pandas as pd
import os, sys
import logging
from os.path import expanduser
import argparse


def get_metrics(metric):

  # Select the best ML matcher using CV
  result = em.select_matcher([dt, rf, svm, ln, lg, nb], table=H, 
          exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'],
          k=5,
          target_attr='gold', metric=metric, random_state=0)
  
  print (result['cv_stats'])

def train(models):
    for model in models:
        # Train using feature vectors from I 
        model.fit(table=H, 
        exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'], 
        target_attr='gold')

        # Convert J into a set of feature vectors using F
        L = em.extract_feature_vecs(J, feature_table=feature_table,
                            attrs_after='gold', show_progress=False)

        # Predict on L 
        predictions = model.predict(table=L, exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'], 
              append=True, target_attr='predicted', inplace=False)
        
        # Evaluate the predictions
        print ('Predictions of ' + model.name + ' on J')
        eval_result = em.eval_matches(predictions, 'gold', 'predicted')
        em.print_eval_summary(eval_result)
        print ('\n\n')

'''
The program takes as input the two structured dataset 
path_A and path_B and a csv file for labelled samples.

The labelled dataset is fed to various ML models
to determine the best matcher. 

Input
===================
path_A : path to the first structured dataset
path_B : path to the second structured dataset
path_G : path to the labelled dataset

Output
============================
Reports the precision and accuracy for the labelled dataset [train, test]

'''
if __name__=='__main__':
    # Add command line arguments for path to files
  parser = argparse.ArgumentParser()
  parser.add_argument('path_A', help='Path to the left table', type=str)
  parser.add_argument('path_B', help='Path to the right table', type = str)
  parser.add_argument('path_G', help='Path to the labelled dataset', type =str)
  args = parser.parse_args()

  # Set up logger
  logging.basicConfig()

  # Set paths
  path_A = args.path_A
  path_B = args.path_B
  path_G = args.path_G

  # Read csv file
  A = em.read_csv_metadata(path_A)
  em.set_key(A, 'id')
  # Read and set metadata for table B
  B = em.read_csv_metadata(path_B, key='id')


  # Get the types of the columns and set the correspondense
  atypes1 = em.get_attr_types(A)
  atypes2 = em.get_attr_types(B)

  block_c = em.get_attr_corres(A,B)

  block_c['corres'] = [
   ('id', 'id'),
   ('title', 'song'),
   ('year', 'year'),
   ('artist_name', 'artists')]


  tok = em.get_tokenizers_for_blocking() 

  sim = em.get_sim_funs_for_blocking()

  G = em.read_csv_metadata(path_G, 
                           key='_id',
                           ltable=A, rtable=B, 
                           fk_ltable='ltable_id', fk_rtable='rtable_id', encoding = 'UTF-8')

  # Split D into development set (I) and evaluation set (J)
  IJ = em.split_train_test(G, train_proportion=0.7, random_state=0)
  I = IJ['train']
  J = IJ['test']


  # Create a set of ML-matchers
  dt = em.DTMatcher(name='DecisionTree', random_state=0)
  svm = em.SVMMatcher(name='SVM', random_state=0)
  rf = em.RFMatcher(name='RF', random_state=0)
  lg = em.LogRegMatcher(name='LogReg', random_state=0)
  ln = em.LinRegMatcher(name='LinReg')
  nb = em.NBMatcher(name='NaiveBayes')

  print ('Generating features for I...')
  # Generate features
  feature_table = em.get_features(A, B, atypes1, atypes2, block_c, tok, sim)

  print ('Extracting feature vectors for I...')
  # Convert the I into a set of feature vectors using F
  H = em.extract_feature_vecs(I, 
                              feature_table=feature_table, 
                              attrs_after='gold',
                              show_progress=True)

  print ('Getting results for I')

  get_metrics('precision')
  get_metrics('recall')
  get_metrics('f1')


  # Create a set of ML-matchers
  dt = em.DTMatcher(name='DecisionTree', random_state=0)
  svm = em.SVMMatcher(name='SVM', random_state=0)
  rf = em.RFMatcher(name='RF', random_state=0)
  lg = em.LogRegMatcher(name='LogReg', random_state=0)
  ln = em.LinRegMatcher(name='LinReg')
  nb = em.NBMatcher(name='NaiveBayes')


  models = [dt, svm, rf, lg, ln, nb]


  print ('Printing results of the test set J')
  train(models)



