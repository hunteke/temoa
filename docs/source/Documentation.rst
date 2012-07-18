=======
Preface
=======

This manual, in both `PDF`_ and `HTML`_ form, is the official documentation of
the Temoa Project.  It describes all functionality of the Temoa model, and
explains the mathematical underpinnings of the implemented equations.

Besides this documentation, there are a couple other sources for Temoa-oriented
information.  The most interactive is the `mailing list`_, and we encourage any
and all Energy Economy Optimization (EEO) related questions.  Publications are
good introductory resources, but are not guaranteed to be the most up-to-date as
information and implementations evolve quickly.  As with many software-oriented
projects, even before this manual, `the code is the most definitive resource`.
That said, please let us know (via the `mailing list`_, or other avenue) of any
discrepancies you find, and we will fix it as soon as possible.

What is Temoa?
--------------

Temoa is an energy-economy optimization (EEO) model.  Briefly, EEO models are
self-consistent frameworks for mathematically optimizing energy flows through a
user-defined energy-system.\ [#eeo_definition]_ One may think of an EEO model as
a "right-from-left" network graph, with a set of energy demands on the right
that must be met by specific energy flows from the system, originating from
energy-sources on the left.

Some of Temoa's specific features are:

   * technology explicit
   * arbitrary model period lengths
   * designed for High Performance Computing
   * written in Python
   * not tied to a particular solver
   * user extendable
   * open source (AGPL)\ [#open_source_realities]_

The word 'Temoa' is actually an acronym for "Tools for Energy Model Optimization
and Analysis."  We do not follow the acronym precisely, however, so the Temoa
Project is in reality a culmination of four (major) pieces of infrastructure:

   * The mathematical model
   * The implemented model (code)
   * Surrounding tools
   * An online presence

Each of these pieces is fundamental to creating a transparent and usable model
with a community oriented around collaboration.


Why Temoa?
----------

In short, because we believe that EEO model analyses should be recreatable by
independent third parties.  The only realistic method to make this happen is to
have a freely available model, and to create an ecosystem of freely shared data
and model inputs.

For the longer explanation, please see "The TEMOA Project: Tools for Energy
Model Optimization and Analysis", by DeCarolis, J.  and Hunter, K.  and
Sreepathi, S.  (2010) (available from `temoaproject.org/`_).  The highlights
boil down to the facts that EEO model-based analyses are impossible to verify,
complex enough as to be non-repeatable without electronic access to **exact**
versions of code *and* data input, and are used to inform large-scale public
policy.  Especially in light of the last point, we believe that EEO model
analyses should be completely open, independently recreatable, and
electronically available.


Conventions
-----------

 * We use the word 'Temoa' somewhat interchangeably to describe the project as a
   whole, as well as the optimization model.  When the context does not make it
   obvious which is meant, we delineate with "Temoa Project" and "Temoa model".

 * Though TEMOA is an acronym for 'Tools for Energy Model Optimization and
   Analysis', we generally use 'Temoa' as a proper noun, and so forgo the need
   for all-caps.  Regardless, either are acceptable, persuant to the needs of
   the situation.

 * In the mathematical notation, we use CAPITALIZATION to denote a container,
   like a set, indexed variable, or indexed parameter.  Sets use only a single
   letter, so we use the lower case to represent an item from the set.  For
   example, :math:`T` represents the set of all technologies and :math:`t`
   represents a single item from :math:`T`.

 * Variables are named V\_VarName within the code to aid readability.  However,
   in the documentation where there is benefit of italics and other font
   manipulations, we elide the 'V\_' prefix.

 * In all equations, we **bold** variables to distinguish them from parameters.
   Take, for example, this excerpt from the Temoa default objective function:

   .. math::
      C_{marginal} & = \sum_{p, t, v \in \Theta_{MC}} \left (
              MC_{p, t, v}
        \cdot R_p
        \cdot \textbf{ACT}_{t, v}
        \right )

   Note that :math:`C_{marginal}` is not bold, as it is a temporary variable
   used for clarity while constructing the objective function.  It is not a
   structural variable and the solver never sees it.

 * Where appropriate, we put the variable on the right side of the coefficient.
   In other words, this is not a preferred form of the previous equation:

   .. math::

      C_{marginal} & = \sum_{p, t, v \in \Theta_{MC}} \left (
              \textbf{ACT}_{t, v}
        \cdot R_p
        \cdot MC_{p, t, v}
        \right )

 * We generally put the limiting or defining aspect of an equation on the right
   hand side of the relational operator, and the aspect being limited or defined
   on the left hand side.  For example, Temoa's mathematical definition of a
   process capacity (eq. :eq:`Capacity`) depends on that process' activity:

   .. math::

          \left (
                  \text{CF}_{t, v}
            \cdot \text{C2A}_{t}
            \cdot \text{SEG}_{s, d}
          \right )
          \cdot \textbf{CAP}_{t, v}
      \ge
          \textbf{ACT}_{p, s, d, t, v}

      \\
      \forall \{p, s, d, t, v\} \in \Theta_{\text{activity}}

 * We use the word 'process' to refer to the tuple of technology and vintage
   (``<t,v>``), when knowing the vintage of a process is not pertinent to the
   context at hand.

 * Mathematical notation:

   * We use the symbol :math:`\mathbb{I}` to represent the unit interval ([0,
     1]).

   * We use the symbol :math:`\mathbb{Z}` to represent "the set of all
     integers."

   * We use the symbol :math:`\mathbb{N}` to represent natural numbers (i.e.,
     integers greater than zero: 1, 2, 3, :math:`\ldots`).

   * We use the symbol :math:`\mathbb{R}` to denote the set of real numbers, and
     :math:`\mathbb{R}^+_0` to denote non-negative real numbers.


Temoa Origin and Pronunciation
------------------------------

While we use 'temoa' as an acronym, it is an actual word in the Nahuatl (Aztec)
language, meaning "to seek something."

One pronounces the word 'Temoa' as "teh", "moe", "uh", like the first part of
the word "Tech", and the last syllable of the word "Shenandoah".


Bug Reporting
-------------

Temoa strives for correctness.  Unfortunately, as an EEO model and software
project there are plenty of levels and avenues for error.  If you spot a bug,
inconsistency, or general "that could be improved", we want to hear about it.

If you are a software developer-type, feel free to open an issue on our `Github
Issue tracker`_\ .  If you would rather not create a Github account, feel free
to let us know the issue on our `mailing list`_\ .


=======
tl;dnr!
=======

For those without patience, this "Too Long; Did Not Read!" section omits many
details, giving only the bare minimum to get up and running with Temoa.

Temoa is built with Sandia National Laboratories' COOPR project, which is in
turn built with Python.  Thus, one must first install these projects:

#. Python v2.7 (http://python.org/)

   * Temoa requires v2.7.  Temoa will not work with v2.6, and Coopr does not
     work with v3+.

#. Linear Program Solver

   * Any solver for which COOPR has a plugin will work.
   * For ease of integration, we recommend the `GNU Linear Programming Kit`_,
     with two caveats:

     #.  The GLPK project does not directly provide a Windows version.  We
         suggest `WinGLPK`_.

     #. For larger data sets you may need to invest in a commercial
        solver.\ [#glpk_presolve]_

#. COOPR (https://software.sandia.gov/trac/coopr)

   * COOPR is a set of Python Optimization libraries.  Temoa mainly uses Pyomo.

After the above 3 items are installed and tested, download both the
`Temoa model`_ and the `example data sets`_.  Then run Temoa from your operating
system's command line interface.  (In the example, lines beginning with the
dollar symbol '``$``' canonically represent a Unix command line.  Windows
prompts will likely end with a right carot '``>``'.)

.. parsed-literal::

   $ **coopr_python  temoa.py  -h**
   usage: temoa.py [-h] [--graph_format GRAPH_FORMAT] [--show_capacity]
                   [--graph_type GRAPH_TYPE] [--use_splines]
                   dot_dat [dot_dat ...]
   [ ... output trimmed for brevity ... ]

   $ **coopr_python  temoa.py  utopia.dat**
   [    0.08] Reading data files.
   [    0.96] Creating Temoa model instance.
   [    1.65] Solving.
   [    1.77] Formatting results.
   Model name: Temoa Entire Energy System Economic Optimization Model
   Objective function value (TotalCost): 35657.0718528
   Non-zero variable values:
        0.578040628071     V_Activity(1990,inter,day,E01,1960)
        0.1445872          V_Activity(1990,inter,day,E31,1980)
   [ ... output trimmed for brevity ... ]


=====================
The Math Behind Temoa
=====================

   To understand this section, the reader will need at least a cursory
   understanding of mathematical optimization.  We omit here that introduction,
   and instead refer the reader to `various`_ `available`_ `online`_ `sources`_.
   The key piece to note is that Temoa eventually relies on a computer, and thus
   needs some concrete pieces of information to produce useful results.  These
   pieces are generally organized into sets, parameters, variables, and equation
   definitions.

The heart of Temoa is a technology explicit energy system optimization model.
It is an algebraic network of linked processes -- understood by the model as a
set of engineering characteristics (e.g. capital cost, efficiency, capacity
factor, emission rates) -- that transform raw energy sources into end-use
demands.  The model objective function minimizes the present-value cost of
energy supply through manipulation of capacity use and installation over time.

.. _simple_system:

.. figure:: images/simple_system2.*
   :align: center
   :alt: A simple energy system, with energy sources on the left and energy
         sinks (end-use demands) on the right.
   :figclass: align-center

   A common visualization of EEO models is a directed network graph, with energy
   sources on the left and end-use demands on the right.  The modeler must
   specify the specific end-use demands to be met, the technologies of the
   system (green boxes), and the inputs and outputs of each (red and green
   arrows).  The blue boxes represent distinct types of energy carriers.

The most fundamental tenet of the model is the understanding of energy flow,
treating all processes as black boxes that take inputs and produce outputs.
Specifically, Temoa does not care about the inner workings of a process, only
its global input and output characteristics.  In this vein, the above graphic
can be broken down into per-process segments.  For example, the coal power plant
takes as input coal and produces electricity, and is subject to various costs
(e.g. marginal cost) and constraints (e.g. efficiency) along the way.

.. graphviz::
   :align: center
   :alt: A single process, with various engineering characteristics.
   :caption: The model does not assign any weight to the input or output
             commodities of a process, just the engineering characteristics for
             use of the process itself.


   digraph coal {
   	rankdir = "LR" ;
   	node [ style="filled", shape="circle" ] ;
   	edge [ arrowhead="vee", labelfontcolor="lightgreen" ] ;

   	coal [ label="coal" ];
   	coal_plant [ shape="none", style="rounded", label=<
   <font color="#666666" face="Helvetica Bold">
   <table border="0" cellborder="0" cellspacing="0">
   	<tr>
   		<td cellpadding="4" align="center" bgcolor="green4"><font color="#ffffff">Process: coal_power_plant</font></td>
   	</tr>
   	<tr><td></td></tr>
   	<tr><td align="left">installed capacity</td></tr>
   	<tr><td align="left">efficiency</td></tr>
   	<tr><td align="left">install cost</td></tr>
   	<tr><td align="left">fixed cost</td></tr>
   	<tr><td align="left">marginal cost</td></tr>
   	<tr><td align="left">emission per unit activity</td></tr>
   	<tr><td align="left">useful life</td></tr>
   	<tr><td align="left">loan life</td></tr>
   	<tr><td align="left">...</td></tr>
   </table>
   </font>> ] ;
   	electricity [ label="electricity" ];

   	coal -> coal_plant [ label="Input, (V_FlowIn)" ];
   	coal_plant -> electricity [ label="Output, (V_FlowOut)"];
   }


The modeler defines the processes and engineering characteristics through an
amalgam of sets and parameters, described in the next few sections.  Temoa then
translates these into variables and constraints that an optimizer may then
solve.

Sets
----

.. _table_set:

.. csv-table:: List of all Temoa sets with which a modeler might interact.  The
             asterisked (\*) elements are automatically derived by the model and
             are not user-specifiable.
   :header: "Set","Temoa Name","Data Type","Short Description"
   :widths: 10, 25, 15, 50

   ":math:`\text{E}`","time_existing",":math:`\mathbb{Z}`","model periods before optimization begins"
   ":math:`\text{H}`","time_horizon",":math:`\mathbb{Z}`","model time scale of interest;"
   ":math:`\text{F}`","time_future",":math:`\mathbb{Z}`","model periods beyond H;"
   ":math:`{}^*\text{P}`","time_optimize",":math:`\mathbb{Z}`","model time periods to optimize; (:math:`(H \cup F) - \text{max}(F)`)"
   ":math:`{}^*\text{V}`","vintage_all",":math:`\mathbb{Z}`","possible tech vintages; (:math:`E \cup P`)"
   ":math:`\text{S}`","time_season","string","seasonal divisions (e.g. winter, summer)"
   ":math:`\text{D}`","time_of_day","string","time-of-day divisions (e.g. morning)"
   ":math:`\text{T}_r`","tech_resource","string","resource extraction techs"
   ":math:`\text{T}_p`","tech_production","string","techs producing intermediate commodities"
   ":math:`{}^*\text{T}`","tech_all","string","all technologies to be modeled; (:math:`T_r \cup T_p`)"
   ":math:`\text{T}_b`","tech_baseload","string","baseload electric generators; (:math:`T_b \subset T`)"
   ":math:`\text{T}_s`","tech_storage","string","storage technologies; (:math:`T_s \subset T`)"
   ":math:`\text{C}_d`","commodity_demand","string","end-use demand commodities"
   ":math:`\text{C}_e`","commodity_emissions","string","emission commodities (e.g. :math:`\text{CO}_\text{2}`, :math:`\text{NO}_\text{x}`)"
   ":math:`\text{C}_p`","commodity_physical","string","general energy forms (e.g. electricity, coal, uranium, oil)"
   ":math:`{}^*\text{C}_c`","commodity_carrier","string","physical energy carriers and end-use demands (:math:`\text{C}_p \cup \text{C}_d`)"
   ":math:`{}^*\text{C}`","commodity_all","string","union of all commodity sets"
   ":math:`\text{I}`","","string","alias of :math:`\text{C}_p`; used in documentation only to mean "input""
   ":math:`\text{O}`","","string","alias of :math:`\text{C}_c`; used in documentation only to mean "output""

Temoa uses two different set notation styles, one for paper and code
representation (e.g. this documentation), and one that attempts to conform to
standard mathematical notation.  For brevity, the mathematical representation
uses capital glyphs to denote sets, and small glyphs to represent items within
sets.  For example, :math:`T` represents the set of all technologies and
:math:`t` represents an item within :math:`T`.

The code and paper representation is more verbose, and in this documentation
will be presented in an italicized font.  The same example of all technologies
is represented in the code as :math:`tech\_all`.  Note that regardless, the
meanings are identical, with only minor interaction differences inherent to
"implementation details."

Their are four basic set "groups" within Temoa: periods, annual "slices",
technology, and energy commodities.  The technological sets contain all the
possible energy technologies that the model may build and the commodities sets
contain all the input and output forms of energy that technologies consume and
produce.  The period and slice sets merit a slightly longer discussion.

Temoa's conceptual model of *time* is broken up into three levels:

 * **Periods** - consecutive blocks of years, marked by the first year in the
   period.  For example, a two-period model might consist of :math:`P = {2010,
   2015}` and :math:`F = {2025}`, and would represent the two periods of years
   from 2010 to 2015, and from 2015 to 2025.

 * **Seasonal** - Each year may have multiple seasons.  For example, winter
   might demand more heating, while spring might demand more cooling and
   transportation.

 * **Daily** - Within a season, a day might have various times of interest.
   For instance, the peak electrical load might occur midday in the summer, and
   a secondary peak might happen in the evening.

There are three specifiable period sets: :math:`time\_exist`,
:math:`time\_horizon`, and :math:`time\_future`.  The :math:`time\_horizon` set
contains the future periods that the model will optimize.  As this set must
contain only integers, Temoa interprets the elements to be the beginning of each
period of interest.  Temoa uses these period boundary years to automatically
calculate the length of each optimization period, enabling a modeler to create
variable period lengths within a model.  (To our knowledge, this capability is
unique to Temoa.)  The :math:`time\_exist` set contains periods before
:math:`time\_horizon`.  Its primary purpose is to specify the vintages for
capacity that exist prior to the model optimization.  (This is Temoa's answer to
what most models model as "residual capacity".)  The :math:`time\_future` set
contains any period beyond the model horizon.  As this set's main use is to to
calculate the final optimization period length, most modelers will supply it
with a single year.  The :math:`time\_optimize` set is the union of
:math:`time\_horizon` and :math:`time\_future`\ [#union]_ and is the time set
most used in the Temoa formulation.

One final note on periods: rather than optimizing each year within a period
individually, Temoa makes a simplifying assumption that each period contains
:math:`n` copies of a single, representative year.  Temoa optimizes just this
characteristic year, and only delineates each year within a period through a
time-value of money calculation in the objective function.  Figure 3.3 gives a
graphical explanation of the annual delineation.

.. _FigureObjectiveComparison:

.. figure:: images/ObjectiveUsageVsCostComparison.*
   :align: center
   :alt: Energy use same each year; time-value of annual costs reduced each year
   :figclass: align-center

   The left graph is of energy, while the right graph is of the annual costs.
   In other words, the energy used in a period by a process is the same for all
   years (with exception for those processes that cease their useful life
   mid-period).  However, even though the costs incurred will be the same, the
   time-value of money changes due to the discount-rate.  As the fixed costs of
   a process are tied to the length of its useful life, those processes that do
   not fall on a period boundary require unique time-value multipliers in the
   objective function.

Many EEO efforts need to model sub-annual variations in demand as well.  Temoa
allows the modeler to subdivide years into slices, comprised of a season and a
time of day (e.g.  winter evening).  Unlike the periods, there is no restriction
on what labels the modeler may assign to the :math:`time\_season` and
:math:`time\_of\_day` set elements.  There is similarly no pre-described order,
and modeling efforts should not rely on a specific ordering of annual slices.


A Word on Index Ordering
^^^^^^^^^^^^^^^^^^^^^^^^

The ordering of the indices is consistent throughout the model to promote an
intuitive "left-to-right" description of each parameter, variable, and
constraint set.  For example, Temoa's output commodity flow variable
:math:`FO_{p,s,d,i,t,v,o}` may be described as "in period (:math:`p`) during
season (:math:`s`) at time of day (:math:`d`), the flow of input commodity
(:math:`i`) to technology (:math:`t`) of vintage (:math:`v`) generates an output
commodity flow (:math:`o`) of :math:`FO_{p,s,d,i,t,v,o}`."  For any indexed
parameter or variable within Temoa, our intent is to enable a mental model of a
left-to-right arrow-box-arrow as a simple mnemonic to describe the "input
:math:`\rightarrow` process :math:`\rightarrow` output" flow of energy.  And
while not all variables, parameters, or constraints have 7 indices, the 7-index
order mentioned here (p, s, d, i, t, v, o) is the canonical ordering.  If you
note any case where, for example, d comes before s, that is an oversight.


Deviations from Standard Mathematical Notation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Temoa deviates from standard mathematical notation and set understanding in two
ways.  The first is that Temoa places a restriction on the *time* set elements.
Specifically, while most optimization programs treat set elements as arbitrary
labels, Temoa assumes that all elements of the :math:`time\_existing`,
:math:`time\_horizon`, and :math:`time\_future` sets are integers.  Further,
these sets are assumed to be `ordered`, such that the minimum element is
"nought".  For example, if :math:`P = \{2015, 2020, 2030\}`, then :math:`P_0 =
2015`.  (Note the capital :math:`P` with the nought subscript indicates the
first element in the P set.)  We will explain the reason for this deviation
shortly.

The second set of deviations revolves around the use of the Theta superset
(:math:`\Theta`).  The Temoa code makes heavy use of sparse sets, for both
correctness and efficient use of computational resources, but for brevity and
some "implementation details," we do not enumerate their logical creation here.
Instead, we rely on the readers general understanding of the context.  For
example, in the sparse creation of the constraints of the Demand constraint
class (explained in sections 3.4  and 4.2), we state simply that the constraint
is instantiated "for all the ``<p``,\ ``s``,\ ``d``,\ ``dem>`` tuples in
:math:`\Theta_{\text{demand parameter}}`".  This means that the constraint is
only defined for the exact indices for which the modeler specified end-use
demands via the Demand parameter.

A similar deviation from standard notation occurs with summation over some sets.
Rather then being pedantically correct, including various "such that" clauses in
summation domain specifications, we assume that all summations occur in a sparse
manner.  Take equation :eq:`Activity` as an example (described in context in
section 3.4.):

.. math::

   \textbf{ACT}_{p, s, d, t, v} = \sum_{I, O} \textbf{FO}_{p,s,d,i,t,v,o}

   \\
   \forall \{p, s, d, t, v\} \in \Theta_{\text{activity}}

It defines the Activity variable for every valid combination of ``p``, ``s``,
``d``, ``t``, and ``v`` as the sum over all inputs and outputs.  In standard
notation, this might include nonsensical items in each summation, like perhaps
an input of electricity and an output of sunlight for a diesel powered vehicle.
However, in this context, summing over I and O implicitly only includes the
valid combinations of :math:`\Theta_{flow}`.


Parameters
----------

.. _table_parameter:

.. csv-table:: List of Temoa parameters with which a modeler might interact.
           The asterisked (\*) elements are automatically derived by the model
           and are not user-specifiable.
   :header: "Parameter","Temoa Name","Domain","Short Description"
   :widths: 12, 25, 5, 50

   ":math:`\text{CF}_{s,d,t,v}`","CapacityFactor",":math:`\mathbb{I}`","Capacity factor of a process"
   ":math:`\text{C2A}_{t,v}`","Capacity2Activity",":math:`\mathbb{R}^+_0`","Converts from capacity to activity units"
   ":math:`\text{FC}_{p,t,v}`","CostFixed",":math:`\mathbb{R}`","Fixed operations \& maintenance cost"
   ":math:`\text{IC}_{t,v}`","CostInvest",":math:`\mathbb{R}`","Tech-specific investment cost"
   ":math:`\text{MC}_{p,t,v}`","CostMarginal",":math:`\mathbb{R}`","Variable operations \& maintenance cost"
   ":math:`\text{DEM}_{p,s,d,c}`","Demand",":math:`\mathbb{R}^+_0`","End-use demands"
   ":math:`\text{DR}_t`","DiscountRate",":math:`\mathbb{R}`","Tech-specific interest rate on investment"
   ":math:`\text{EFF}_{i,t,v,o}`","Efficiency",":math:`\mathbb{R}^+_0`","Tech- and commodity-specific efficiency"
   ":math:`\text{EAC}_{i,t,v,o,e}`","EmissionsActivity",":math:`\mathbb{R}`","Tech-specific emissions rate"
   ":math:`\text{ELM}_{p,e}`","EmissionsLimit",":math:`\mathbb{R}^+_0`","Emissions limit by time period"
   ":math:`\text{ECAP}_{t,v}`","ExistingCapacity",":math:`\mathbb{R}^+_0`","Pre-existing capacity"
   ":math:`\text{GDR}`","GlobalDiscountRate",":math:`\mathbb{R}`","Global rate used to calculate present cost"
   ":math:`\text{LLN}_{t,v}`","LifetimeLoan",":math:`\mathbb{N}`","Tech- and vintage-specific loan term"
   ":math:`\text{LTC}_{p,t,v}`","LifetimeTech",":math:`\mathbb{N}`","Tech- and vintage-specific lifetime"
   ":math:`\text{MAX}_{p,t}`","MaxCapacity",":math:`\mathbb{R}^+_0`","maximum tech-specific capacity by period"
   ":math:`\text{MIN}_{p,t}`","MinCapacity",":math:`\mathbb{R}^+_0`","minimum tech-specific capacity by period"
   ":math:`\text{RSC}_{p,c}`","ResourceBound",":math:`\mathbb{R}^+_0`","Upper bound on resource capacity"
   ":math:`\text{SEG}_{s,d}`","SegFrac",":math:`\mathbb{I}`","Fraction of yr represented by each (s, d) tuple"
   ":math:`\text{SPL}_{i,t,o}`","TechOutputSplit",":math:`\mathbb{I}`","Fraction of total tech output by input commodity"
   ":math:`{}^*\text{LA}_{t,v}`","LoanAnnualize",":math:`\mathbb{R}^+_0`","loan amortization by tech and vintage; based on :math:`DR_t`"
   ":math:`{}^*\text{LEN}_p`","PeriodLength",":math:`\mathbb{N}`","Number of years in period :math:`p`"
   ":math:`{}^*\text{R}_p`","PeriodRate",":math:`\mathbb{R}`","Converts future annual cost to discounted period cost"
   ":math:`{}^*\text{TLF}_{p,t,v}`","TechLifetimeFrac",":math:`\mathbb{I}`","Fraction of last time period that tech is active"


.. _influential_efficiency:

Parameter: Efficiency (:math:`{EFF}_{i \in C_p,t \in T,v \in V,o \in C_c}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As it is the most influentual to the rest of the Temoa model, we present the
Efficiency (EFF) parameter first.  Beyond defining the efficiency of each
process, Temoa also notes the *indices* to understand the valid input
:math:`\rightarrow` process :math:`\rightarrow` output paths for energy.  For
instance, if a modeler does not specify an efficiency for a 2020 vintage coal
power plant, then Temoa will recognize any mention of a 2020 vintage coal power
plant elsewhere as an error.  Generally, if a process is not specified in the
efficiency table,\ [#efficiency_table]_ Temoa assumes it is not a valid process
and will warn with pointed debugging information, where appropriate.


Parameter CapacityFactor (:math:`{CF}_{s \in S,d \in D,t \in T,v \in T}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Where many models assign a capacity factor to a technology class only, Temoa
indexes the CapacityFactor parameter by vintage and time slice as well.  This
enables the modeler to specify the capacity factor of a process per season and
time of day, as well as recognizing any advances within a sector of technology.
This may be useful, for example, in working with a renewable portfolio, where
the amount of a resource is dependent on the time of year and time of day.


Parameter: Capacity2Activity (:math:`{C2A}_{t \in T,v \in V}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Capacity and Activity are inherently two different units of measure.  Capacity
is a unit of energy per time (:math:`\frac{energy}{time}`), while Activity is
a measure of total energy actually emitted (:math:`energy`).  However, there are
times when one needs to compare the two, and this parameter makes those
comparisons more natural.  For example, a capacity of 1 GW for one year works
out to an activity of

.. math::

   {1 GW} \cdot {8,760 \tfrac{hr}{yr}} \cdot {3,600 \tfrac{sec}{hr}} \cdot
      {10^{-6} \tfrac{P}{G}} = {31.536 \tfrac{PJ}{yr}}

.. centered::
   or

.. math::

   {1 GW} \cdot {8,760 \tfrac{hr}{yr}} \cdot {10^{-3} \tfrac{T}{G}} = {8.75 TWh}

The best place to see this in use is in the CapacityConstraint (explained in
section 3.4).  When comparing one capacity to another, the comparison is easy,
unit wise.  However, when one *needs* to compare capacity and activity, how does
one reconcile the units?  One way to think about the utility of this parameter
is in the context of the question: "How much activity would this capacity
create, if used 100% of the time?"


Parameter: CostFixed (:math:`{FC}_{p \in P,t \in T,v \in V}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The CostFixed parameter states the fixed cost associated with any process.
Fixed costs are those that **must** be paid, regardless of the use of a
facility.  For instance, if a nuclear power plant is built, there are certain
costs that must be paid, like insurance, security, mowing the lawn, etc.
These are in addition to the loan, so once the loan is paid off, these costs are
still incurred every year.

Temoa's default objective function assumes the modeler has specified this
parameter in units of currency per unit capacity (:math:`\tfrac{CUR}{Unit
Cap}`).


Parameter: CostInvest (:math:`{IC}_{t \in T,v \in P}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This parameter is basically the cost of the loan.  Unlike the CostFixed and
CostMarginal parameters, CostInvest only applies to vintages of technologies
within the model optimization horizon (:math:`time\_optimize`).  Like CostFixed,
CostInvest is specified in units of currency per unit of capacity and is only
used in the default objective function.


Parameter: CostMarginal (:math:`{MC}_{p \in P,t \in T,v \in V}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The CostMarginal parameter is a measure of the cost of a unit of activity of an
installed process.  It is specified as a unit of currency per a unit of
activity and is only used in the default objective function.


Parameter: Demand (:math:`{DEM}_{p \in P,s \in S,d \in D,c \in C_d}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Demand parameter allows the modeler to define the end-use demand levels for
all periods and time-slices.  This parameter is the most important parameter
because without it, the rest of model has no incentive to build anything.

It is a historical -- and unfortunately tedious -- detail that one must specify
a demand for every time slice within a period.  One of the items on the Temoa
Project TODO list is to update the model so that one only need specify a
time-slice distribution for Demand, and period-specific demand levels.


Parameter: DiscountRate (:math:`{DR}_{t \in T}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to the :math:`GlobalDiscountRate`, a modeler may also specify a
technology-specific discount rate.  If not specified, this rate defaults to 5%.


Parameter: EmissionsActivity (:math:`{EAC}_{e \in C_e,\{i,t,v,o\} \in \Theta_{\text{efficiency}}}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Temoa currently has two methods for enabling a process to produce an output: the
Efficiency parameter, and the EmissionsActivity parameter.  Where the Efficiency
parameter defines the efficiency for a unit of process activity to produce an
output, the EmissionsActivity parameter allows for secondary outputs.  As the
name suggests, this parameter was originally intended to account for emissions
per unit activity, but it more accurately describes *parallel* activity.  For
the time being, it is restricted to emissions accounting (by the :math:`e \in
C_e` set restriction), but an item on the Temoa TODO list is to upgrade the use
of this parameter.  For instance, there is currently no avenue to model with
Temoa a dual-function process, such as a combined heat and power plant.


Parameter: EmissionsLimit (:math:`{ELM}_{p \in P,e \in C_e}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The EmissionsLimit parameter is fairly self explanatory, ensuring that Temoa
finds a solution that fits within the modeler-specified limit of emission
:math:`e` in time period :math:`p`.


Parameter: ExistingCapacity (:math:`{ECAP}_{t \in T,v \in E}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In contrast to some competing models, technologies in Temoa can have
vintage-specific characteristics within the same period.  Thus, Temoa treats
existing technological capacity as full-blown processes, requiring all of the
engineering characteristics of a standard process.  This is Temoa's answer to
what some call "residual capacity."


.. _GDR:

Parameter: GlobalDiscountRate (:math:`{GDR}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In financial circles, the value of money is dependendent on when it was
measured.  There is no method to measure the absolute value of a currency, but
there are `generally accepted relative rates`_ for forecasting and historical
purposes.  Temoa uses the same general concept, that the future value (FV) of a
sum of currency is related to the net present value (NPV) via the formula:

.. math::

   FV = \frac{NPV}{(1 + GDR)^n}

where :math:`n` is in years.  This parameter is only used in Temoa's objective
function.


Parameter: LifetimeLoan (:math:`{LLN}_{t \in T,v \in P}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Temoa differs from many EEO models by giving the modeler the ability to separate
the loan lifetime from the useful life of the technology.  This parameter
specifies the length of the loan associated with investing in a process, in
years.  If not specified, the default is 30 years.


Parameter: LifetimeTech (:math:`{LTC}_{p \in P,t \in T,v \in V}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Similar to LifetimeLoan, this parameter specifies the total useful life of
technology, years.  If not specified, the default is 10 years.


.. _ParamMaxCapacity:

Parameter: MaxCapacity (:math:`{MAX}_{p \in P,t \in T}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The MaxCapacity parameter enables a modeler to ensure that a certain technology
is not overused.  There is some subtlety with this parameter as the enforcing
constraint ensures that the max **total** capacity of a technology class is
under this maximum.  That is, all active vintages are constrained.  We provide
more information in the :ref:`maximum capacity constraint
<MaxCapacity_Constraint>` explanation.


Parameter: MinCapacity (:math:`{MIN}_{p \in P,t \in T}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The MinCapacity parameter is analogous to the :ref:`maximum capacity
parameter<ParamMaxCapacity>`, except that it specifies the minimum capacity for
which Temoa must ensure installation.


Parameter: ResourceBound (:math:`{RSC}_{p \in P,c \in C_p}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

   Joe, I'm thinking about removing this parameter and constraint
   entirely.  This constraint is only partially correct because it currently
   limits the flow of a resource over the entire system (in a period), not just
   on the cradle side of the energy flow.  If a modeler wants to limit the
   input, they should perhaps limit the capacity?  Or we need to reformulate
   this slightly so that it actually does apply solely to the cradle side of the
   system map.


Parameter: SegFrac (:math:`{SEG}_{s \in S,d \in D}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Temoa does not "hard code" the percentage of an annum that each time slice
consumes.  This parameter is the modeler's avenue to adjust to the specific
needs, with the caveat that the sum over all slices must be 1.


Parameter: TechOutputSplit (:math:`{SPL}_{i \in C_p,t \in T,o \in C_c}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some technologies have a single input fuel but have multiple output forms of
energy.  For the sake of modeling, certain technologies require a fixed
apportion of relative output.  For example, an oil refinery might have an input
energy of crude oil, and the modeler wants to ensure that its output is 70%
diesel and 30% gasoline.


\*Parameter: LoanAnnualize (:math:`{LA}_{t \in T,v \in P}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is an automatically calculated pseudo-parameter based on the
process-specific loan length (the LifetimeLoan parameter), and process-specific
discount rate (the DiscountRate parameter).  It is calculated via the formula:

.. math::

   LA_{t,v} = \frac{DR_{t,v}}{1 - (1 + DR_{t,v})^{{}^- LLN_{t,v}}}

   \forall \{t, v\} \in \Theta_\text{CostInvest}


\*Parameter: PeriodLength (:math:`{LEN}_{p \in P}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Given that the modeler may specify arbitrary period boundaries, this parameter
specifies the number of years contained in each period.  The final year is the
largest element in :math:`time\_future` which is specifically not included in
the list of periods in :math:`time\_optimize` (:math:`P`).  The length
calculation for each period then exploits the fact that the ``time`` sets are
ordered:

.. math::

   \text{LET boundaries} & = \text{sorted}(H \cup F) \\
   \text{LET I(x)} & = \text{index of x in boundaries} \\
   & \therefore \\
   {LEN}_p & = \text{periods}[ I(x) + 1 ] - p

   \forall p \in P


\*Parameter: PeriodRate (:math:`R_{p \in P}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This pseudo-parameter is a micro optimization for the Temoa objective function.
Because Temoa optimizes a single characteristic year within a period, and
differentiates the :math:`n` copies of that single year solely by the time-value
of money, the marginal cost of every activity will be the
same for the whole period.  Thus, rather than calculating the same summation for
every technology and vintage within a period, we calculate it once in this
pseudo-parameter and lookup the value as necessary during the objective function
generation.  The formula is:

.. math::

   R_p = \sum_{y = 0}^{{LEN}_p} \frac{1}{{(1 + GDR)}^{(P_0 - p - y)}}

   \\
   \forall p \in P


\*Parameter: TechLifeFrac (:math:`{TLF}_{p \in P,t \in T,v \in V}`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The modeler may specify a useful lifetime of a process such that the process
will be decommissioned part way through a period.  Rather than attempt to
delineate each year within that final period, Temoa makes the choice to average
the the total output of the process over the entire period but limit the
available capacity and output of the decommissioning process by the ratio of how
long through the period the process is active.  This parameter is that ratio,
formally defined as:

.. math::

   TLF_{p,t,v} = \frac{v + LTC_{t,v} - p}{LEN_p}

   \\
   \forall \{p,t,v\} & \in \Theta_\text{Activity by PTV} | \\
   v + LTC_{t,v} & \notin P, \\
   v + LTC_{t,v} & \le max(F), \\
   p & = max(P | p < v + LTC_{t,v})

Note that this parameter is defined only for the final period of these "partial
period" processes.  As an example, if a model has ``P = {2010, 2012, 2020}``,
and a process ``<t,v> = <car,2010>`` has a useful lifetime of 5 years, then this
parameter would include only the last activity index for the process.  Namely,
:math:`p = 2012` as ``<p,t,v> = <2012,car,2010>``.  Note that this parameter
does *not* cover any technology whose end of useful life falls on a period
boundary.


Variables
---------

.. _table_variable:

.. tabularcolumns:: |l|L|c|l|

.. raw:: latex

   \begin{threeparttable}
   \capstart\caption{Temoa's Main Variables}

   \begin{tabulary}{\linewidth}{| l | p{3cm} | c | l |}
   \hline
   \textbf{Variable} & \textbf{Temoa Name} & \textbf{Domain} & \textbf{Short Description}
   \\\hline

   $FI_{p,s,d,i,t,v,o}$ & V\_FlowIn & $\mathbb{R}^+_0$   & Commodity flow into a tech to produce a given output
   \\\hline

   $FO_{p,s,d,i,t,v,o}$ & V\_FlowOut & $\mathbb{R}^+_0$  & Commodity flow out of a tech based on a given input
   \\\hline

   $ACT_{p,s,d,t,v}$    & V\_Activity & $\mathbb{R}^+_0$ & Total tech commodity production in each (s, d) tuple
   \\\hline

   $CAP_{t,v}$          & V\_Capacity & $\mathbb{R}^+_0$ & Required tech capacity to support associated activity
   \\\hline

   $CAPAVL_{p,t}$       & V\_CapacityAvailable\-ByPeriodAndTech & $\mathbb{R}^+_0$ & The Capacity of technology $t$ available in period $p$
   \\\hline
   \end{tabulary}

   \end{threeparttable}

.. only:: html

   .. csv-table:: Temoa's Main Variables
      :header: "Variable","Temoa Name","Domain","Short Description"
      :widths: 15, 15, 10, 60

      ":math:`FI_{p,s,d,i,t,v,o}`","V\_FlowIn",":math:`\mathbb{R}^+_0`","Commodity flow into a tech to produce a given output"
      ":math:`FO_{p,s,d,i,t,v,o}`","V_FlowOut",":math:`\mathbb{R}^+_0`","Commodity flow out of a tech based on a given input"
      ":math:`ACT_{p,s,d,t,v}`","V_Activity",":math:`\mathbb{R}^+_0`","Total tech commodity production in each (s, d) tuple"
      ":math:`CAP_{t,v}`","V_Capacity",":math:`\mathbb{R}^+_0`","Required tech capacity to support associated activity"
      ":math:`CAPAVL_{p,t}`","V_CapacityAvailable\-ByPeriodAndTech",":math:`\mathbb{R}^+_0`","The Capacity of technology :math:`t` available in period :math:`p`"


The most fundamental variables in the Temoa formulation are :math:`FlowIn` and
:math:`FlowOut`.  They describe the commodity flows into and out of a process in
a given time slice.  They are related through the ProcessBalance constraint
:eq:`ProcessBalance`, which in essence, guarantees the conservation of energy
for each process.

The Activity variable is defined as the sum over all inputs and outpus of a
process in a given time slice (see equation :eq:`Activity`).  At this time, one
potential "gotcha" is that for a process with multiple inputs or outputs, there
is no attempt to reconcile energy units: Temoa assumes all inputs are
comparable, and as no understanding of units.  The onus is on the modeler to
ensure that all inputs and outputs have similar units.\ [#units_comparison]_

The Capacity variable is used in the default objective function as the amount of
capacity of a process to build.  It is indexed for each process, and Temoa
constrains the Capacity variable to at least be able to meet the Activity of
that process in all time slices in which it is active :eq:`Capacity`.

Finally, CapacityAvailableByPeriodAndTech is a convenience variable that is
not strictly necessary, but used where the individual vintages of a technology
are not warranted (e.g. in calco).

The equations governing these variables are shown in the Constraints section,
below.


Constraints
-----------

There are 4 main equations that govern the flow of energy through the model
network.  The DemandConstraint ensures that the supply meets demand in every
time slice.  For each process, the ProcessBalance ensures at least as much
energy enters a process as leaves it (conservation of energy at the process
level).  Between processes, the CommodityBalance ensures that at least as much
of a commodity is generated as is demanded by other process inputs.

In combination, those three constraints ensure the flow of energy through the
system.  The final calculation, the objective function, is what puts a monetary
cost to the actions dictated by the model.

The rest of this section defines each model constraint, with a rational for
existance.  We use the implementation-specific names for the constraint names as
both an artifact of our documentation generation process, and to highlight the
organization of the functions within the actual code.  They are listed roughly
in order of importance.

Variable Related Constraints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These first four constraints relate specifically to the calculation of
variables.  There is some overlap with the rest of the constraints, but they
are unique enough to warrant special attention to a Temoa modeler.

.. autofunction:: temoa_rules.ProcessBalance_Constraint

.. autofunction:: temoa_rules.Activity_Constraint

.. autofunction:: temoa_rules.Capacity_Constraint

Objective Function
^^^^^^^^^^^^^^^^^^

.. autofunction:: temoa_rules.Objective_rule

General Temoa Constraints
^^^^^^^^^^^^^^^^^^^^^^^^^

The rest of the constraints fine-tune the Temoa model to account for various
real-world phenomena.

.. autofunction:: temoa_rules.Demand_Constraint

.. autofunction:: temoa_rules.DemandActivity_Constraint

.. autofunction:: temoa_rules.CommodityBalance_Constraint

.. autofunction:: temoa_rules.FractionalLifeActivityLimit_Constraint

.. autofunction:: temoa_rules.BaseloadDiurnal_Constraint

.. autofunction:: temoa_rules.Storage_Constraint

User-Specific Constraints
^^^^^^^^^^^^^^^^^^^^^^^^^

The constraints provided in this section are not required for proper system
operation, but allow the modeler some further degree of system specification.

.. autofunction:: temoa_rules.ExistingCapacity_Constraint

.. autofunction:: temoa_rules.EmissionLimit_Constraint

.. _MaxCapacity_Constraint:

.. autofunction:: temoa_rules.MaxCapacity_Constraint

.. autofunction:: temoa_rules.ResourceExtraction_Constraint

.. autofunction:: temoa_rules.TechOutputSplit_Constraint



General Caveats
---------------

With the example of a cogeneration plant in mind, there is currently only a
roundabout way to account for multiple concurrent outputs.



.. ===========================
.. The Temoa Model Formulation
.. ===========================
..
.. General Formulation Concepts
.. ----------------------------
..
.. The heart of Temoa is a technology explicit energy system optimization model.
.. It is an algebraic network of linked processes -- understood by the model as a
.. set of engineering characteristics (e.g. capital cost, efficiency, capacity
.. factor, emission rates) -- that transform raw energy sources into end-use
.. demands.  The model objective function minimizes the present-value cost of
.. energy supply through manipulation of installed process capacity and use over
.. time.
..
.. Figure 1 is a simplified visual example of the above paragraph.  It is a
.. "right-from-left" network graph, where the boxes represent processes, and the
.. circles represent the energy carriers between processes.  The modeler explicitly
.. dictates the size of the circles on the right via the "Demand" input, as well
.. the processes the model may employ to fill (meet) the demand circles.  The model
.. then decides the optimal (cheapest) allocation and use of processes and
.. resources.
..
.. It is important to note that Temoa is an abstract model, following the adage
.. "Garbage in?  Garbage out."  That is, the value of its output is directly
.. related to the quality of a modeler's input.  Generally, an optimization
.. analysis requires `both` the mathematical model `and` a set of input data:
.. without either, there is no analysis.



======================================
The Temoa Computational Implementation
======================================

We have implemented Temoa within an algebraic modeling environment (AME).  AMEs
provide both a convenient avenue to describe mathematical optimization models
for a computational context, and allow for abstract model formulations
(Kallrath, 2004).  In contrast to describing a model in a formal computer
programming language like C or Java, AMEs generally have syntax that directly
translates to standard mathematical notation.  Consequently, models written in
AMEs are more easily understood by a wider variety of people.  Further, by
allowing abstract formulations, a model written with an AME may be used with
many different input data sets.

Probably the most well known algebraic modeling environments are the General
Algebraic Modeling System (GAMS) (Brooke and Rosenthal, 2003), AMPL (Fourer,
1987), and perhaps GNU MathProg (Makhorin, 2001).  All three environments
provide concise syntax that closely resembles standard (paper) notation.  For
various reasons, we decided to implement Temoa with Python Optimization Modeling
Objects (Pyomo).

Pyomo provides similar functionality to GAMS, AMPL, and MathProg, but is open
source and written in the Python scripting language.  This has two general
consequences of which to be aware:

 * Python is a scripting language; Python scripts are therefore an order of
   magnitude slower than an equivalent compiled program.
 * Pyomo provides similar functionality, but because of its Python heritage, is
   **much** more verbose than GAMS, AMPL, or MathProg.

It is our view that the speed penalty of Python as compared to compiled
languages is inconsequential in the face of other large resource bottle necks,
so we omit any discussion of it as an issue.  However, the "boiler-plate" code
(verbosity) overhead requires some discussion.  We discuss this in the
:ref:`Anatomy of a Constraint <constraint-anatomy>`.

File Structure
--------------

The Temoa model code is split into 5 main files:

 * ``temoa_model.py`` - contains the overall model definition, defining the
   various sets, parameters, variables, and equations of the Temoa model.  To
   get a high-level overview of the model, this is the file to peruse.

 * ``temoa_rules.py`` - mainly contains the rule implementations.  That is, this
   file has the meat of the objective function, pseudo-parameter creation, and
   constraint creation logic.  Where ``temoa_model`` provides the high-level
   overview, this file provides the actual summations and relational equation
   implementations.

 * ``temoa_lib.py`` - mainly contains meta functions for the model.  For
   instance, Temoa makes heavy use of sparse sets, and ``temoa_lib`` contains
   the functions that create those sparse sets.  This file also contains various
   error checking routines, so that their logic does not clutter the
   implementations in ``temoa_rules``, as well as the logic that handles the
   command line interaction.

 * ``temoa_graphviz.py`` - Currently Temoa's sole visualizations are generated
   through Graphviz.  This file contains the various Graphviz-specific graph
   generation routines.

 * ``temoa_stochastic.py`` - contains the PySP mandated alterations to the
   deterministic model for use in a stochastic function.  Specifically, Temoa
   only needs one additional constraint class in order to partition the
   calculation of the objective function per period.

If you are working with the release snapshot of the Temoa model, then you will
only see one file, ``temoa.py``.  This file is actually a compressed archive (in
ZIP format) containing these 5 files, and may be manipulated with standard
utilities (e.g. PKZIP, WinZip, Info-ZIP).  (Due to implementation details, be
careful uncompressing the archive as it is analogous to a "`Tarbomb`_".)

If you are working with a Temoa Git repository, these files are in the
``temoa_model/`` subdirectory.


.. _constraint-anatomy:

Anatomy of a Constraint
-----------------------

Consider the demand constraint (equation :eq:`Demand`, above):

.. math::
   \sum_{I, T, V} FO_{p, s, d, i, t, v, dem} \ge DEM_{p, s, d, dem}

   \\
   \forall \{p, s, d, dem\} \in \Theta_{\text{demand parameter}}

Implementing this with Pyomo requires two pieces:

 #. a constraint definition (in ``temoa_model.py``), and
 #. the constraint implementation (in ``temoa_rules.py``).

One Pyomo definition of this constraint might be:

.. topic:: temoa_model.py

   ...

   .. code-block:: python
      :linenos:

      M.DemandConstraint = Constraint(
        M.time_optimize, M.time_season, M.time_of_day, M.commodity_demand,
        rule=Demand_Constraint
      )

   ...

In line 1, '``M.DemandConstraint =``' creates a place holder in the model object
``M``, called 'DemandConstraint'.  Like a variable, this is the name through
which Pyomo will reference this class of constraints.  ``Constraint(...)`` is a
Pyomo-specific function that creates each individual constraint in the class.
The first arguments (line 2) are the index sets of the constraint class.  Line 2
is the Pyomo method of saying "for all" (:math:`\forall`).  Line 3 contains the
final, mandatory argument (``rule=...``) that specifies the name of the
implementation rule for the constraint, in this case ``Demand_Constraint``.
Pyomo will call this rule with each tuple in the cartesian product of the index
sets.

The associated implementation rule might be:

.. topic:: temoa_rules.py

   ...

   .. code-block:: python
      :linenos:

      def Demand_Constraint ( M, p, s, d, dem ):
         if (p, s, d, dem) not in M.Demand:  # If user did not specify this Demand, tell
            return Constraint.Skip           # Pyomo to ignore this constraint index.

           # store the summation into the local variable 'supply' for later reference
         supply = sum(
           M.V_FlowOut[p, s, d, S_i, S_t, S_v, dem]

           for S_t in M.tech_all
           for S_v in M.vintage_all
           for S_i in ProcessInputsByOutput( p, S_t, S_v, dem )
         )

           # The '>=' operator creates (in this case) a "Greater Than" *object*, not a
           # True/False value as a Python programmer might expect; the intermediate
           # variable 'expr' is thus not strictly necessary, but we leave it as reminder
           # of this potentially confusing behavior
         expr = (supply >= M.Demand[p, s, d, dem])
         return expr

   ...

The Python boiler-plate code to create the rule is on line 1.  It begins with
:code:`def`, followed by the rule name (matching the :code:`rule=...`  argument
in the constraint definition in ``temoa_model``), followed by the argument list.
The argument list will always start with the model (Temoa convention shortens
this to just :code:`M`) followed by local variable names in which to store the
index set elements passed by Pyomo.  Note that the ordering is the same as
specified in the constraint definition.  Thus the first item after :code:`M`
will be an item from :math:`time\_optimize`, the second from
:math:`time\_season`, the third from :math:`time\_of\_day`, and the fourth from
:math:`commodity\_demand`.  Though one could choose :code:`a`, :code:`b`,
:code:`c`, and :code:`d` (or any naming scheme), we chose :code:`p`, :code:`s`,
:code:`d`, and :code:`dem` as part of a :ref:`naming scheme
<naming_conventions>` to aid in mnemonic understanding.  Consequently, the rule
signature (Line 1) is another place to look to discover what general indices
define a constraint.

Lines 2 and 3 are an indication that this constraint is implemented in a
non-sparse manner.  That is, Pyomo does not inherently know the valid indices
for all of a model's contexts.  In ``temoa_model``, the constraint definition
listed four index sets, so Pyomo will naively call this function for every
possible combination of tuple ``<p``,\ ``s``,\ ``d``,\ ``dem>``.  However, as
there may be slices for which a demand does not exist (e.g. the winter season
might have no cooling demand), there is no need to create a constraint for any
tuple involving 'winter' and 'cooling'.  Indeed, an attempt to access a demand
for which the modeler has not specified a value results in a Pyomo error, so it
is necessary to ignore any tuple for which no Demand exists.

Lines 6 through 12 are a single *source-line* that we split over 7 lines for
clarity.  These lines implement the summation of the Demand constraint, summing
over all technologies, vintages, and the inputs that generate the end-use demand
``dem``.

Lines 6 through 12 also showcase a very common idiom in Python:
list-comprehension.  List comprehension is a concise and efficient syntax to
create lists.  As opposed to building a list element-by-element, list
comprehension can convert many statements into a single operation.  Consider a
naive approach to calculating the supply::

   to_sum = list()
   for S_t in M.tech_all:
      for S_v in M.vintage_all:
         for S_i in ProcessInputsByOutput( p, S_t, S_v, dem ):
            to_sum.append( M.V_FlowOut[p, s, d, S_i, S_t, S_v, dem] )
   supply = sum( to_sum )

While both implementations have the same number of lines, this last one
creates an extra list (``to_sum``), then builds the list element by element with
``.append()``, before finally calculating the summation.  This means that the
Python interpreter must iterate through the elements of the summation, not once,
but twice.

A less naive approach would replace the ``append()`` call with the ``+=``
operator, reducing the number of iterations through the elements to one::

   supply = 0
   for S_t in M.tech_all:
      for S_v in M.vintage_all:
         for S_i in ProcessInputsByOutput( p, S_t, S_v, dem ):
            supply += M.V_FlowOut[p, s, d, S_i, S_t, S_v, dem]

Why is list comprehension necessary?  Strictly speaking, it is not, especially
in light of this last example, which may read more familiar to those comfortable
with C, Fortran, or Java.  However, due to quirks of both Python and Pyomo,
list-comprehension is preferred both syntactically as "the Pythonic" way, and as
the more efficient route for many list manipulations.  (It also *may* seem
slightly more familiar to those used to a more mainstream algebraic modeling
language.)

With the correct model variables summed and stored in the ``supply`` variable,
line 18 creates the actual inequality comparison.  This line is superfluous, but
we leave it in the code as a reminder that inequality operators (i.e. :code:`<=`
and :code:`>=`) with a Pyomo object (like supply) generate a Pyomo *expression
object*, not a boolean True or False as one might expect.  It is this expression
object that must be returned to Pyomo, as on line 19.

The actual DemandConstraint differs from this one in only a couple of ways.
First, rather than calling the Demand_Constraint function for every possible
tuple combination, Temoa indexes DemandConstraint with a sparse index:

.. topic:: temoa_model.py (actual implementation)

   ...

   .. code-block:: python
      :linenos:

      M.DemandConstraint_psdc = Set( dimen=4, rule=lambda M: M.Demand.sparse_iterkeys() )
      # ...
      M.DemandConstraint = Constraint( M.DemandConstraint_psdc, rule=Demand_Constraint )

   ...

As discussed above, the DemandConstraint is only valid for modeler-specified
``<p``,\ ``s``,\ ``d``,\ ``dem>`` tuples.  Pyomo makes these accessible via the
parameter methods :code:`sparse_iterkeys()` and :code:`sparse_keys()`.  (In this
context, they both have the same result, so the decision of which to use is
outside the scope of this document.)  To create an index set from these, one
must make use of two keyword arguments to Pyomo's :code:`Set` class:
:code:`dimen=` and :code:`rule=`.  The :code:`dimen` keyword tells Pyomo how
many items each tuple will have (the dimensionality of the set), and the
:code:`rule` keyword should specify a function that will define the elements
(tuples) in the set.  In this case, the function for :code:`rule` is so simple
that there is no need to create a function elsewhere in the code base.  Instead,
a one-line `lambda function`_ returns the keys of the Demand parameter from the
instantiated model.  Finally, in place of the four sets specified in the
non-sparse implementation, one can use the now-available sparse-set
:code:`DemandConstraint_psdc`.  Pyomo will now only call the constraint
implementation rule for the items in the :code:`DemandConstraint_psdc` set, or
only for those Demands that the modeler specified.

On the choice of :code:`_psdc` for the index set name, there is no
Pyomo-enforced restriction.  However, use of an index set in place of the
non-sparse specification obfuscates over what indexes a constraint is defined.
While it is not impossible to deduce, either from the mathematical documentation
or from looking at the rule implementation of the constraint, the Temoa
convention includes in index set names the one-character version of each set
dimension.  In this case, the name :code:`DemandConstraint_psdc` implies that
this set has a dimensionality of 4, and (following the :ref:`naming scheme
<naming_conventions>`) the first index of each tuple will be an element of
:math:`time\_optimize`, the second an element of :math:`time\_season`, the third
an element of :math:`time\_of\_day`, and the fourth a commodity.  From the
contextual information that this is the Demand constraint, one can assume that
the ``c`` represents an element from :math:`commodity\_demand`.

Over a sparse-index, the constraint implementation changes only slightly:

.. topic:: temoa_rules.py (actual implementation)

   ...

   .. code-block:: python
      :linenos:
      :emphasize-lines: 2-5,15

      def Demand_Constraint ( M, p, s, d, dem ):
         if not (M.Demand[p, s, d, dem] > 0):
            # User must have supplied a 0 demand: no need to create a useless
            # constraint like X >= 0
            return Constraint.Skip

         supply = sum(
           M.V_FlowOut[p, s, d, S_i, S_t, S_v, dem]

           for S_t in M.tech_all
           for S_v in M.vintage_all
           for S_i in ProcessInputsByOutput( p, S_t, S_v, dem )
         )

         DemandConstraintErrorCheck ( supply, dem, p, s, d )

         expr = (supply >= M.Demand[p, s, d, dem])
         return expr

   ...

As this constraint is guaranteed to be called only for the demand indices
specified by the modeler, there is no need to check for the existence of a tuple
in the Demand parameter.  Instead, the constraint ensures that a Demand is
non-zero.  The only other change is the error check on line 15.  This function
is defined in ``temoa_lib``, and simply ensures that at least one process
supplies the demand ``dem`` in time slice ``<p``,\ ``s``\, ``d>``.  If no
process supplies the demand, then it quits computation immediately (as opposed
to completing a potentially lengthy model generation and waiting for the solver
to recognize the infeasibility of the model).  Further, the function lists
potential places for the modeler to look to correct the problem.  This last
capability is subtle, but in practice is extremely useful while debugging a
model.


A Word on Verbosity
-------------------

Implementing this same constraint in AMPL, GAMS, or MathProg would require only
a single source-line (in a single file).  Using MathProg as an example, it might
look like:

.. code-block:: mathprog

   s.t. DemandConstraint{(p, s, d, dem) in sDemand_psd_dem} :
       sum{(p, s, d, Si, St, Sv, dem) in sFlowVar_psditvo}
         V_FlowOut[p, s, d, Si, St, Sv, dem]
    >=
       pDemand[p, s, d, dem];

While the syntax is not a direct translation, the indices of the constraint
(``p``, ``s``, ``d``, and ``dem``) are clear, and by inference, so are the
indices of summation (``i``, ``t``, ``v``) and operand (``V_FlowOut``).  This
one-line definition creates an inequality for each period, season, time of day,
and demand, ensuring that total output meets each demand in each time slice --
almost exactly as we have formulated the demand constraint :eq:`Demand`.  In
contrast, Temoa's implementation in Pyomo takes 47 source-lines (the code
discussed above does not include the function documentation).  While some of the
verbosity is inherent to working with a general purpose scripting language, and
most of it is our formatting for clarity, the absolute minimum number of lines a
Pyomo constraint can be is 2 lines, and that likely will be even less readable.

So why use Python and Pyomo if they are so verbose?  In short, for four
reasons:

 * Temoa has the full power of Python, and has access to a rich ecosystem of
   tools (e.g. numpy, matplotlib) that are not as cleanly available to other
   AMLs.  For instance, there is minimal capability in MathProg to error check a
   model before a solve, and providing interactive feedback like what Temoa's
   DemandConstraintErrorCheck function does is difficult, if not impossible.
   While a subtle addition, specific and directed error messages are an
   effective measure to reduce the learning curve for new modelers.

 * Python has a vibrant community.  Whereas mathematical optimization has a
   small community, its open-source segment even smaller, and the EEO segment
   significantly smaller than that, the Python community is huge, and ecompasses
   many disciplines.  This means that where a developer may struggle to find an
   answer, implementation, or workaround to a problem with a more standard AML,
   Python will likely enable a community-suggested solution.

 * Powerful documentation tools.  One of the available toolsets in the Python
   world is documentation generators that *dynamically* introspect Python code.
   While it is possible to inline and block comment with more traditional AMLs,
   the integration with Python that many documentation generators have is much
   more powerful.  Temoa uses this capability to embed user-oriented
   documentation literally in the code, and almost every constraint has a block
   comment.  Having both the documentation and implementation in one place helps
   reduce the mental friction and discrepencies often involved in maintaining
   multiple sources of model authority.

 * AMLs are not as concise as thought.

This last point is somewhat esoteric, but consider the MathProg implementation
of the Demand constraint in constrast with the last line of the Pyomo verson::

   expr = (supply >= M.Demand[p, s, d, dem])

While the MathProg version indeed translates more directly to standard notation,
consider that standard notation itself needs extensive surrounding text to
explain the significance of an equation.  *Why* does the equation compare the
sum of a subset of FlowOut to Demand?  In Temoa's implementation, a high-level
understanding of what a constraint does requires only the last line of code:
"Supply must meet demand."

.. note:: Joe: Should I include a word on functional programming?  I don't know
   AMPL's syntax through first-hand experience, but MathProg is a subset of AMPL.

   Also, should I include the complete Demand_Constraint (i.e. with the block
   comment)?  To go along with that I have a rudimentary histogram::

   +++++++++++++++++++++++++ (user-manual/function-specific documentation)
   ++++++ (summation)
   ++++ (blank lines)
   +++ (error check)
   ++ (in-line comment)
   + function signature
   + (constraint equation creation)
   + (return statement)



Visualization
-------------

From the definition of the Temoa model as "an algebraic network of linked
processes," a directed network graph is a natural visualization.  Temoa utilizes
a graphic package called Graphviz to create a series of data-specific and
interactive energy-system maps.  The graphs are available in any format Graphviz
provides, including scalable vector graphics (SVG), portable network graphics
(PNG), portable document format (PDF), and (ecapsulated) postscript (E/PS).
Currently, the output graphs consist of a pre-results (possible) energy map, and
results per model period, including breakdowns of individual technology
activity.

Here are some examples of the graphical outputs Temoa can dynamically create.

.. figure:: images/simple_model.*
   :align: center
   :figclass: center

   This is a dynamically created image of one of the energy systems supplied
   with the Temoa example data sets.  It shows the possible flows energy could
   take in the energy system, providing a good overview of the system.

.. figure:: images/global_results.*
   :align: center
   :figclass: center

   The solved system graph, showing the high-level flow energy actually took in
   a period of the optimal system configuration.

.. figure:: images/tech_results.*
   :align: center
   :figclass: center

   This graphic shows the amount of installed capacity and total flow of energy
   through each vintage of a technology in a model period.

.. figure:: images/techvintage_results.*
   :align: center
   :figclass: center

   Drilling down even further, this image shows the individual time slice
   decisions the optimizer chose for a process in a model period.

Contrary to the static nature of other image file formats (e.g. PNG), SVG is a
text-based format (XML), with a much richer set of information encoding
possibilities than mere image display.  On top of being infinitely scalable, the
SVG format allows the inclusion of links and hyperlinks.  Temoa exploits this
capability to make interactive system and solution graphs.  Currently, this
means that one can use a web browser to view and interact with the generated SVG
images.\ [#web_browser_svg]_

Regardless of the final visual format chosen, the programmatic interaction with
Graphviz is entirely text based.  As RCS systems excel at handling text, the
input files created by Temoa for Graphviz can simultaneously provide another
vector for model debugging and a space-efficient archive of visualizations for
posterity and auditing purposes.  In addition, we have taken care to make these
intermediate files well-formatted so that a human eye may understand them
without undue effort.



======================
Interacting with Temoa
======================

The Command Line
----------------

Notwithstanding the graphical output afforded by Graphviz, interaction with
Temoa is currently a command line (CLI) venture.  Fortunately, Temoa does not
have many command line arguments so the cognitive effort required to understand
the interaction is minimal.

After downloading the ``temoa.py`` file from http://temoaproject.org/, open a
command line and run it with :code:`coopr_python`:

.. code::

   $ coopr_python  temoa.py
   usage: temoa.py [-h] [--graph_format GRAPH_FORMAT] [--show_capacity]
                   [--graph_type GRAPH_TYPE] [--use_splines]
                   dot_dat [dot_dat ...]
   temoa.py: error: too few arguments

In a Unix environment, you can make the file executable, and it can be executed
directly:

.. code::

   $ chmod +x temoa.py
   $ ./temoa.py
   usage: temoa.py [-h] [--graph_format GRAPH_FORMAT] [--show_capacity]
                   [--graph_type GRAPH_TYPE] [--use_splines]
                   dot_dat [dot_dat ...]
   temoa.py: error: too few arguments

The :code:`-h` command line argument provides the longer synopsis of the
available arguments:

.. code::

   $ ./temoa.py -h
   usage: temoa.py [-h] [--graph_format GRAPH_FORMAT] [--show_capacity]
                   [--graph_type GRAPH_TYPE] [--use_splines]
                   dot_dat [dot_dat ...]

   positional arguments:
     dot_dat               AMPL-format data file(s) with which to create a model
                           instance. e.g. "data.dat"

   optional arguments:
     -h, --help            show this help message and exit
     --graph_format GRAPH_FORMAT
                           Create a system-wide visual depiction of the model.
                           The available options are the formats available to
                           Graphviz. To get a list of available formats, use the
                           "dot" command: dot -Txxx. [Default: None]
     --show_capacity       Choose whether or not the capacity shows up in the
                           subgraphs. [Default: not shown]
     --graph_type GRAPH_TYPE
                           Choose the type of subgraph depiction desired. The
                           available options are "explicit_vintages" and
                           "separate_vintages". [Default: separate_vintages]
     --use_splines         Choose whether the subgraph edges needs to be straight
                           or curved. [Default: use straight lines, not splines]

Solving a model simply requires a data file.  The Temoa Project supplies example
data files on the website.  One of those data files is called ``test.dat``:

.. code::

   $ ./temoa.py  test.dat
   [    0.04] Reading data files.
   [        ] Creating Temoa model instance.Warning: ('t_oil_refinery', 2000) has a
   Warning: ('t_elccar', 2000) has a specified Efficiency, but does not have any ex
   Warning: ('t_oil_refinery', 2000) has a specified Efficiency, but does not have
   [    0.43
   [    0.80] Solving.
   [    0.85] Formatting results.
   Model name: TEMOA Entire Energy System Economic Optimization Model
   Objective function value (TotalCost): 398469346.331
   Non-zero variable values:
        395.535714285714    V_Activity(2010,summer,day,imp,coal,2000)
          2.480158730159    V_Activity(2010,summer,day,imp,gsl,2000)
        197.767857142857    V_Activity(2010,summer,day,t,coal,1990)
         39.553571428571    V_Activity(2010,summer,day,t,elccar,2010)
          0.446428571429    V_Activity(2010,summer,day,t,gascar,2000)
   [ ... ]

The model world described by ``test.dat`` is incredibly simple, and so solves
near instantaneously.  The output is extensive, enumerating the value of all
variables for the optimal configuration, so we show just the first few lines in
the documentation.  It is enough to get a sense of it however.

Temoa provides line-by-line output as progresses through each stage of a solve.
The very first line explains that temoa took 0.04 *processing* seconds to read
and parse the supplied model data.  *Processing* seconds are roughly a measure
of exactly how much time the program spent in the CPU, but are not a measure of
how long the modeler actually waited: though the output above suggests that the
whole model took about 0.85 processing seconds to complete, the time the author
sat waiting for the prompt to return was closer 1.8 seconds.

The next timing slot is empty, but the same line also contains a warning
message.  The warning message is pointing out that the input file includes some
inconsistent data that the modeler may want to address.  The timing information
immediately below the warnings is how long it took Coopr to create the Temoa
model instance.

Temoa intelligently emits these messages.  If only the results are warranted,
the modeler can redirect the *stderr* stream to the virtual wastebin:

.. code::

   $ ./temoa.py  test.dat  2>  /dev/null
   Model name: TEMOA Entire Energy System Economic Optimization Model
   Objective function value (TotalCost): 398469346.331
   Non-zero variable values:
        395.535714285714    V_Activity(2010,summer,day,imp,coal,2000)
          2.480158730159    V_Activity(2010,summer,day,imp,gsl,2000)
        197.767857142857    V_Activity(2010,summer,day,t,coal,1990)
         39.553571428571    V_Activity(2010,summer,day,t,elccar,2010)
          0.446428571429    V_Activity(2010,summer,day,t,gascar,2000)
   [ ... ]

Conversely, the modeler can redirect the *stdout* stream to a file, while still
receiving status information about the solve.  This way, the modeler can view
the output later, or post-process it as necessary.

.. code::

   $ ./temoa.py  test.dat  >  test.sol
   [    0.04] Reading data files.
   [        ] Creating Temoa model instance.Warning: ('t_oil_refinery', 2000) has a
   Warning: ('t_elccar', 2000) has a specified Efficiency, but does not have any ex
   Warning: ('t_oil_refinery', 2000) has a specified Efficiency, but does not have
   [    0.44
   [    0.81] Solving.
   [    0.86] Formatting results.

   $ head test.sol
   Model name: TEMOA Entire Energy System Economic Optimization Model
   Objective function value (TotalCost): 398469346.331
   Non-zero variable values:
        395.535714285714    V_Activity(2010,summer,day,imp,coal,2000)
          2.480158730159    V_Activity(2010,summer,day,imp,gsl,2000)
        197.767857142857    V_Activity(2010,summer,day,t,coal,1990)
         39.553571428571    V_Activity(2010,summer,day,t,elccar,2010)
          0.446428571429    V_Activity(2010,summer,day,t,gascar,2000)
         98.883928571429    V_Activity(2010,summer,night,imp,coal,2000)
          1.240079365079    V_Activity(2010,summer,night,imp,gsl,2000)

The next command line of real interest is :code:`--graph_format`.  If Graphviz
is installed on the machine, then specifying any output format that Graphviz
supports will generate set of graphs.  First, test if Graphviz is available,
then see what output formats it supports:

.. code::

   $ dot -V
   dot - graphviz version 2.26.3 (20100126.1600)

   $ dot -Txxx
   Format: "xxx" not recognized. Use one of: canon cmap cmapx cmapx_np dot eps
     fig gd gd2 gif gv imap imap_np ismap jpe jpeg jpg pdf plain plain-ext png
     ps ps2 svg svgz tk vml vmlz vrml wbmp x11 xdot xlib

From the list of available outputs, one might be interested in an interactive
map with SVG, so:

.. code::

   $ ./temoa.py  test.dat  --graph_format  svg  >  test.sol
   [    0.04] Reading data files.
   [        ] Creating Temoa model instance.Warning: ('t_oil_refinery', 2000) has a
   Warning: ('t_elccar', 2000) has a specified Efficiency, but does not have any ex
   Warning: ('t_oil_refinery', 2000) has a specified Efficiency, but does not have
   [    0.43
   [    0.81] Solving.
   [    0.86] Formatting results.
   [    0.93] Creating Temoa model diagrams.

The generated image might look like Figure 4.1.


Exactly What is Temoa Doing?
----------------------------

At some point, a modeler may be curious to open up the tiny file that is
``temoa.py`` to peek under the hood.  Luckily, ``temoa.py`` is merely a standard
ZIP file with 28 bytes of extra information to interoperate with Python.  This
means that a standard ZIP manipulation program can view and unpack the contents
of the archive:

.. code::

   $ unzip -l temoa.py
   Archive:  temoa.py
   warning [temoa.py]:  28 extra bytes at beginning or within zipfile
     (attempting to process anyway)
     Length      Date    Time    Name
   ---------  ---------- -----   ----
          19  2012-06-22 17:21   ReferenceModel.py
        4125  2012-06-22 17:21   pformat_results.py
       42167  2012-07-05 03:17   temoa_rules.py
        1698  2012-06-22 17:21   temoa_stochastic.py
       44670  2012-07-05 03:22   temoa_graphviz.py
       13910  2012-07-05 03:18   temoa_model.py
       30366  2012-07-05 04:29   temoa_lib.py
          86  2012-06-22 17:21   __main__.py
          52  2012-06-22 17:21   __init__.py
   ---------                     -------
      137093                     9 files

To work with the files, make a directory and unpack the archive:

.. code::

   $ mkdir temoa_model
   $ cd temoa_model/
   $ unzip ../temoa.py
   Archive:  ../temoa.py
   warning [../temoa.py]:  28 extra bytes at beginning or within zipfile
     (attempting to process anyway)
       linking: ReferenceModel.py       -> temoa_stochastic.py
     inflating: pformat_results.py
     inflating: temoa_rules.py
     inflating: temoa_stochastic.py
     inflating: temoa_graphviz.py
     inflating: temoa_model.py
     inflating: temoa_lib.py
     inflating: __main__.py
     inflating: __init__.py
   finishing deferred symbolic links:
     ReferenceModel.py      -> temoa_stochastic.py

   $ cd ..

If you want to make a change to Temoa, there is no need to repack it into
temoa.py.  Instead, Python can "execute" the directory directly:

.. code::

   $ coopr_python temoa_model
   usage: temoa_model [-h] [--graph_format GRAPH_FORMAT] [--show_capacity]
                      [--graph_type GRAPH_TYPE] [--use_splines]
                      dot_dat [dot_dat ...]
   temoa_model: error: too few arguments


The Bleeding Edge
-----------------

The Temoa Project uses the Git source code management system, and the services
of Github.com.  If you are inclined to work with the bleeding edge of the Temoa
Project code base, then take a look at the `Temoa repository`_.  To acquire a
copy, make sure you have Git installed on your local machine, then execute this
command to clone the repository:

.. code::

   $ git clone git://github.com/hunteke/temoa.git
   Cloning into 'temoa'...
   remote: Counting objects: 2386, done.
   remote: Compressing objects: 100% (910/910), done.
   remote: Total 2386 (delta 1552), reused 2280 (delta 1446)
   Receiving objects: 100% (2386/2386), 2.79 MiB | 1.82 MiB/s, done.
   Resolving deltas: 100% (1552/1552), done.

You will now have a new subdirectory called ``temoa``, that contains the entire
Temoa Project code and archive history.  Note that Git is a *distributed* source
code management tool.  This means that by cloning the Temoa repository, you have
your own copy to which you are welcome (and encouraged!) to alter and make
commits to.  It will not affect the source repository.

Though this is not a Git manual, we recognize that many readers of this manual
may not be software developers, so we offer a few quick pointers to using Git
effectively.

If you want to see the log of commits, use the command git log:

.. code::

   $ git log -1
   commit b5bddea7312c34c5c44fe5cce2830cbf5b9f0f3b
   Date:   Thu Jul 5 03:23:11 2012 -0400

       Update two APIs

        * I had updated the internal global variables to use the _psditvo
          naming scheme, and had forgotten to make the changes to _graphviz.py
        * Coopr also updated their API with the new .sparse_* methods.

You can also explore the various development branches in the repository:

.. code::

   $ ls
   data_files  stochastic  temoa_model  create_archive.sh  README.txt

   $ git branch -a
   * energysystem
     remotes/origin/HEAD -> origin/energysystem
     remotes/origin/energysystem
     remotes/origin/exp_electric_load_duration_reorg
     remotes/origin/exp_electricity_sector
     remotes/origin/exp_energysystem_flow_based
     remotes/origin/exp_energysystem_match_markal
     remotes/origin/exp_energysystem_test_framework
     remotes/origin/misc_scripts
     remotes/origin/old_energysystem_coopr2
     remotes/origin/temoaproject.org

   $ git checkout exp_energysystem_match_markal
   Branch exp_energysystem_match_markal set up to track remote branch
   exp_energysystem_match_markal from origin.
   Switched to a new branch 'exp_energysystem_match_markal'

   $ ls
   temoa_model                create_archive.sh     utopia-markal-20.dat
   compare_with_utopia-15.py  README.txt
   compare_with_utopia-20.py  utopia-markal-15.dat

To view exactly what changes you have made since the most recent commit to the
repository use the ``diff`` command to ``git``:

.. code::

   $ git diff
   diff --git a/temoa_model/temoa_lib.py b/temoa_model/temoa_lib.py
   index 4ff9b30..0ba15b0 100644
   --- a/temoa_model/temoa_lib.py
   +++ b/temoa_model/temoa_lib.py
   @@ -246,7 +246,7 @@ def InitializeProcessParameters ( M ):
                   if l_vin in M.vintage_exist:
                           if l_process not in l_exist_indices:
                                   msg = ('Warning: %s has a specified Efficiency, but does not '
   -                                 'have any existing install base (ExistingCapacity)\n.')
   +                                 'have any existing install base (ExistingCapacity).\n')
                                   SE.write( msg % str(l_process) )
                                   continue
                           if 0 == M.ExistingCapacity[ l_process ]:
    [ ... ]

This manual will not discuss the file format layout, or how to explicitly write
code for Temoa.  For that, please direct questions and discussion to the Temoa
user forum.


======================
Temoa Code Style Guide
======================

It is an open question in programming circles whether code formatting actually
matters.  The Temoa Project developers believe that it does for these main
reasons:

 * Consistently-formatted code reduces the cognitive work required to understand
   the structure and intent of a code base.  Specifically, we believe that
   before code is to be executed, it is to be understood by other humans.  The
   fact that it makes the computer do something useful is a (happy) coincidence.
 * Consistently-formatted code helps identify `code smell`_\ .
 * Consistently-formatted code helps one to spot code bugs and typos more
   easily.

Note, however, that this is a style `guide`, not a strict ruleset.  There will
also be corner cases to which a style guide does not apply, and in these cases,
the judgement of what to do is left to the implementers and maintainers of the
code base.  To this end, the Python project has a well-written treatise in `PEP
8`_\ :

   **A Foolish Consistency is the Hobgoblin of Little Minds**

   One of Guido's key insights is that code is read much more often than it is
   written.  The guidelines provided here are intended to improve the
   readability of code and make it consitent across the wide spectrum of Python
   code.  As PEP 20 says, "Readability counts".

   A style guide is about consistency.  Consistency with this style guide is
   important.  Consistency within a project is more important.  Consistency
   within one module or function is most important.

   But most importantly: know when to be inconsistent -- sometimes the style
   guide just doesn't apply.  When in doubt, use your best judgment.  Look at
   other examples and decide what looks best.  And don't hesitate to ask!

   Two good reasons to break a particular rule:

     1. When applying the rule would make the code less readable, even for
        someone who is used to reading code that follows the rules.
     2. To be consistent with surrounding code that also breaks it (maybe for
        historic reasons) -- although this is also an opportunity to clean up
        someone else's mess (in true XP style).


Indentation: Tabs and Spaces
----------------------------

The indentation of a section of code should always reflect the logical structure
of the code.  Python enforces this at a consistency level, but we make the
provision here that **real tabs** (specifically **not spaces**) should be used
at the beginning of lines.  This allows the most flexibility across text editors
and preferences for indentation width.

Spaces (and *not* tabs) should be used for mid-line spacing and alignment.

Many editors have functionality to highlight various whitespace characters.


End of Line Whitespace
----------------------

Remove it.  Many editors have plugins or builtin functionality that will take
care of this automatically when the file is saved.


Maximum Line Length
-------------------

(Similar to `PEP 8`_\ ) Limit all lines to a maximum of 80 characters.

Historically, 80 characters was the width (in monospace characters) that a
terminal had to display output.  With the advent of graphical user interfaces
with variable font-sizes, this technological limit no longer exists.  However,
80 characters remains an excellent metric of what constitutes a "long line."   A
long line in this sense is one that is not as transparent as to its intent as it
could be.  The 80-character width of code also represents a good "squint-test"
metric.  If a code-base has many lines longer than 80 characters, it may benefit
from a refactoring.

Slightly adapted from `PEP 8`_\ :

   The preferred way of wrapping long lines is by using Python's implied line
   continuation inside parentheses, brackets and braces.  Long lines can be
   broken over multiple lines by wrapping expressions in parentheses.  These
   should be used in preference to using a backslash for line continuation.
   Make sure to indent the continued line appropriately.  The preferred place to
   break around a binary operator is after the operator, not before it.  Some
   examples:

   .. code-block:: python

      class Rectangle ( Blob ):

         def __init__ ( self, width, height,
                        color='black', emphasis=None, highlight=0 ):
            if ( width == 0 and height == 0 and
                color == 'red' and emphasis == 'strong' or
                highlight > 100 ):
                raise ValueError("sorry, you lose")
            if width == 0 and height == 0 and (color == 'red' or
                                               emphasis is None):
                raise ValueError("I don't think so -- values are {}, {}".format(
                                 (width, height) ))
            Blob.__init__( self, width, height,
                          color, emphasis, highlight )


Blank Lines
-----------

 * Separate logical sections within a single function with a single blank line.
 * Separate function and method definitions with two blank lines.
 * Separate class definitions with three blank lines.


Encodings
---------

Following `PEP 3120`, all code files should use UTF-8 encoding.


Punctuation and Spacing
-----------------------

Always put spaces after code punctuation, like equivalence tests, assignments,
and index lookups.

.. code-block:: python

   a=b            # bad
   a = b          # good

   a==b           # bad
   a == b         # good

   a[b] = c       # bad
   a[ b ] = c     # good

      # exception: if there is more than one index
   a[ b, c ] = d  # acceptable, but not preferred
   a[b, c] = d    # good, preferred

      # exception: if using a string literal, don't include a space:
   a[ 'x' ] == d  # bad
   a['x'] == d    # good

When defining a function or method, put a single space on either side of each
parenthesis:

.. code-block:: python

   def someFunction(a, b, c):      # bad
      pass

   def someFunction ( a, b, c ):   # good
      pass


Vertical Alignment
------------------

*Where appropriate*, vertically align sections of the code.

.. code-block:: python

      # bad
   M.someVariable = Var( M.someIndex, domain=NonNegativeIntegers )
   M.otherVariable = Var( M.otherIndex, domain=NonNegativeReals )

      # good
   M.someVariable  = Var( M.someIndex,  domain=NonNegativeIntegers )
   M.otherVariable = Var( M.otherIndex, domain=NonNegativeReals )


Single, Double, and Triple Quotes
---------------------------------

Python has four delimiters to mark a string literal in the code: ``"``, ``'``,
``"""``, and |'''|.  Use each as appropriate.  One should rarely need to escape
a quote within a string literal, because one can merely alternate use of the
single, double or triple quotes:

.. code-block:: python

   a = "She said, \"Do not do that!\""  # bad
   a = 'She said, "Do not do that!"'    # good

   b = "She said, \"Don't do that!\""    # bad
   b = 'She said, "Don\'t do that!"'     # bad
   b = """She said, "Don't do that!\"""" # bad
   b = '''She said, "Don't do that!"'''  # good


.. _naming_conventions:

Naming Conventions
------------------

All constraints attached to a model should end with ``Constraint``.  Similarly,
the function they use to define the constraint for each index should use the
same prefix and ``Constraint`` suffix, but separate them with an underscore
(e.g. ``M.somenameConstraint = Constraint( ...,  rule=somename_Constraint``):

.. code-block:: python

   M.CapacityConstraint = Constraint( M.CapacityVar_tv, rule=Capacity_Constraint )

When providing the implementation for a constraint rule, use a consistent naming
scheme between functions and constraint definitions.  For instance, we have
already chosen ``M`` to represent the Pyomo model instance, ``t`` to represent
*technology*, and ``v`` to represent *vintage*:

.. code-block:: python

   def Capacity_Constraint ( M, t, v ):
      ...

The complete list we have already chosen:

 * :math:`p` to represent a period item from :math:`time\_optimize`
 * :math:`s` to represent a season item from :math:`time\_season`
 * :math:`d` to represent a time of day item from :math:`time\_of\_day`
 * :math:`i` to represent an input to a process, an item from
   :math:`commodity\_physical`
 * :math:`t` to represent a technology from :math:`tech\_all`
 * :math:`v` to represent a vintage from :math:`vintage\_all`
 * :math:`o` to represent an output of a process, an item from
   :math:`commodity\_carrier`

Note also the order of presentation, even in this list.  In order to reduce the
number mental "question marks" one might have while discovering Temoa, we
attempt to rigidly reference a mental model of "left to right".  Just as the
entire energy system that Temoa optimizes may be thought of as a left-to-right
graph, so too are the individual processes.  As said in section `A Word on Index
Ordering`_:

  For any indexed parameter or variable within Temoa, our intent is to enable a
  mental model of a left-to-right arrow-box-arrow as a simple mnemonic to
  describe the "input :math:`\rightarrow` process :math:`\rightarrow` output"
  flow of energy.  And while not all variables, parameters, or constraints have
  7 indices, the 7-index order mentioned here (p, s, d, i, t, v, o) is the
  canonical ordering.  If you note any case where, for example, d comes before
  s, that is an oversight.


In-line Implementation Conventions
----------------------------------

Wherever possible, implement the algorithm in a way that is *pedagogically*
sound or reads like an English sentence.  Consider this snippet:

.. code-block:: python

   if ( a > 5 and a < 10 ):
      doSomething()

In English, one might translate this snippet as "If a is greater than 5 and less
then 10, do something."  However, a semantically stronger implementation might
be:

.. code-block:: python

   if ( 5 < a and a < 10 ):
      doSomething()

This reads closer to the more familar mathematical notation of ``5 < a < 10``
and translates to English as "If a is between 5 and 10, do something."  The
semantic meaning that ``a`` should be *between* 5 and 10 is more readily
apparent from just the visual placement between 5 and 10, and is easier for the
"next person" to understand (who may very well be you in six months!).

Consider the reverse case:

.. code-block:: python

   if ( a < 5 or a > 10 ):
      doSomething()

On the number line, this says that a must fall before 5 or beyond 10.  But the
intent might more easily be understood if altered as above:

.. code-block:: python

   if not ( 5 < a and a < 10 ):
      doSomething()

This last snippet now makes clear the core question that a should ``not`` fall
between 5 and 10.

Consider another snippet:

.. code-block:: python

   acounter = scounter + 1

This method of increasing or incrementing a variable is one that many
mathematicians-turned-programmers prefer, but is more prone to error.  For
example, is that an intentional use of ``acounter`` or ``scounter``?  Assuming
as written that it's incorrect, a better paradigm uses the += operator:

.. code-block:: python

   acounter += 1

This performs the same operation, but makes clear that the ``acounter`` variable
is to be incremented by one, rather than be set to one greater than ``scounter``.

The same argument can be made for the related operators:

.. code-block:: python

   >>> a, b, c = 10, 3, 2

   >>> a += 5;  a    # same as a = a + 5
   15
   >>> a -= b;  a    # same as a = a - b
   12
   >>> a /= b;  a    # same as a = a / b
   4
   >>> a *= c;  a    # same as a = a * c
   8
   >>> a **= c; a    # same as a = a ** c
   64


Miscellanous Style Coventions
-----------------------------

 * (Same as `PEP 8`_\ ) Do not use spaces around the assignment operater (``=``)
   when used to indicate a default argument or keyword parameter:

   .. code-block:: python

      def complex ( real, imag = 0.0 ):         # bad
         return magic(r = real, i = imag)       # bad

      def complex ( real, imag=0.0 ):           # good
         return magic( r=real, i=imag )         # good

 * (Same as `PEP 8`_\ ) Do not use spaces immediately before the open
   parenthesis that starts the argument list of a function call:

   .. code-block:: python

      a = b.calc ()         # bad
      a = b.calc ( c )      # bad
      a = b.calc( c )       # good

 * (Same as `PEP 8`_\ ) Do not use spaces immediately before the open
   bracket that starts an indexing or slicing:

   .. code-block:: python

      a = b ['key']         # bad
      a = b [a, b]          # bad
      a = b['key']          # good
      a = b[a, b]           # good


Patches and Commits to the Repository
-------------------------------------

In terms of code quality and maintaining a legible "audit trail," every patch
should meet a basic standard of quality:

 * Every commit to the repository must include an appropriate summary message
   about the accompanying code changes.  Include enough context that one reading
   the patch need not also inspect the code to get a high-level understanding of
   the changes.  For example, "Fixed broken algorithm" does not convey much
   information.  A more appropriate and complete summary message might be::

      Fixed broken storage algorithm

      The previous implementation erroneously assumed that only the energy flow
      out of a storage device mattered.  However, Temoa needs to know the energy
      flow in to all devices so that it can appropriately calculate the
      inter-process commodity balance.

      License: AGPL-3.0

   If there is any external information that would be helpful, such as a bug
   report, include a "clickable" link to it, such that one reading the patch as
   via an email or online, can immediately view the external information.

   Specifically, commit messages should follow the form::

      A subject line of 50 characters or less
       [ an empty line ]
      * http://any.com/
      * http://relevant.org/some/path/
      * http://urls.edu/~some/other/path/

      Any amount and format of text, such that it conforms to a line-width of 72
      characters.  Bonus points for being aware of the Github Markdown syntax:
      https://github.com/blog/926-shiny-new-commit-styles

      License: AGPL-3.0

 * Ensure that each commit contains no more than one *logical* change to the
   code base.  This is very important for later auditing.  If you have not
   developed in a logical manner (like most of us don't), :code:`git add -p` is
   the answer

 * If you are not a core maintainer of the project, all commits must also
   include a specific reference to the license under which you are giving your
   code to the project.  Note that Temoa will not accept any patches that
   are not licensed under AGPL-3.0.  A line like this at the end of your commit
   will suffice::

      ... the last line of the commit message.

      License: AGPL-3.0

.. _OpenSourceNote:

=======================
A note on "Open Source"
=======================

Though Temoa's stature as an open source product is enforced by the AGPL, the
code is only half the battle.  The other half involves the exact input fed to
Temoa to create an analysis, and there is no method available to require
modelers to share the inner workings of their analyses.

Specifically, this means that if a modeling team makes changes to the Temoa
codebase, and publishes an analysis based on them, their is no legal requirement
to share either the code or the input data.  To that end, all we can do is plea
to modeling teams to "do the right thing", and be transparent about all aspects
of an analysis.


.. rubric:: Footnotes

.. [#open_source_realities] The two main goals behind Temoa are transparency and
   recreatability, hence the AGPL license.  Unfortunately, there are some harsh
   realities in the current climate of EEO modeling, so this license is not a
   guarantee of openness.  This documentation touches on the issues involved in
   the final section, :ref:`OpenSourceNote`.

.. [#elided_math] However, the code is freely inspectable: ``temoa_lib.py``.
   You are also welcome to inquire on the Temoa Project forum.  Please see
   http://temoaproject.org/ for a link.

.. [#efficiency_table] The efficiency parameter is often refered to as the
   efficiency table, due to how it looks after even only a few entries in the
   Pyomo input "dot dat" file.

.. [#glpk_presolve] Circa 2012, GLPK uses more memory than commercial
   alternatives and has vastly weaker presolve capabilities.

.. [#eeo_definition] For a more in-depth description of EEO models and their
   place in the energy modeling community, as well as references to other papers
   and sources, see "The TEMOA Project: Tools for Energy Model Optimization and
   Analysis", by DeCarolis, J. and Hunter, K. and Sreepathi, S. (2010).
   (Available from `temoaproject.org/`_.)

.. [#union] Specifically, :math:`time\_optimize` is the union of the ordered
   sets :math:`time\_horizon` and :math:`time\_future`, less the last element of
   the latter, so as to be able to calculate a period length for the final
   element in :math:`time\_optimize`.

.. [#units_comparison] There is an open ticket to address the lack of unit
   awareness in Temoa.  See `issue 5`_ in our issue tracker.

.. [#web_browser_svg] SVG support in web browsers is currently hit or miss.  The
   most recent versions of Chromium, Google Chrome, and Mozilla Firefox support
   SVG well enough for Temoa's current use of SVG.

.. [#return_expression] A word on `return` expressions in Pyomo: in most
   contexts a relational expression is evaluated instantly.  However, in Pyomo,
   a relational expression returns an `expression` object.  That is, `'M.aVar >=
   5'` does not evaluate to a boolean *true* or *false*, and Pyomo will
   manipulate it into the final LP formulation.

.. |'''| replace:: ``'``\ ``'``\ ``'``

.. _GNU Linear Programming Kit: https://www.gnu.org/software/glpk/
.. _WinGLPK: http://winglpk.sf.net/
.. _Temoa model: http://temoaproject.org/download/temoa.py
.. _example data sets: http://temoaproject.org/download/example_data_sets.zip
.. _temoaproject.org/: http://temoaproject.org/
.. _mailing list: https://groups.google.com/forum/#!forum/temoa-project
.. _various: http://xlinux.nist.gov/dads/HTML/optimization.html
.. _available: http://www.solver.com/probtype.htm
.. _online: https://en.wikipedia.org/wiki/Optimization_problem
.. _sources: https://en.wikipedia.org/wiki/Mathematical_optimization
.. _GAMS: http://www.gams.com/
.. _AMPL: http://www.ampl.com/
.. _PDF: http://temoaproject.org/downloads/TemoaDocumentation.pdf
.. _HTML: http://temoaproject.org/docs/
.. _Github Issue tracker: https://github.com/hunteke/temoa/issues
.. _HTML version: http://temoaproject.org/docs/
.. _code smell: https://en.wikipedia.org/wiki/Code_smell
.. _PEP 8: http://www.python.org/dev/peps/pep-0008/
.. _PEP 3120: http://www.python.org/dev/peps/pep-3120/
.. _list comprehension: http://docs.python.org/tutorial/datastructures.html#list-comprehensions
.. _lambda function: http://docs.python.org/tutorial/controlflow.html#lambda-forms
.. _Tarbomb: https://en.wikipedia.org/wiki/Tar_(file_format)#Tarbom
.. _generally accepted relative rates: http://www.forecasts.org/inflation.htm
.. _Temoa repository: https://github.com/hunteke/temoa/
.. _issue 5: https://github.com/hunteke/temoa/issues/5
