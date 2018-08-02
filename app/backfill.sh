#!/bin/bash

if [ ! -f authors.csv   ]; then
    echo "Downloading authors.csv ..."
    curl -o authors.csv http://s2-interview.s3-website-us-west-2.amazonaws.com/authors.csv  
fi


if [ ! -f papers.csv   ]; then
    echo "Downloading paper.csv ..."
    curl -o papers.csv http://s2-interview.s3-website-us-west-2.amazonaws.com/papers.csv
fi

python backfill.py