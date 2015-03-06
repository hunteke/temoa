This "database_io" branch is being used for the development of a database schema that can be used to handle both input and output data for Temoa. Included files are:

temoa_schema.sql: This file includes the Temoa database schema. All database tables are defined and remain empty, with the exception of the tables that specify labels. Since some of the tables must be split in particular ways to form the DAT file, we thought it useful to keep the "_label" tables populated.

temoa_schema.db: This is the actual SQLite DB file based on temoa_schema.sql.

temoa_utopia.sql: This file utilizes the Temoa database schema to create the Utopia test dataset packaged with the MARKAL model generator.

temoa_utopia.db: This is the actual SQLite DB file based on temoa_utopia.sql.

DB_to_DAT.py: Python script queries a database to create a Pyomo-formatted DAT file.

Make_Graphviz.py: Python script that creates input Graphviz diagram.
