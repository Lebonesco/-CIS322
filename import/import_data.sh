#1 /usr/bin/bash

DB_NAME=$1
INPUT_DIR=$2
PORT=5432
HOST="/tmp"
echo "Importing data from $INPUT_DIR"
python gen_insert.py $DB_NAME $PORT $INPUT_DIR
