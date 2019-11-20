#! /bin/bash

# Try running the Dockerfile on the data in training/.

if [[ $# -ne 1 ]];
then
  echo "Format is $0 <Dockerfile home>"
  exit 2
fi


echo "Mounting $1/training as input and $1/output for outputs."

docker build -t beataml .
docker run -v "$PWD/training/:/input/" -v "$PWD/output:/output/" beataml

