#!/bin/bash

(
cd sql
psql lost -f create_table.sql
./import_data.sh lost 5432
)
