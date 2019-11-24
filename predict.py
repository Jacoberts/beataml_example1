"""A script which executes an drug repurposing model on input files.

Expects:
  /model/: should have pkl_1.csv and pkl_2.csv
  /input/: should have rnaseq.csv and input.csv

Creates:
  /output/aucs.csv: a CSV with columns ['inhibitor', 'lab_id', 'auc']
"""

import util


if __name__ == "__main__":
  util.RunPredictions('/model', '/input', '/output')
