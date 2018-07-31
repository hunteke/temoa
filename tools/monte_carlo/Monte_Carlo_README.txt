-----------------------
Monte Carlo README
-----------------------

The 3 Monte Carlo simulations performed in [1], require installing a python library called joblib [2]. To minimize the computational time, this library creates an embarrassingly parallel implementation of the framework. 
To run the Uncertain World, Uncertain Fuels and Stable World cases, type the following commands (A detailed description of the three Monte Carlo cases is provided in [1]):
Uncertain World: $ python Monte-Carlo-UW.py
Uncertain Fuels: $ python Monte-Carlo-UF.py
Stable Worlds: $ python Monte-Carlo.py

There are also three .txt files that define the ranges used in each Monte Carlo cases.  


References:
1. Eshraghi, h.; De Queiroz, A, R,; DeCarolis, J, F,; US Energy-Related Greenhouse Gas Emissions in the Absence of Federal Climate Policy, Environmental Science and Technology, 2018
2. joblib 0.11 : Python Package Index, https://pypi.python.org/pypi/joblib