energysystem-process-match-MARKAL is a branch of
energysystem-process-Coopr3.  It the necessary changes to the
-Coopr3 model to make Temoa match MARKAL's results against the
Utopia model.

To run this model, you can either:

$ pyomo temoa_model utopia-markal.dat

  or

$ coopr_python  temoa_model  utopia-markal.dat

The first uses Pyomo through Coopr's scripts, while the latter
option is maintained by the Temoa developers and presents more
easily read output.  The latter is also how to gain access to some
of the external features, like Graphviz.  For general help use
--help:

$ coopr_python  temoa_model  --help

Or for specific examples:

$ coopr_python  temoa_model  --graph_format svg  utopia-markal.dat
$ coopr_python  temoa_model  --graph_format pdf  utopia-markal.dat

