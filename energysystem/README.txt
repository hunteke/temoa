This branch of code is based on Temoa's code repository branch
"energysystem-process-Coopr3".  Any changes to this code will be
tested in that branch before moving here, making this our "stable"
branch.

To run this model, you can either:

$ pyomo  temoa_model  path/to/dat/file

  or

$ coopr_python  temoa_model  path/to/dat/file

 or

$ ./create_archive.sh
$ ./temoa_model.py  path/to/dat/file

The first uses Coopr's scripts to run our model, while the latter
two options are maintained by the Temoa developers and present a
more easily read output.  The latter is also how to gain access to
some of the external features, like Graphviz.  For general help use
--help:

$ coopr_python  temoa_model  --help

Or for specific examples:

$ coopr_python  temoa_model  --graph_format svg  path/to/dat/file
$ coopr_python  temoa_model  --graph_format pdf  path/to/dat/file

