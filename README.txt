NOTE: This branch currently does not work.  It was our initial attempt at a
simple electric-sector optimization system.  If warranted, an interested party
should be able to revitalize this branch without too much effort.

Given that the energysystem_process branch is both current, and could implement
an electric-sector only system, why would one want to revitalize this? It might
be a good "get up to speed" project, including an introduction to coding with
Coopr/Pyomo.  It also will be slightly more efficient than the more general
energysystem_process code.

Prerequisites
-------------------------------
* Python 2.7 (v2.6 will not work, and Coopr can't yet use v3+)
* COOPR (COmmon Optimization Python Repository) : developed at Sandia National labs https://software.sandia.gov/trac/coopr/
* A solver.  We suggest the freely available GNU Linear Programming Kit (GLPK)

Run
-------------------------------
Just use
"pyomo elc.py elc.dat"
