This "database_io" folder contains database files used to manage Temoa input/output data. Included files are:

temoa_schema.sql: This file includes the Temoa database schema. All database tables are defined and remain empty, with the exception of the tables that specify labels. Since some of the tables must be split in particular ways to form the DAT file, we thought it useful to keep the '_label' tables populated.

temoa_schema.sqlite: This is the binary SQLite database file based on 'temoa_schema.sql'.

temoa_utopia.sql: This file utilizes the Temoa database schema to create the Utopia test dataset packaged with the MARKAL model generator. 

temoa_utopia.sqlite: This is the binary SQLite database file based on temoa_utopia.sql.

DB_to_Excel.py: Python script that queries database output tables to create an Excel file containing scenario-specific results.

Make_Graphviz.py: Python script that creates input Graphviz diagram.
