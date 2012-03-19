NOTE: This branch is close to obsolete.  It has not been
significantly developed since mid-2010, and does not work with
current versions of Coopr.  You may be more interested in the
energysystem_process branch.

Summary
-------------------------------
This file provides the basic usage info for our electric sector
energy model.  This directory contains prototype U.S. Electricity
Sector model.  Detailed documentation is available from the project
website (http://temoaproject.org).

The model specification is done using Pyomo (developed at Sandia
National labs).

Prerequisites
-------------------------------
* Python (2.6 or later)
* COOPR (COmmon Optimization Python Repository) : developed at Sandia National labs https://software.sandia.gov/trac/coopr/
* GNU Linear Programming Kit (GLPK)

Run
-------------------------------
Just use
"pyomo elc.py elc.dat"

