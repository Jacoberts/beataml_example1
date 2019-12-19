# BeatAML CTD^2 DREAM Challenge: Example 1

Example implementation of a solution to subchallenge 1 of the BeatAML CTD^2 DREAM challenge. This example uses gene expression to train a RidgeRegression model for each inhibitor to predict AUC.

## To Train a model

- Run Jupyter with `docker run -p 8888:8888 -v "$PWD:/home/jovyan" jupyter/scipy-notebook`
  - Stdout will include a URL to open the notebook
- Go through the steps in `index.ipynb`
  - The model will be stored in `model/` in two files: `pkl_1.csv` and `pkl_2.csv`
  - Read more about the model [below](#the_model)

## To Run Your Model on Training Data

This model can be run on the same data it was trained on, to test whether the Dockerfile works:

```bash
SYNAPSE_PROJECT_ID=<...>
docker build -t docker.synapse.org/$SYNAPSE_PROJECT_ID/sc1_model .
docker run -v "$PWD/training/:/input/" -v "$PWD/output:/output/" docker.synapse.org/$SYNAPSE_PROJECT_ID/sc1_model 
```

## Submitting to Synapse DockerHub

```bash
SYNAPSE_PROJECT_ID=<...>
docker login docker.synapse.org
docker build -t docker.synapse.org/$SYNAPSE_PROJECT_ID/sc1_model .
docker push docker.synapse.org/$SYNAPSE_PROJECT_ID/sc1_model
```

## The Model

One Ridge Regression model is trained for each inhibitor to predict AUC. The only input is gene expression (rnaseq.csv).

Specifics:

* The 1000 most variable genes are used for training
* The log2(cpm) values are normalized per-specimen
* The z-score is computed for each gene
* Ridge Regression is trained using hold-one-out cross-validation to predict AUC

### On-Disk Representation

The trained model is stored in two "pickles": pkl_1 and pkl_2:

- pkl_1: has one row per gene included in the model and N+3 columns (N is the number of inhibitors):
  - gene: Include this gene's expression in the linear fit.
  - gene_mean: The mean expression in the training data (to compute z-score).
  - gene_std: The standard deviation of expression in the training data (to compute z-score).
  - <inhibitor>: The Ridge Regression weight coefficient for this gene for `inhibitor`.
- pkl_2: one row per inhibitor and two columns:
  - inhibitor: The inhibitor name.
  - intercept: The Ridge Regression intercept.
