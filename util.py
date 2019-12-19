"""Utilities for training and running the model."""

from itertools import product
import os

import numpy
import pandas


def TransposeRnaSeqTable(rnaseq):
  """Convert the RnaSeq table, indexed by gene, to be indexed by specimen."""
  rnaseq.index = rnaseq.Gene
  return rnaseq[rnaseq.columns[2:]].T


def GetPickledModelState(pkl_1_path, pkl_2_path):
  """Fetches (pkl_1, pkl_2) from storage."""
  pkl_1 = pandas.read_csv(pkl_1_path).set_index('gene', drop=False)
  pkl_2 = pandas.read_csv(pkl_2_path).set_index('inhibitor')
  return (pkl_1, pkl_2)


def NormSpecimens(specimens):
  normed_specimens = specimens.apply(
      lambda specimen : specimen / numpy.linalg.norm(specimen), axis=1)
  return normed_specimens


def Predict(inhibitor, normed_specimen, pkl_1, pkl_2):
  """Uses the pickled model to predict the AUC for the specimen."""
  z_scores = (normed_specimen[pkl_1.gene] - pkl_1.gene_mean) / pkl_1.gene_std
  return z_scores.dot(pkl_1[inhibitor]) + pkl_2.loc[inhibitor].intercept


def RunPredictions(model_dir, input_dir, output_dir):
  print('Loading data...')
  (pkl_1, pkl_2) = GetPickledModelState(
      os.path.join(model_dir, 'pkl_1.csv'),
      os.path.join(model_dir, 'pkl_2.csv'))
  specimens = TransposeRnaSeqTable(
      pandas.read_csv(os.path.join(input_dir, 'rnaseq.csv')))
  normed_specimens = NormSpecimens(specimens)

  print('Getting the cartesian product of inhibitors and specimens...')
  inhibitors = pkl_2.index
  specimens = normed_specimens.index
  aucs = pandas.DataFrame(
      product(inhibitors, specimens),
      columns=['inhibitor', 'lab_id'])

  print('Predicting per-specimen AUC...')
  aucs['auc'] = aucs.apply(lambda r: (
    Predict(r['inhibitor'], normed_specimens.loc[r['lab_id']], pkl_1, pkl_2)),
    axis=1)
  aucs.to_csv(os.path.join(output_dir, 'predictions.csv'), index=False)
