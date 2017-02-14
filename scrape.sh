#! /bin/bash

conferences=( ovc mvfc )
years=( 2008 2009 2010 2011 2012 2013 2014 2015 2016 )

for conference in "${conferences[@]}"
do
  input=data/$conference.csv

  for year in "${years[@]}"
  do
    if [ ! -d "data/$year/$conference" ]; then
      mkdir -p data/$year/$conference
    fi
  done


  [ ! -f $input ] && { echo "$input file not found"; exit 99; }
  while IFS=, read source destination
  do
    if [ ! -f "$destination" ]; then
      fifthdown scrape $source > $destination
      echo $destination created.
    fi
  done < $input
done
