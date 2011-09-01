energysystem-process-Coopr3 is the current active branch of the
Temoa project.  Any changes to our model will see birth in this
branch before being moved to our trunk.

To run this model, you can either:

$ pyomo temoa_model  path/to/dat/file

  or

$ coopr_python  temoa_model  path/to/dat/file

 or

$ ./create_archive.sh
$ ./temoa_model.py  path/to/dat/file

The first uses Pyomo through Coopr's scripts, while the latter two
options are maintained by the Temoa developers and presents a more
easily read output.  The latter is also how to gain access to some
of the external features, like Graphviz.  For general help use
--help:

$ coopr_python  temoa_model  --help

Or for specific examples:

$ coopr_python  temoa_model  --graph_format svg  path/to/dat/file
$ coopr_python  temoa_model  --graph_format pdf  path/to/dat/file

