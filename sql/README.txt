FILE INFORMATION:

create_tables.sql: 

SQL to create the lost database tables

import_data.sh:

shell scrip that downloads legacy data and accepts 2 arguments(database name, port)

gen_insert.py:

gets called by import_data.sh. Grabs downloaded legacy data and places into database.
