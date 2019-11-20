# Inherit from Jupyter Docker Stacks so we have all the data processing
# tools we may ever need already imported.
FROM jupyter/scipy-notebook

WORKDIR /

COPY model model
COPY predict.py .
COPY util.py .

ENTRYPOINT ["python3", "predict.py"]

