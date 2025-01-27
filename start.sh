#!/bin/bash
app="docker.test"
docker build -t ${app} .
docker build -t docker.test .
# docker run -d --name invoice-matching-container -p 56733:80 docker.test
docker run -d -p 56733:80 \
  --name=${app} \
  -v $PWD:/app ${app}