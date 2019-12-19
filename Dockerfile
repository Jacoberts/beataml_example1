# Inherit from Jupyter Docker Stacks so we have all the data processing
# tools we may ever need already imported.
FROM python:3.7

RUN pip3 install numpy pandas

WORKDIR /

COPY model model
COPY predict.py .
COPY util.py .

ENTRYPOINT ["python3", "predict.py"]

