#!/bin/bash

db_name=$1
port=$2


downLoadFiles="curl -o files.tar.gz https://classes.cs.ureogon.edu/17W/cis322/project.php/files/osnap_legaacy.tar.gz"

echo "unzipping legacy data\n"
echo "$downLoadFiles"
echo "gzip -d files.tar.gz"
echo "tar xvf files.tar"

echo "python gen_insert.py > insert.sql"

