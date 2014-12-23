(Jan 2012) The entry point into Temoa stochastics is most easily done through
the generate_scenario_tree.py script.  To use it, one needs 3 items in place:

* a stochastic version of the Temoa model.  This is generally the same as the
  LP version of the Temoa model, with two changes: the objective function, and
  a single constraint to tie the objective function to individual stages of
  the stochastic model.

* a reference data file.  Temoa generally calls data files "dot dat" files,
  and as long as the LP version of Temoa can run it, then it can serve as a
  reference data file.  If you've used Pyomo's PySP before, then note that
  this file will become ReferenceModel.dat to the PySP scripts.

* an options.py file.  The options.py is a little lengthy to describe here,
  but is fairly self explanatory if you are aware of what PySP needs.
  Generally, the options.py file describes the branches of the nodes in the
  stochastic event tree, including the "names" of each branch, the conditional
  probabilities of each branch, which parameters and indexes to vary and by
  how much.  There are examples of options.py files in the subdirectory
  options/.


An example interaction might be:

$ pyomo_python generate_scenario_tree.py options/utopia_coal_vs_nuc.py
[  0.00] Setting up working directory (utopia_demand)
[  0.01] Import model definition (../temoa_model/temoa_model.py)
[  0.37] Create concrete instance (../data_files/utopia-15.dat)
[  0.37] Collecting stochastic points from model (TEMOA Entire Energy System Economic Optimization Model)
[  0.38] Building tree:                        91
[  0.41] Writing scenario "dot dat" files:     91
[  0.41] Copying ReferenceModel.dat as scenario tree root

When the script is complete, the directory, in this case 'utopia_demand', will
have 91 "dot dat" files, each representing a different node in a scenario tree.

To run the stochastic tree just generated:

$ cd utopia_demand
$ runef -m ../../temoa_model --verbose
[... and away PySP will go ...]

Please also note that this is still preliminary; if it doesn't immediately work
as "advertised", please don't get angry.  Get helpful.
