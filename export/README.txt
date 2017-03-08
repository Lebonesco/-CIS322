


To export all of the data from the lost database into csvs within the "file" directory held in the root run:


./export_data.sh lost ../files

export_data.sh: shell script that calls exportCSV.py and passes in table names

exportCSV.py: takes in table names and outputs csvs with data
