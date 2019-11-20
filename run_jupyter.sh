#! /bin/bash

if [[ $# -ne 1 ]];
then
  echo "Format is $0 <working directory to mount>"
  exit 2
fi


echo "Mounting $1 as the code directory."

docker run -p 8888:8888 -v "$1:/home/jovyan" jupyter/scipy-notebook
