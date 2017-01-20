#!/bin/bash

db_name=$1
port=$2

downLoadFiles="curl -o file.tar.gz https://classes.cs.uoregon.edu/17W/cis322/files/osnap_legacy.tar.gz"

echo "unzipping legacy data\n"
$downLoadFiles
gzip -d file.tar.gz
tar xvf file.tar
rm ./osnap_legacy/.*.csv
python gen_insert.py > insert.sql #run python script to generate insert.sql file
echo "psql $db_name -f insert.sql" #run insert script
#echo "rm insert.sql" #clean up

rm file.tar
rm -R osnap_legacy

