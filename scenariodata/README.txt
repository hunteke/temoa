README: generate_scenario_tree.py explanation
==============================================================================

To use the generate script, you need to specify which parameters to
vary in a stochastic fashion, and how to vary them.  The pertinent
command line parameters you need to specify:

--params=...
 Expects a comma separated list of model parameters to vary.  An
 example usage might be

  --params=power_dmd,energy_dmd,co2_tot

--stage-types=...
 Name of the possible decisions are each stochastic stage.  You need
 to specify this parameter for every model parameter you specify with
 --params.  The format is <param_name>:<decision_names>.  An example
 that works with the above --params might be

  --stage-types=power_dmd:Low,Med,High \
  --stage-types=energy_dmd:SuperEfficient,Efficient,Average,Wasteful \
  --stage-types=co2_tot:BusinessAsUsual,Improved

--stage-rates=...
 The percentage of change associated with each decision for a given
 parameter.  Like it's sister parameter, stage-rates must be
 specified for each parameter in the CSV list given to --params.
 Additionally, the number of percentages must match the number of
 types listed for each parameter.  In effect this is the "important"
 parameter, but --stage-types is the human readable name, and are
 also added as comments to each "dot dat" file.  An example to match
 with above might be

  --stage-rates=power_dmd:0.85,1.00,1.15 \
  --stage-rates=energy_dmd:0.75,0.90,1.10,1.18 \
  --stage-rates=co2_tot:1.25,0.90

Finally, the script writes all the stage node parameter files to
R_*.dat files and the ScenarioStructure.dat output to stdout.  In
addition, it also writes informational messages to stderr.  This
means that to create a ScenarioStructure.dat file, one runs the
script with an output redirection:

$ R.dat R_*.dat ScenarioStructure.dat | wc -l
/bin/ls: R.dat: No such file or directory
/bin/ls: R_*.dat: No such file or directory
/bin/ls: ScenarioStructure.dat: No such file or directory
0  # the wc command produced this count of files

$ ./generate_scenario_tree.py ... > ScenarioStructure.dat
Import model definition from ReferenceModel: done.
Create concrete instance from ReferenceModel.dat: done.
Collecting stochastic points (periods) from the model: done.
Building tree: .............done.
Writing scenario "dot dat" files: .............done.
Copying ReferenceModel.dat to R.dat (the scenario tree root): done.

$ ls R.dat R_*.dat ScenarioStructure.dat | wc -l
14    # the wc command now shows 14 files, 13 R*.dat files +1 structure file.

Putting it all together, this certainly makes for an ugly command line:

$ ./generate_scenario_tree.py  --params=power_dmd,energy_dmd,co2_tot  --stage-types=power_dmd:Low,Med,High  --stage-types=energy_dmd:SuperEfficient,Efficient,Average,Wasteful  --stage-types=co2_tot:BusinessAsUsual,Improved  --stage-rates=power_dmd:0.85,1.00,1.15  --stage-rates=energy_dmd:0.75,0.90,1.10,1.18  --stage-rates=co2_tot:1.25,0.90 > ScenarioStructure.dat

Or, in a perhaps more readable version, making use of backslash line
continuation:

$ ./generate_scenario_tree.py  \
  --params=power_dmd,energy_dmd,co2_tot  \
  --stage-types=power_dmd:Low,Med,High  \
  --stage-rates=power_dmd:0.85,1.00,1.15  \
  --stage-types=energy_dmd:SuperEfficient,Efficient,Average,Wasteful  \
  --stage-rates=energy_dmd:0.75,0.90,1.10,1.18  \
  --stage-types=co2_tot:BusinessAsUsual,Improved  \
  --stage-rates=co2_tot:1.25,0.90  \
  > ScenarioStructure.dat

This is an early alpha of this script, so if you have more ideas,
please do send them my way (hunteke, earlham, edu)
