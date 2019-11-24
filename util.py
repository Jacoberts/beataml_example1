"""Utilities for training and running the model."""

import os

import numpy
import pandas


def TransposeRnaSeqTable(rnaseq):
  """Convert the RnaSeq table, indexed by gene, to be indexed by specimen."""
  rnaseq.index = rnaseq.Gene
  return rnaseq[rnaseq.columns[9:]].T


def GetPickledModelState(pkl_1_path, pkl_2_path):
  """Fetches (pkl_1, pkl_2) from storage."""
  pkl_1 = pandas.read_csv(pkl_1_path).set_index('gene', drop=False)
  pkl_2 = pandas.read_csv(pkl_2_path).set_index('parameter')
  return (pkl_1, pkl_2)


def PredictForSpecimen(specimen, pkl_1, pkl_2):
  """Uses the pickled model to predict the GRD for the specimen."""
  normed = specimen / numpy.linalg.norm(specimen)
  z_scores = (normed[pkl_1.gene] - pkl_1.gene_mean) / pkl_1.gene_std
  return z_scores.dot(pkl_1.fit) + pkl_2.loc['intercept'].value


def RunPredictions(model_dir, input_dir, output_dir):
  print('Loading data...')
  (pkl_1, pkl_2) = GetPickledModelState(
      os.path.join(model_dir, 'pkl_1.csv'),
      os.path.join(model_dir, 'pkl_2.csv'))
  specimens = TransposeRnaSeqTable(
      pandas.read_csv(os.path.join(input_dir, 'rnaseq.csv')))

  print('Predicting AUCs for each specimen...')
  specimen_to_auc = (specimens
      .apply(lambda spec: PredictForSpecimen(spec, pkl_1, pkl_2), axis=1)
      .rename('auc'))

  print('Joining per-specimen AUC with specimens in the input file...')
  aucs = (
      pandas.read_csv(os.path.join(input_dir, 'input.csv'))
      .join(specimen_to_auc, on='lab_id'))
  aucs.to_csv(os.path.join(output_dir, 'predictions.csv'), index=False)
