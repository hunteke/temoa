"""
Temoa - Tools for Energy Model Optimization and Analysis
  linear optimization; least cost; dynamic system visualization

Copyright (C) 2011-2014  Kevin Hunter, Joseph DeCarolis

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.

Developers of this script will check out a complete copy of the GNU Affero
General Public License in the file COPYING.txt.  Users uncompressing this from
an archive may not have received this license file.  If not, see
<http://www.gnu.org/licenses/>.
"""

from temoa_lib import *

##############################################################################
# Begin *_rule definitions

def TotalCost_rule ( M ):
	r"""

Using the :code:`Activity` and :code:`Capacity` variables, the Temoa objective
funciton calculates the costs associated with supplying the system with energy,
under the assumption that all costs are paid for through loans (rather than with
lump-sum sales).  This implementation sums up all the costs incurred by the
solution, and is defined as :math:`C_{tot} = \text{C}_\text{loans} +
\text{C}_\text{fixed} + \text{C}_\text{variable}`.  Similarly, each term on the
right-hand side is merely a summation of the costs incurred, multiplied by an
annual discount factor to calculate the discounted cost in year
:math:`\text{P}_0`.

.. math::
   C_{loans} & = \sum_{t, v \in \Theta_{IC}} \left (
     \left [
             IC_{t, v}
       \cdot LA_{t, v}
       \cdot {\sum_{y = v - P_0}^{v - P_0 + MLL_{t, v}}
                 \left ( \frac{1}{(1 + GDR)^y} \right ) }
     \right ]
     \cdot \textbf{CAP}_{t, v}
     \right )

.. math::
   C_{fixed} & = \sum_{p, t, v \in \Theta_{FC}} \left (
     \left [
             FC_{p, t, v}
       \cdot {\sum_{y = v - P_0}^{v - P_0 + TPL_{t, v}}
                 \left ( \frac{1}{(1 + GDR)^y} \right ) }
     \right ]
     \cdot \textbf{CAP}_{t, v}
     \right )

.. math::
   C_{variable} & = \sum_{p, t, v \in \Theta_{VC}} \left (
           MC_{p, t, v}
     \cdot R_p
     \cdot \textbf{ACT}_{t, v}
     \right )

In the last sub-equation, :math:`R_p` is the equivalent operation to the inner
summation of the other two sub-equations.  The difference is that where the
inner summations specifically account for the fixed and loan costs of
partial-period processes, the activity is constant for all years within a
period.  There is thus no need to calculate the time-value of money factor for
each process, and instead, :math:`R_p` is calculated once for each period, as a
pseudo-parameter.  While this amounts to little more than an efficiency of model
generation, it is pedogogically significant in that it highlights the fact that
Temoa optimizes only a single characteristic year within each period.

"""
	return sum( PeriodCost_rule(M, p) for p in M.time_optimize )


def PeriodCost_rule ( M, p ):
	P_0 = min( M.time_optimize )
	GDR = value( M.GlobalDiscountRate )

	loan_costs = sum(
	    M.V_Capacity[S_t, S_v]
	  * (
	      value( M.CostInvest[S_t, S_v] )
	    * value( M.LoanAnnualize[S_t, S_v] )
	    * sum( (1 + GDR) ** -y
	        for y in range( S_v - P_0,
	                        S_v - P_0 + value( M.ModelLoanLife[S_t, S_v] ))
	      )
	  )

	  for S_t, S_v in M.CostInvest.sparse_iterkeys()
	  if S_v == p
	)

	fixed_costs = sum(
	    M.V_Capacity[S_t, S_v]
	  * (
	      value( M.CostFixed[p, S_t, S_v] )
	    * sum( (1 + GDR) ** -y
	        for y in range( p - P_0,
	                        p - P_0 + value( M.ModelTechLife[p, S_t, S_v] ))
	      )
	    )

	  for S_p, S_t, S_v in M.CostFixed.sparse_iterkeys()
	  if S_p == p
	)

	variable_costs = sum(
	    M.V_ActivityByPeriodTechAndVintage[p, S_t, S_v]
	  * (
	      value( M.CostVariable[p, S_t, S_v] )
	    * value( M.PeriodRate[ p ] )
	  )

	  for S_p, S_t, S_v in M.CostVariable.sparse_iterkeys()
	  if S_p == p
	)

	period_costs = (loan_costs + fixed_costs + variable_costs)
	return period_costs


##############################################################################
#   Initializaton rules


def ParamModelLoanLife_rule ( M, t, v ):
	loan_length = value( M.LifetimeLoan[t, v] )
	mll = min( loan_length, max(M.time_future) - v )

	return mll


def ParamModelTechLife_rule ( M, p, t, v ):
	life_length = value( M.LifetimeTech[t, v] )
	tpl = min( v + life_length - p, value(M.PeriodLength[ p ]) )

	return tpl


def ParamPeriodLength ( M, p ):
	# This specifically does not use time_optimize because this function is
	# called /over/ time_optimize.
	periods = sorted( M.time_future )

	i = periods.index( p )

	# The +1 won't fail, because this rule is called over time_optimize, which
	# lacks the last period in time_future.
	length = periods[i +1] - periods[ i ]

	return length


def ParamPeriodRate ( M, p ):
	"""\
The "Period Rate" is a multiplier against the costs incurred within a period to
bring the time-value back to the base year.  The parameter PeriodRate is not
directly specified by the modeler, but is a convenience calculation based on the
GlobalDiscountRate and the length of each period.  One may refer to this
(pseudo) parameter via M.PeriodRate[ a_period ]
"""
	rate_multiplier = sum(
	  (1 + M.GlobalDiscountRate) ** (M.time_optimize.first() - p - y)

	  for y in range(0, M.PeriodLength[ p ])
	)

	return value(rate_multiplier)


def ParamTechLifeFraction_rule ( M, p, t, v ):
	"""\

Calculate the fraction of period p that process <t, v> operates.

For most processes and periods, this will likely be one, but for any process
that will cease operation (rust out, be decommissioned, etc.) between periods,
calculate the fraction of the period that the technology is able to
create useful output.
"""
	eol_year = v + value( M.LifetimeTech[t, v] )
	frac  = eol_year - p
	period_length = value( M.PeriodLength[ p ] )
	if frac >= period_length:
		# try to avoid floating point round-off errors for the common case.
		return 1

	  # number of years into final period loan is complete

	frac /= float( period_length )
	return frac


def ParamLoanAnnualize_rule ( M, t, v ):
	dr = value( M.DiscountRate[t, v] )
	lln = value( M.LifetimeLoan[t, v] )
	if not dr:
		return 1 / lln
	annualized_rate = ( dr / (1 - (1 + dr)**(-lln) ))

	return annualized_rate

# End initialization rules
##############################################################################

##############################################################################
#   Constraint rules

def BaseloadDiurnal_Constraint ( M, p, s, d, t, v ):
	r"""
There exists within the electric sector a class of technologies whose
thermodynamic properties are impossible to change over a short period of time
(e.g.  hourly or daily).  These include coal and nuclear power plants, which
take weeks to bring to an operational state, and similarly require weeks to
fully shut down.  Temoa models this behavior by forcing technologies in the
:code:`tech_baseload` set to maintain a constant output for all daily slices.
Note that this allows the model to (not) use a baseload process in a season, and
only applies over the :code:`time_of_day` set.

Ideally, this constraint would not be necessary, and baseload processes would
simply not have a :math:`d` index.  However, implementing the more efficient
functionality is currently on the Temoa TODO list.

.. math::
   :label: BaseloadDaily

         SEG_{s, D_0}
   \cdot \textbf{ACT}_{p, s, d, t, v}
   =
         SEG_{s, d}
   \cdot \textbf{ACT}_{p, s, D_0, t, v}

   \\
   \forall \{p, s, d, t, v\} \in \Theta_{\text{baseload}}
"""
	# Question: How to set the different times of day equal to each other?

	# Step 1: Acquire a "canonical" representation of the times of day
	l_times = sorted( M.time_of_day )  # i.e. a sorted Python list.
	  # This is the commonality between invocations of this method.

	index = l_times.index( d )
	if 0 == index:
		# When index is 0, it means that we've reached the beginning of the array
		# For the algorithm, this is a terminating condition: do not create
		# an effectively useless constraint
		return Constraint.Skip

	# Step 2: Set the rest of the times of day equal in output to the first.
	# i.e. create a set of constraints that look something like:
	# tod[ 2 ] == tod[ 1 ]
	# tod[ 3 ] == tod[ 1 ]
	# tod[ 4 ] == tod[ 1 ]
	# and so on ...
	d_0 = l_times[ 0 ]

	# Step 3: the actual expression.  For baseload, must compute the /average/
	# activity over the segment.  By definition, average is
	#     (segment activity) / (segment length)
	# So:   (ActA / SegA) == (ActB / SegB)
	#   computationally, however, multiplication is cheaper than division, so:
	#       (ActA * SegB) == (ActB * SegA)
	expr = (
	    M.V_Activity[p, s, d, t, v]   * M.SegFrac[s, d_0]
	 ==
	    M.V_Activity[p, s, d_0, t, v] * M.SegFrac[s, d]
	)
	return expr


def EmissionLimit_Constraint ( M, p, e ):
	r"""

A modeler can track emissions through use of the :code:`commodity_emissions`
set and :code:`EmissionActivity` parameter.  The :math:`EAC` parameter is
analogous to the efficiency table, tying emissions to a unit of activity.  The
EmissionLimit constraint allows the modeler to assign an upper bound per period
to each emission commodity.

.. math::
   :label: EmissionLimit

   \sum_{I,T,V,O|{e,i,t,v,o} \in EAC_{ind}} \left (
       EAC_{e, i, t, v, o} \cdot \textbf{FO}_{p, s, d, i, t, v, o}
     \right )
     \le
     ELM_{p, e}

   \\
   \forall \{p, e\} \in ELM_{ind}
"""
	emission_limit = M.EmissionLimit[p, e]

	actual_emissions = sum(
	    M.V_FlowOut[p, S_s, S_d, S_i, S_t, S_v, S_o]
	  * M.EmissionActivity[e, S_i, S_t, S_v, S_o]

	  for tmp_e, S_i, S_t, S_v, S_o in M.EmissionActivity.sparse_iterkeys()
	  if tmp_e == e
	  if ValidActivity( p, S_t, S_v )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	if int is type( actual_emissions ):
		msg = ("Warning: No technology produces emission '%s', though limit was "
		  'specified as %s.\n')
		SE.write( msg % (e, emission_limit) )
		return Constraint.Skip

	expr = (actual_emissions <= emission_limit)
	return expr


def MinCapacity_Constraint ( M, p, t ):
	r""" See MaxCapacity_Constraint """

	min_cap = value( M.MinCapacity[p, t] )
	expr = (M.V_CapacityAvailableByPeriodAndTech[p, t] >= min_cap)
	return expr


def MaxCapacity_Constraint ( M, p, t ):
	r"""

The MinCapacity and MaxCapacity constraints set limits on the what the model is
allowed to (not) have available of a certain technology.  Note that the indices
for these constraints are period and tech_all, not tech and vintage.

.. math::
   :label: MinCapacity

   \textbf{CAPAVL}_{p, t} \ge MIN_{p, t}

   \forall \{p, t\} \in \Theta_{\text{MinCapacity parameter}}

.. math::
   :label: MaxCapacity

   \textbf{CAPAVL}_{p, t} \le MAX_{p, t}

   \forall \{p, t\} \in \Theta_{\text{MaxCapacity parameter}}
"""
	max_cap = value( M.MaxCapacity[p, t] )
	expr = (M.V_CapacityAvailableByPeriodAndTech[p, t] <= max_cap)
	return expr


def Storage_Constraint ( M, p, s, i, t, v, o ):
	r"""

Temoa's algorithm for storage is to ensure that the amount of energy entering
and leaving a storage technology is balanced over the course of a day,
accounting for the conversion efficiency of the storage process.  This

constraint relies on the assumption that the total amount of storage-related
energy is small compared to the amount of energy required by the system over a
season.  If it were not, the algorithm would have to account for
season-to-season transitions, which would require an ordering of seasons within
the model. Currently, each slice is completely independent of other slices.

.. math::
   :label: Storage

   \sum_{D} \left (
            EFF_{i, t, v, o}
      \cdot \textbf{FI}_{p, s, d, i, t, v, o}
      -     \textbf{FO}_{p, s, d, i, t, v, o}
   \right )
   = 0

   \forall \{p, s, i, t, v, o\} \in \Theta_{\text{storage}}
"""
	total_out_in = sum(
	    M.Efficiency[i, t, v, o]
	  * M.V_FlowIn[p, s, S_d, i, t, v, o]
	  - M.V_FlowOut[p, s, S_d, i, t, v, o]

	  for S_d in M.time_of_day
	)

	expr = ( total_out_in == 0 )
	return expr


def TechInputSplit_Constraint ( M, p, s, d, i, t, v, o ):
	r"""

Some processes take a single output and make multiple inputs.  A subset of these
processes have a constant ratio of outputs relative to their input.  See
TechOutputSplit_Constraint for the analogous math reasoning.
"""
	split_indices = M.TechInputSplit.sparse_keys()

	inputs = sorted(
	  inp

	  for inp in M.commodity_physical
	  if (inp, t, o) in split_indices
	)

	index = inputs.index( i )
	if 0 == index:
		return Constraint.Skip

	prev = inputs[ index -1 ]
	prev_split = M.TechInputSplit[prev, t, o]
	split = M.TechInputSplit[i, t, o]

	expr = (
	    M.V_FlowIn[p, s, d, i, t, v, o]
	  * split
	  ==
	    M.V_FlowIn[p, s, d, prev, t, v, o]
	  * prev_split
	)
	return expr


def TechOutputSplit_Constraint ( M, p, s, d, i, t, v, o ):
	r"""

Some processes take a single input and make multiple outputs.  A subset of
these processes have a constant ratio of outputs relative to their input.  The
most canonical example is that of an oil refinery.  Crude oil is composed of
many different types of hydrocarbons, and the refinery process exploits the fact
that they each have a different boiling point.  The amount of each type of
product that a refinery produces is thus directly related to the makeup of the
crude oil input.

The TechOutputSplit constraint assumes that the input to any process of interest
has a constant ratio output.  For example, a hypothetical (and highly
simplified) refinery might have a crude oil input that only contains 4 parts
diesel, 3 parts gasoline, and 2 parts kerosene.  The relative ratios to the
output then are:

.. math::

   d = \tfrac{4}{9} \cdot \text{total output}, \qquad
   g = \tfrac{3}{9} \cdot \text{total output}, \qquad
   k = \tfrac{2}{9} \cdot \text{total output}

Using the total output as the commonality, these can then be compared to each
other:

.. math::
   \tfrac{9}{4} \cdot d = \tfrac{9}{3} \cdot g = \tfrac{9}{2} \cdot k
   = \text{total}

Finally, in constraint form:

.. math::
   \tfrac{9}{3} d &= \tfrac{9}{4} g \\
   \tfrac{9}{2} d &= \tfrac{9}{4} k

Generalized, the constraint in set notation is:

.. math::
   :label: TechOutputSplit


     SPL_{i, t, o} \cdot \textbf{FO}_{p, s, d, i, t, v, o_0}
   =
     SPL_{i, t, o_0} \cdot \textbf{FO}_{p, s, d, i, t ,v, o}

   \forall \{p, s, d, i, t, v, o\} \in \Theta_{\text{split output}}
"""
	split_indices = M.TechOutputSplit.sparse_keys()

	outputs = sorted(
	  output

	  for output in M.commodity_carrier
	  if (i, t, output) in split_indices
	)

	index = outputs.index( o )
	if 0 == index:
		return Constraint.Skip

	prev = outputs[ index -1 ]
	prev_split = M.TechOutputSplit[i, t, prev]
	split = M.TechOutputSplit[i, t, o]

	expr = (
	    M.V_FlowOut[p, s, d, i, t, v, o]
	  * split
	  ==
	    M.V_FlowOut[p, s, d, i, t, v, prev]
	  * prev_split
	)
	return expr


def Activity_Constraint ( M, p, s, d, t, v ):
	r"""
The Activity constraint defines the Activity convenience variable.  The Activity
variable is mainly used in the objective function to calculate the cost
associated with use of a technology.  In English, this constraint states that
"the activity of a process is the sum of its outputs."

There is one caveat to keep in mind in regards to the Activity variable: if
there is more than one output, there is currently no attempt by Temoa to convert
to a common unit of measurement.  For example, common measurements for heat
include mass of steam at a given tempurature, or total BTUs, while electricity
is generally measured in a variant of watt-hours.  Reconciling these units of
measurement, as for example with a cogeneration plant, is currently left as an
accounting exercise for the modeler.

.. math::
   :label: Activity

   \textbf{ACT}_{p, s, d, t, v} = \sum_{I, O} \textbf{FO}_{p,s,d,i,t,v,o}

   \\
   \forall \{p, s, d, t, v\} \in \Theta_{\text{activity}}
"""
	activity = sum(
	  M.V_FlowOut[p, s, d, S_i, t, v, S_o]

	  for S_i in ProcessInputs( p, t, v )
	  for S_o in ProcessOutputsByInput( p, t, v, S_i )
	)

	expr = ( M.V_Activity[p, s, d, t, v] == activity )
	return expr


def Capacity_Constraint ( M, p, s, d, t, v ):
	r"""

Temoa's definition of a process' capacity is the total size of installation
required to meet all of that process' demands.  The Activity convenience
variable represents exactly that, so the calculation on the left hand side of
the inequality is the maximum amount of energy a process can produce in the time
slice ``<s``,\ ``d>``.

.. math::
   :label: Capacity

       \left (
               \text{CF}_{t, v}
         \cdot \text{C2A}_{t}
         \cdot \text{SEG}_{s, d}
         \cdot \text{TLF}_{p, t, v}
       \right )
       \cdot \textbf{CAP}_{t, v}
   \ge
       \textbf{ACT}_{p, s, d, t, v}

   \\
   \forall \{p, s, d, t, v\} \in \Theta_{\text{activity}}
"""
	produceable = (
	  (   value( M.CapacityFactor[s, d, t, v] )
	    * value( M.CapacityToActivity[ t ] )
	    * value( M.SegFrac[s, d]) )
	    * value( M.TechLifeFrac[p, t, v] )
	  * M.V_Capacity[t, v]
	)

	expr = (produceable >= M.V_Activity[p, s, d, t, v])
	return expr


def ExistingCapacity_Constraint ( M, t, v ):
	r"""

Temoa treats residual capacity from before the model's optimization horizon as
regular processes, that require the same parameter specification in the data
file as do new vintage technologies (e.g. entries in the efficiency table),
except the :code:`CostInvest` parameter.  This constraint sets the capacity of
processes for model periods that exist prior to the optimization horizon to
user-specified values.

.. math::
   :label: ExistingCapacity

   \textbf{CAP}_{t, v} = ECAP_{t, v}

   \forall \{t, v\} \in \Theta_{\text{existing}}
"""
	expr = ( M.V_Capacity[t, v] == M.ExistingCapacity[t, v] )
	return expr


def ResourceExtraction_Constraint ( M, p, r ):
	r"""

The ResourceExtraction constraint allows a modeler to specify an annual limit on
the amount of a particular resource Temoa may use in a period.

.. math::
   :label: ResourceExtraction

   \sum_{S, D, I, t \in T^r, V} \textbf{FO}_{p, s, d, i, t, v, c} \le RSC_{p, c}

   \forall \{p, c\} \in \Theta_{\text{resource bound parameter}}
"""
	collected = sum(
	  M.V_FlowOut[p, S_s, S_d, S_i, S_t, S_v, r]

	  for S_t, S_v in ProcessesByPeriodAndOutput( p, r )
	  if S_t in M.tech_resource
	  for S_i in ProcessInputsByOutput( p, S_t, S_v, r )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	expr = (collected <= M.ResourceBound[p, r])
	return expr


def CommodityBalance_Constraint ( M, p, s, d, c ):
	r"""

Where the Demand constraint :eq:`Demand` ensures that end-use demands are met,
the CommodityBalance constraint ensures that the internal system demands are
met.  That is, this is the constraint that ties the output of one process to the
input of another.  At the same time, this constraint also conserves energy
between process.  (But it does not account for transmission loss.)  In this
manner, it is a corollary to both the ProcessBalance :eq:`ProcessBalance` and
Demand :eq:`Demand` constraints.

.. math::
   :label: CommodityBalance

   \sum_{I, T, V} \textbf{FO}_{p, s, d, i, t, v, c}
   \ge
   \sum_{T, V, O} \textbf{FI}_{p, s, d, c, t, v, o}

   \\
   \forall \{p, s, d, c\} \in \Theta_{\text{commodity balance}}
"""
	if c in M.commodity_demand:
		return Constraint.Skip

	vflow_in = sum(
	  M.V_FlowIn[p, s, d, c, S_t, S_v, S_o]

	  for S_t in M.tech_production
	  for S_v in M.vintage_all
	  for S_o in ProcessOutputsByInput( p, S_t, S_v, c )
	)

	vflow_out = sum(
	  M.V_FlowOut[p, s, d, S_i, S_t, S_v, c]

	  for S_t in M.tech_all
	  for S_v in M.vintage_all
	  for S_i in ProcessInputsByOutput( p, S_t, S_v, c )
	)

	CommodityBalanceConstraintErrorCheck( vflow_out, vflow_in, p, s, d, c )

	expr = (vflow_out >= vflow_in)
	return expr


def ProcessBalance_Constraint ( M, p, s, d, i, t, v, o ):
	r"""

The ProcessBalance constraint is one of the most fundamental constraints in the
Temoa model.  It defines the basic relationship between the energy entering a
process (:math:`\textbf{FI}`) and the energy leaving a processing
(:math:`\textbf{FO}`). This constraint sets the :code:`FlowOut` variable, upon
which all other constraints rely.

Conceptually, this constraint treats every process as a "black box," caring only
about the process efficiency. In other words, the amount of energy leaving a
process cannot exceed the amount coming in.

Note that this constraint is an inequality -- not a strict equality.  In most
sane cases, the optimal solution should make this constraint and supply should
exactly meet demand.  If this constraint is not binding, it is likely a clue
that the model under inspection could be more tightly specified and has at least
one input data anomaly.

.. math::
   :label: ProcessBalance

          \textbf{FO}_{p, s, d, i, t, v, o}
   \le
          EFF_{i, t, v, o}
    \cdot \textbf{FI}_{p, s, d, i, t, v, o}

   \\
   \forall \{p, s, d, i, t, v, o\} \in \Theta_{\text{valid process flows}}
"""
	expr = (
	    M.V_FlowOut[p, s, d, i, t, v, o]
	      <=
	    M.V_FlowIn[p, s, d, i, t, v, o]
	  * value( M.Efficiency[i, t, v, o] )
	)

	return expr


def DemandActivity_Constraint ( M, p, s, d, t, v, dem, s_0, d_0 ):
	r"""

For end-use demands, it is unreasonable to let the optimizer only allow use in a
single time slice.  For instance, if household A buys a natural gas furnace
while household B buys an electric furnace, then both units should be used
throughout the year.  Without this constraint, the model might choose to only
use the electric furnace during the day, and the natural gas furnace during the
night.

This constraint ensures that the ratio of a process activity to demand is
constant for all time slices.  Note that if a demand is not specified in a given
time slice, or is zero, then this constraint will not be considered for that
slice and demand.  This is transparently handled by the :math:`\Theta` superset.

.. math::
   :label: DemandActivity

      DEM_{p, s, d, dem} \cdot \sum_{I} \textbf{FO}_{p, s_0, d_0, i, t, v, dem}
   =
      DEM_{p, s_0, d_0, dem} \cdot \sum_{I} \textbf{FO}_{p, s, d, i, t, v, dem}

   \\
   \forall \{p, s, d, t, v, dem, s_0, d_0\} \in \Theta_{\text{demand activity}}
"""

	DSD = M.DemandSpecificDistribution   # lazy programmer
	act_a = sum(
	  M.V_FlowOut[p, s_0, d_0, S_i, t, v, dem]

	  for S_i in ProcessInputsByOutput( p, t, v, dem )
	)
	act_b = sum(
	  M.V_FlowOut[p, s, d, S_i, t, v, dem]

	  for S_i in ProcessInputsByOutput( p, t, v, dem )
	)

	expr = (
	  act_a * DSD[s, d, dem]
	     ==
	  act_b * DSD[s_0, d_0, dem]
	)
	return expr


def Demand_Constraint ( M, p, s, d, dem ):
	r"""

The Demand constraint drives the model.  This constraint ensures that supply at
least meets the demand specified by the Demand parameter in all periods and
slices, by ensuring that the sum of all the demand output commodity (:math:`c`)
generated by :math:`\textbf{FO}` must meet the modeler-specified demand, in
each time slice.

.. math::
   :label: Demand

   \sum_{I, T, V} \textbf{FO}_{p, s, d, i, t, v, dem}
   \ge
   {DEM}_{p, dem} \cdot {DSD}_{s, d, dem}

   \\
   \forall \{p, s, d, dem\} \in \Theta_{\text{demand}}

Note that the validity of this constraint relies on the fact that the
:math:`C^d` set is distinct from both :math:`C^e` and :math:`C^p`. In other
words, an end-use demand must only be an end-use demand.  Note that if an output
could satisfy both an end-use and internal system demand, then the output from
:math:`\textbf{FO}` would be double counted.

Note also that this constraint is an inequality, not a strict equality.  "Supply
must meet or exceed demand."  Like with the ProcessBalance constraint, if this
constraint is not binding, it may be a clue that the model under inspection
could be more tightly specified and could have at least one input data anomaly.

"""
	supply = sum(
	  M.V_FlowOut[p, s, d, S_i, S_t, S_v, dem]

	  for S_t in M.tech_all
	  for S_v in M.vintage_all
	  for S_i in ProcessInputsByOutput( p, S_t, S_v, dem )
	)

	DemandConstraintErrorCheck( supply, p, s, d, dem )

	expr = (supply >= M.Demand[p, dem] * M.DemandSpecificDistribution[s, d, dem])

	return expr


def GrowthRateConstraint_rule ( M, p, t ):
	GRS = value( M.GrowthRateSeed[ t ] )
	GRM = value( M.GrowthRateMax[ t ] )
	CapPT = M.V_CapacityAvailableByPeriodAndTech

	periods = sorted(set(p_ for p_, t_ in CapPT if t_ == t) )

	if p not in periods:
		return Constraint.Skip

	if p == periods[0]:
		expr = ( CapPT[p, t] <= GRS )

	else:
		p_prev = periods.index( p )
		p_prev = periods[ p_prev -1]

		expr = ( CapPT[p, t] <= GRM * CapPT[p_prev, t] + GRS )

	return expr


##############################################################################
# Additional and derived (informational) variable constraints


def ActivityByPeriodTechAndVintage_Constraint ( M, p, t, v ):
	if p < v or v not in ProcessVintages( p, t ):
		return Constraint.Skip

	activity = sum(
	  M.V_Activity[p, S_s, S_d, t, v]

	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	if int is type( activity ):
		return Constraint.Skip

	expr = (M.V_ActivityByPeriodTechAndVintage[p, t, v] == activity)
	return expr


def CapacityAvailableByPeriodAndTech_Constraint ( M, p, t ):
	r"""
The :math:`\textbf{CAPAVL}` variable is nominally for reporting solution values,
but is also used in the Max and Min constraint calculations.  For any process
with an end-of-life (EOL) on a period boundary, all of its capacity is available
for use in all periods in which it is active (the process' TLF is 1). However,
for any process with an EOL that falls between periods, Temoa makes the
simplifying assumption that the available capacity from the expiring technology
is available through the whole period, but only as much percentage as its
lifespan through the period.  For example, if a process expires 3 years into an
8 year period, then only :math:`\frac{3}{8}` of the installed capacity is
available for use throughout the period.

.. math::
   :label: CapacityAvailable

   \textbf{CAPAVL}_{p, t} = \sum_{V} {TLF}_{p, t, v} \cdot \textbf{CAP}

   \\
   \forall p \in \text{P}^o, t \in T
"""
	cap_avail = sum(
	    value( M.TechLifeFrac[p, t, S_v] )
	  * M.V_Capacity[t, S_v]

	  for S_v in ProcessVintages( p, t )
	)

	expr = (M.V_CapacityAvailableByPeriodAndTech[p, t] == cap_avail)
	return expr


# End additional and derived (informational) variable constraints
##############################################################################

# End *_rule definitions
##############################################################################

