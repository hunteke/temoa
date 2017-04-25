This branch named 'energysystem' is the current main branch of the 
Temoa Project.  The four subdirectories are:

1. temoa_model/
Contains the core Temoa model code.

2. data_files/
Containd simple input data (DAT) files for Temoa. Note that the file 
'utopia-15.dat' represents a simple system called 'Utopia', which 
is packaged with the MARKAL model generator and has been used 
extensively for benchmarking exercises.

3. tools/
Contains scripts used to conduct sensitivity and uncertainty analysis. 
See README inside this folder for more information.

4. docs/
Contains the source code for the Temoa project manual, in reStructuredText
(ReST) format.

***Running Temoa***

To run Temoa, you have a few options.

Option 1 (full-featured):
Invokes python directly, and gives the user access to 
several model features via a configuration file:

$ python  temoa_model/  --config=temoa_model/config_sample

Running the model with a config file allows the user to (1) use a sqlite 
database for storing input and output data, (2) create a formatted Excel 
output file, (3) return the log file produced during model execution, 
(4) return the lp file utilized by the solver, and (5) to execute modeling-
to-generate alternatives (MGA).


Option 2 (basic):
Uses Pyomo's own scripts and provides basic solver output:

$ pyomo solve --solver=<solver> temoa_model/temoa_model.py  path/to/dat/file

This option will only work with a text ('DAT') file as input. 
Results are placed in a yml file within the top-level 'temoa' directory.


Option 3 (basic +): 
Copies the relevant Temoa model files into an executable archive 
(this only needs to be done once):

$ python create_archive.py

This makes the model more portable by placing all contents in a 
single file. Now it is possible to execute the model with the 
following simply command:

$ ./temoa.py  path/to/dat/file

For general help use --help:

$ python  temoa_model/  --help



