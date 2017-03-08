
To import correctly formated data from csvs, located in the "files" directory, into the lost database run:

./import_data.sh lost ../files


import_data.sh: calls exportCSV.py and passes in database name, port, and file directory

gen_insert.py: python program that inserts the csvs into the database
