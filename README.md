# beataml_example

Example implementation of a CTD^2 BeatAML solution.

## To Train a model

- Put training files in `training/`
  - At least rnaseq.csv, input.csv, aucs.csv
  - These files are described in [the wiki](https://www.synapse.org/#!Synapse:syn20940518/wiki/596265)
- Run Jupyter with `docker run -p 8888:8888 -v "$1:/home/jovyan" jupyter/scipy-notebook`
  - Stdout will include a URL to open the notebook
- Go through the steps in `index.ipynb`
  - The model will be stored in `model/` in two files: `pkl_1.csv` and `pkl_2.csv`
  - Read more about the model [below](#the_model)

## To Run Your Model on Training Data

This model can be run on the same data it was trained on, to test whether the Dockerfile works:

```bash
docker build -t beataml .
docker run -v "$PWD/training/:/input/" -v "$PWD/output:/output/" beataml
```

## Submitting to Synapse DockerHub

```bash
SYNAPSE_PROJECT_ID=<...>
docker login docker.synapse.org
docker build -t docker.synapse.org/$SYNAPSE_PROJECT_ID/baseline_model .
docker push docker.synapse.org/$SYNAPSE_PROJECT_ID/baseline_model
```

## The Model

This is a Ridge Regression model trained on gene expression to predict a specimen's General Response to Drugs (GRD). The GRD is based on the observation that most specimens respond similarly to all inhibitors - they either respond well to all, or respond poorly to all.

Specifics:

* The 1000 most variable genes are used for training
* The log2(cpm) values are normalized per-specimen
* The z-score is computed for each gene
* Ridge Regression is trained using hold-one-out cross-validation to predict GRD per-specimen
* To predict the AUC for a single (speciment lab_id, inhibitor) pair, simply compute the GRD for that lab_id

### On-Disk Representation

The trained model is stored in two "pickles": pkl_1 and pkl_2:

- pkl_1: has one row per gene included in the model, and four columns:
  - gene: Include this gene's expression in the linear fit.
  - gene_mean: The mean expression in the training data (to compute z-score).
  - gene_std: The standard deviation of expression in the training data (to compute z-score).
  - fit: The Ridge Regression weight coefficient for this gene.
- pkl_2: list of scalar valued parameters:
  - intercept: The Ridge Regression intercept.
