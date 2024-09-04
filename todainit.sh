#!/bin/bash
PWD=`pwd`

for CONTAINER in dbt gitsync ; do
    cd docker/${CONTAINER}
    docker build --tag toda-${CONTAINER} .
    cd ${PWD}
done    