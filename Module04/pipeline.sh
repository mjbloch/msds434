#!/bin/bash

rm -r *.csv

bash download.sh 2015 02

cp 201502.csv 201502.bck

rm *.csv

python3 trim.py

gsutil -m cp *.csv gs://msds434-week-4-demo

bq load --autodetect --source_format=CSV msds434_demo.flight_auto gs://msds434-week-4-demo/201502.csv