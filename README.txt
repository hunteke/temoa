This branch named 'energysystem' is the current "main" branch of the 
Temoa Project.  The four subdirectories are:

1. temoa_model/
This contains the Temoa model code.

2. data_files/
The example input data (DAT) files for Temoa. Note that the file 
'utopia-15.dat' represents a simple system called 'Utopia', which 
is packaged with the MARKAL model generator and has been used 
extensively for benchmarking exercises.

3. stochastic/
Scripts for generation of PySP event trees.

4. docs/
The ReST documentation source of the Temoa project manual.

***Running Temoa***

To run Temoa, you have a few options.

Option 1 uses Pyomo's own scripts and provides basic solver output:

$ pyomo  temoa_model/temoa_model.py  path/to/dat/file

Option 2 invokes python directly, and gives the user access to 
additional capability, including more nicely formatted output:

$ python  temoa_model/  path/to/dat/file

Option 3 below copies the relevant Temoa model files into an 
executable archive (this only needs to be done once):

$ python create_archive.py

This makes the model more portable by placing all contents in a 
single file. Now it is possible to execute the model with the 
following simply command:

$ ./temoa.py  path/to/dat/file

For general help use --help:

$ python  temoa_model/  --help

And to place the solution information into a file:

$ python  temoa_model data_files/utopia.dat > temoa_utopia.sol


