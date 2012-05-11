energysystem_process_match_MARKAL is a branch of energysystem_process.  This branch houses the necessary changes to the Temoa model to match MARKAL's results
against the Utopia model.

To run this model, you can either:

$ pyomo  temoa_model  utopia-markal-15.dat

  or

$ coopr_python  temoa_model  utopia-markal-15.dat

The first uses Pyomo through Coopr's scripts, while the latter
option is maintained by the Temoa developers and presents more
easily read output.  The latter is also how to gain access to some
of the external features, like Graphviz.  For general help use
--help:

$ coopr_python  temoa_model  --help

Or for specific examples:

$ coopr_python  temoa_model  --graph_format svg  utopia-markal.dat
$ coopr_python  temoa_model  --graph_format pdf  utopia-markal.dat

List of files
=============
utopia-markal-15.dat  -  A copy of the Utopia system with 15-year vehicle lives
utopia-markal-20.dat  -  A copy of the Utopia system with 20-year vehicle lives

compare_with_utopia-*.py - Create ODF spreadsheets for "prettier" comparisons.
