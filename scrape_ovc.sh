#! /bin/bash

INPUT=data/ovc.csv
mkdir data/ovc

[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while IFS=, read source destination
do
  fifthdown scrape $source > $destination
  echo $destination created.
done < $INPUT
