This branch, energysystem_process, is the current "main" branch of the Temoa
Project.  The four subdirectories are:

1. temoa_model/
  This contains the Temoa model code.

2. data_files/
  The example data files that exemplar input to Temoa.

3. stochastic/
  Some (perhaps useful) scripts for generation of PySP event trees.

4. docs/
  The ReST documentation source of the Temoa project manual.

To run Temoa, you can either:

$ pyomo  temoa_model/temoa_model.py  path/to/dat/file

  or

$ coopr_python  temoa_model/  path/to/dat/file

  or

$ ./create_archive.sh
$ ./temoa.py  path/to/dat/file

The first uses Pyomo through Coopr's scripts, while the latter two options are
maintained by the Temoa developers and presents a more easily read output.  The
latter is also how to gain access to some of the external features, like
Graphviz.  For general help use --help:

$ coopr_python  temoa_model  --help

Or for specific examples:

$ coopr_python  temoa_model  --graph_format svg  data_files/utopia.dat
$ coopr_python  temoa_model  --graph_format pdf  data_files/utopia.dat

And to place the gobs of solution information into a file:

$ coopr_python  temoa_model \
  --graph_format svg \
  data_files/utopia.dat > temoa_utopia.sol


If you are running Coopr from Windows, you may have more luck with a direct
python command:

\> python  temoa_model  --graph_format svg  data_files\utopia.dat > temoa_utopia.sol
