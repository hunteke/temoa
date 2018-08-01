-----------------------
Monte Carlo README
-----------------------

The current version of this Monte Carlo script was developed to run the cases 
associated with Eshraghi et al. [1]. The script contains some hard-wired 
elements that need to be fixed to make the code generalizable to other studies.

Running the Monte Carlo script requires the installation of a python library 
called joblib [2]. To minimize the computational time, this library creates 
an embarrassingly parallel implementation of the framework. 

To run the script, run the following from the command line:

$ python Monte-Carlo.py

The Monte-Carlo.txt file defines the parameter ranges used in each Monte Carlo simulation.  



References:
[1] Eshraghi, h.; De Queiroz, A, R,; DeCarolis, J, F,; US Energy-Related Greenhouse Gas Emissions in the Absence of Federal Climate Policy, Environmental Science and Technology, 2018
[2] joblib 0.11 : Python Package Index, https://pypi.python.org/pypi/joblib