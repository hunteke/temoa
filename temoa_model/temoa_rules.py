"""
Tools for Energy Model Optimization and Analysis (Temoa): 
An open source framework for energy systems optimization modeling

Copyright (C) 2015,  NC State University

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

A complete copy of the GNU General Public License v2 (GPLv2) is available 
in LICENSE.txt.  Users uncompressing this from an archive may not have 
received this license file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Import below required in Python 2.7 to avoid integer division
# (e.g., 1/2 = 0 instead of 0.5)
from __future__ import division

from temoa_initialize import *
# ---------------------------------------------------------------
# Define the derived variables used in the objective function
# and constraints below.
# ---------------------------------------------------------------

def Activity_Constraint(M, p, s, d, t, v):
    r"""

The Activity constraint defines the Activity convenience variable.  The Activity
variable is mainly used in the objective function to calculate the cost
associated with use of a technology.  This constraint sums the 
:math:`\textbf{FO}_{p,s,d,i,t,v,o}` over all input and output commodities.

There is one caveat to keep in mind in regards to the Activity variable: if
there is more than one output, there is currently no attempt by Temoa to convert
to a common unit of measurement.  For example, common measurements for heat
include mass of steam at a given temperature, or total BTUs, while electricity
is generally measured in a variant of watt-hours.  Reconciling these units of
measurement, as for example with a cogeneration plant, is currently left as an
accounting exercise for the modeler.

.. math::
   :label: Activity

   \textbf{ACT}_{p, s, d, t, v} = \sum_{I, O} \textbf{FO}_{p,s,d,i,t,v,o}

   \\
   \forall \{p, s, d, t, v\} \in \Theta_{\text{Activity}}
"""
    return sum( \
        M.V_FlowOut[p, s, d, S_i, t, v, S_o] \
        for S_i in M.processInputs[p, t, v] \
        for S_o in M.ProcessOutputsByInput[p, t, v, S_i] \
    ) \
        == M.V_Activity[p, s, d, t, v]

def Capacity_Constraint(M, p, s, d, t, v):
    r"""

This constraint ensures that the capacity of a given process is sufficient
to support its activity across all time periods and time slices. The calculation
on the left hand side of the equality is the maximum amount of energy a process
can produce in the timeslice ``<s``,\ ``d>``. Note that the curtailment variable
shown below only applies to technologies are members of the curtailment set.
Curtailment is necessary to track explicitly in scenarios that include a high
renewable target. Without it, the model can generate more activity than is used
to meet demand, and have all activity (including the portion curtailed) count
towards the target. Tracking activity and curtailment separately prevents this
possibility.

.. math::
   :label: Capacity

       \left (
               \text{CFP}_{t, v}
         \cdot \text{C2A}_{t}
         \cdot \text{SEG}_{s, d}
         \cdot \text{TLF}_{p, t, v}
       \right )
       \cdot \textbf{CAP}_{t, v}
   =
       \textbf{ACT}_{p, s, d, t, v}
       +
       \sum_{I, O} \textbf{CUR}_{p,s,d,i,t,v,o}

   \\
   \forall \{p, s, d, t, v\} \in \Theta_{\text{Activity}}



"""
    if t in M.tech_storage:
        return Constraint.Skip
    # The expressions below are defined in-line to minimize the amount of
    # expression cloning taking place with Pyomo.
    if t in M.tech_curtailment:
        # If technologies are present in the curtailment set, then enough
        # capacity must be available to cover both activity and curtailment.
        return value(M.CapacityFactorProcess[s, d, t, v]) \
            * value(M.CapacityToActivity[t]) * value(M.SegFrac[s, d]) \
            * value(M.ProcessLifeFrac[p, t, v]) \
            * M.V_Capacity[t, v] == M.V_Activity[p, s, d, t, v] + sum( \
            M.V_Curtailment[p, s, d, S_i, t, v, S_o] \
            for S_i in M.processInputs[p, t, v] \
            for S_o in M.ProcessOutputsByInput[p, t, v, S_i])
    else:
        return value(M.CapacityFactorProcess[s, d, t, v]) \
        * value(M.CapacityToActivity[t]) \
        * value(M.SegFrac[s, d]) \
        * value(M.ProcessLifeFrac[p, t, v]) \
        * M.V_Capacity[t, v] >= M.V_Activity[p, s, d, t, v]

def ActivityByPeriodAndProcess_Constraint(M, p, t, v):
    r"""
    
    This constraint creates a derived variable in which the activity variable 
	is summed over the season and time-of-day time slices:

    .. math::
    :label: ActivityByPeriodAndProcess

    \textbf{ACT}_{p, t, v} = \sum_{I, O} \textbf{ACT}_{p,s,d,t,v}

    \\
    \forall \{p, s, d, t, v\} \in \Theta_{\text{activity}}
	"""
    if p < v or v not in M.processVintages[p, t]:
        return Constraint.Skip

    activity = sum(
        M.V_Activity[p, S_s, S_d, t, v]
        for S_s in M.time_season
        for S_d in M.time_of_day
    )

    if int is type(activity):
        return Constraint.Skip

    expr = M.V_ActivityByPeriodAndProcess[p, t, v] == activity
    return expr


# This is required for MGA objective function
def ActivityByTech_Constraint(M, t):
    r"""
    
    This constraint is utilized by the MGA objective function and sums 
	activity by each technology over all time elements and vintages:

    .. math::
    :label: ActivityByTech

    \textbf{ACT}_{t} = \sum_{I, O} \textbf{ACT}_{p,s,d,t,v}

    \\
    \forall \{p, s, d, t, v\} \in \Theta_{\text{activity}}
	"""

    activity = sum(
        M.V_Activity[S_p, S_s, S_d, t, S_v]
        for S_p, S_v in M.processTechs[t]
        for S_s in M.time_season
        for S_d in M.time_of_day
    )

    if int is type(activity):
        return Constraint.Skip

    expr = M.V_ActivityByTech[t] == activity
    return expr


def CapacityAvailableByPeriodAndTech_Constraint(M, p, t):
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
        value(M.ProcessLifeFrac[p, t, S_v]) * M.V_Capacity[t, S_v]
        for S_v in M.processVintages[p, t]
    )

    expr = M.V_CapacityAvailableByPeriodAndTech[p, t] == cap_avail
    return expr


def ExistingCapacity_Constraint(M, t, v):
    r"""

Temoa treats existing capacity installed prior to the beginning of the model's
optimization horizon as regular processes that require the same parameter
specification as do new vintage technologies, except for the :code:`CostInvest`
parameter.  This constraint sets the capacity of processes for model periods
that exist prior to the optimization horizon to user-specified values.

.. math::
   :label: ExistingCapacity

   \textbf{CAP}_{t, v} = ECAP_{t, v}

   \forall \{t, v\} \in \Theta_{\text{ExistingCapacity}}
"""
    expr = M.V_Capacity[t, v] == M.ExistingCapacity[t, v]
    return expr


def EmissionActivityByPeriodAndTech_Constraint(M, e, p, t):
    r"""

This constraint creates a derived variable that tracks the total emissions by
pollutant, model time period, and technology.
"""
    emission_total = sum(
        M.V_FlowOut[p, S_s, S_d, S_i, t, S_v, S_o]
        * M.EmissionActivity[e, S_i, t, S_v, S_o]
        for tmp_e, S_i, S_t, S_v, S_o in M.EmissionActivity.sparse_iterkeys()
        if tmp_e == e and S_t == t
        if (p, S_t, S_v) in M.processInputs.keys()
        for S_s in M.time_season
        for S_d in M.time_of_day
    )

    if type(emission_total) is int:
        return Constraint.Skip

    expr = M.V_EmissionActivityByPeriodAndTech[e, p, t] == emission_total
    return expr


# ---------------------------------------------------------------
# Define the Objective Function
# ---------------------------------------------------------------
def TotalCost_rule(M):
    r"""

Using the :code:`Activity` and :code:`Capacity` variables, the Temoa objective
function calculates the cost of energy supply, under the assumption that capital 
costs are paid through loans. This implementation sums up all the costs incurred, 
and is defined as :math:`C_{tot} = C_{loans} + C_{fixed} + C_{variable}`. Each 
term on the right-hand side represents the cost incurred over the model 
time horizon and discounted to the initial year in the horizon (:math:`{P}_0`). 
The calculation of each term is given below.

.. math::
   :label: obj_loan

   C_{loans} = \sum_{t, v \in \Theta_{IC}} \left (
     \left [
             IC_{t, v}
       \cdot LA_{t, v}
       \cdot \frac{(1 + GDR)^{P_0 - v +1} \cdot (1 - (1 + GDR)^{-{LLN}_{t, v}})}{GDR}
       \cdot \frac{ 1-(1+GDR)^{-LPA_{t,v}} }{ 1-(1+GDR)^{-LP_{t,v}} }
     \right ]
     \cdot \textbf{CAP}_{t, v}
     \right )

Note that capital costs (:math:`{IC}_{t,v}`) are handled in several steps. First, each capital cost 
is amortized using the loan rate (i.e., technology-specific discount rate) and loan 
period. Second, the annual stream of payments is converted into a lump sum using 
the global discount rate and loan period. Third, the new lump sum is amortized 
at the global discount rate and technology lifetime. Fourth, loan payments beyond 
the model time horizon are removed and the lump sum recalculated. The terms used 
in Steps 3-4 are :math:`\frac{ GDR }{ 1-(1+GDR)^{-LP_{t,v} } }\cdot
\frac{ 1-(1+GDR)^{-LPA_{t,v}} }{ GDR }`. The product simplifies to 
:math:`\frac{ 1-(1+GDR)^{-LPA_{t,v}} }{ 1-(1+GDR)^{-LP_{t,v}} }`, where 
:math:`LPA_{t,v}` represents the active lifetime of a process :math:`(t,v)` 
before the end of the model horizon, and :math:`LP_{t,v}` represents the full 
lifetime of a process :math:`(t,v)`. Fifth, the lump sum is discounted back to the 
beginning of the horizon (:math:`P_0`) using the global discount rate. While an 
explicit salvage term is not included, this approach properly captures the capital 
costs incurred within the model time horizon, accounting for technology-specific 
loan rates and periods.

.. math::
   :label: obj_fixed

   C_{fixed} = \sum_{p, t, v \in \Theta_{FC}} \left (
     \left [
             FC_{p, t, v}
       \cdot \frac{(1 + GDR)^{P_0 - p +1} \cdot (1 - (1 + GDR)^{-{MPL}_{t, v}})}{GDR}
     \right ]
     \cdot \textbf{CAP}_{t, v}
     \right )

.. math::
   :label: obj_variable

   C_{variable} = \sum_{p, t, v \in \Theta_{VC}} \left (
           MC_{p, t, v}
     \cdot
     \frac{
       (1 + GDR)^{P_0 - p + 1} \cdot (1 - (1 + GDR)^{-{MPL}_{p,t, v}})
     }{
       GDR
     }
     \cdot \textbf{ACT}_{t, v}
     \right )

"""
    return sum(PeriodCost_rule(M, p) for p in M.time_optimize)


def PeriodCost_rule(M, p):
    P_0 = min(M.time_optimize)
    P_e = M.time_future.last()  # End point of modeled horizon
    GDR = value(M.GlobalDiscountRate)
    MLL = M.ModelLoanLife
    MPL = M.ModelProcessLife
    x = 1 + GDR  # convenience variable, nothing more.

    loan_costs = sum(
        M.V_Capacity[S_t, S_v]
        * (
            value(M.CostInvest[S_t, S_v])
            * value(M.LoanAnnualize[S_t, S_v])
            * (
                value(M.LifetimeLoanProcess[S_t, S_v])
                if not GDR
                else (
                    x ** (P_0 - S_v + 1)
                    * (1 - x ** (-value(M.LifetimeLoanProcess[S_t, S_v])))
                    / GDR
                )
            )
        )
        * (
            (1 - x ** (-min(value(M.LifetimeProcess[S_t, S_v]), P_e - S_v)))
            / (1 - x ** (-value(M.LifetimeProcess[S_t, S_v])))
        )
        for S_t, S_v in M.CostInvest.sparse_iterkeys()
        if S_v == p
    )

    fixed_costs = sum(
        M.V_Capacity[S_t, S_v]
        * (
            value(M.CostFixed[p, S_t, S_v])
            * (
                value(MPL[p, S_t, S_v])
                if not GDR
                else (x ** (P_0 - p + 1) * (1 - x ** (-value(MPL[p, S_t, S_v]))) / GDR)
            )
        )
        for S_p, S_t, S_v in M.CostFixed.sparse_iterkeys()
        if S_p == p
    )

    variable_costs = sum(
        M.V_ActivityByPeriodAndProcess[p, S_t, S_v]
        * (
            value(M.CostVariable[p, S_t, S_v])
            * (
                value(MPL[p, S_t, S_v])
                if not GDR
                else (x ** (P_0 - p + 1) * (1 - x ** (-value(MPL[p, S_t, S_v]))) / GDR)
            )
        )
        for S_p, S_t, S_v in M.CostVariable.sparse_iterkeys()
        if S_p == p
    )

    period_costs = loan_costs + fixed_costs + variable_costs
    return period_costs


# ---------------------------------------------------------------
# Define the Model Constraints.
# The order of constraint definitions follows the same order as the
# declarations in temoa_model.py.
# ---------------------------------------------------------------


def Demand_Constraint(M, p, s, d, dem):
    r"""

The Demand constraint drives the model.  This constraint ensures that supply at
least meets the demand specified by the Demand parameter in all periods and
slices, by ensuring that the sum of all the demand output commodity (:math:`c`)
generated by :math:`\textbf{FO}` must meet the modeler-specified demand, in
each time slice.

.. math::
   :label: Demand

   \sum_{I, T, V} \textbf{FO}_{p, s, d, i, t, v, dem}
   =
   {DEM}_{p, dem} \cdot {DSD}_{s, d, dem}

   \\
   \forall \{p, s, d, dem\} \in \Theta_{\text{Demand}}

Note that the validity of this constraint relies on the fact that the
:math:`C^d` set is distinct from both :math:`C^e` and :math:`C^p`. In other
words, an end-use demand must only be an end-use demand.  Note that if an output
could satisfy both an end-use and internal system demand, then the output from
:math:`\textbf{FO}` would be double counted.

"""
    if (s,d,dem) not in M.DemandSpecificDistribution.sparse_keys():
        return Constraint.Skip
    supply = sum(
        M.V_FlowOut[p, s, d, S_i, S_t, S_v, dem]
        for S_t, S_v in M.commodityUStreamProcess[p, dem]
        for S_i in M.ProcessInputsByOutput[p, S_t, S_v, dem]
    )

    DemandConstraintErrorCheck(supply, p, s, d, dem)

    expr = supply == M.Demand[p, dem] * M.DemandSpecificDistribution[s, d, dem]

    return expr

def DemandActivity_Constraint(M, p, s, d, t, v, dem, s_0, d_0):
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
   \forall \{p, s, d, t, v, dem, s_0, d_0\} \in \Theta_{\text{DemandActivity}}
"""
    if (s,d,dem) not in M.DemandSpecificDistribution.sparse_keys():
        return Constraint.Skip
    DSD = M.DemandSpecificDistribution  # lazy programmer

    act_a = sum(
        M.V_FlowOut[p, s_0, d_0, S_i, t, v, dem]
        for S_i in M.ProcessInputsByOutput[p, t, v, dem]
    )
    act_b = sum(
        M.V_FlowOut[p, s, d, S_i, t, v, dem]
        for S_i in M.ProcessInputsByOutput[p, t, v, dem]
    )

    expr = act_a * DSD[s, d, dem] == act_b * DSD[s_0, d_0, dem]
    return expr


def CommodityBalance_Constraint(M, p, s, d, c):
    r"""

Where the Demand constraint :eq:`Demand` ensures that end-use demands are met,
the CommodityBalance constraint ensures that the endogenous system demands are
met.  This constraint requires the total production of a given commodity
to equal the amount consumed, thus ensuring an energy balance at the system
level. In the updated version of Temoa, the activity variables 
:math:`textbf{FI}_{p, s, d, i, t, v, c}` is defined only for storage technologies. 
This change requires having separate expressions for calculating the 
consumption of commodity :math:`c` : one expressions using 
:math:`textbf{FI}_{p, s, d, i, t, v, c}` for storage technologies, and one 
expression using :math:textbf{FO}_{p, s, d, i, t, v, c}/EF_{i,t,v,o} for regular 
non-storage technologies. The devision by :math:`EF_{c,t,v,o}` is applied to the 
output flows of downstream processes that consume commodity :math:`c`.

.. math::
  generation = consumption 

 \sum_{I,T, V} \textbf{FO}_{p, s, d, i, t, v, c}
  =
 \sum_{T\textsuperscript{s}, V, I} \textbf{FI}_{p, s, d, c, t, v, i} +
 \sum_{T-T\textsuperscript{s}, V, O} \textbf{FO}_{p, s, d, c, t, v, o} /EF_{c,t,v,o}

 \\
 \forall \{p, s, d, c\} \in \Theta_{\text{CommodityBalance}}
"""
    if c in M.commodity_demand:
        return Constraint.Skip

    vflow_in_ToStorage = sum(
        M.V_FlowIn[p, s, d, c, S_t, S_v, S_o]
        for S_t, S_v in M.commodityDStreamProcess[p, c] if S_t in M.tech_storage
        for S_o in M.ProcessOutputsByInput[p, S_t, S_v, c]
    )
    
    vflow_in_ToNonStorage = sum(
        M.V_FlowOut[p, s, d, c, S_t, S_v, S_o] / value(M.Efficiency[c, S_t, S_v, S_o])
        for S_t, S_v in M.commodityDStreamProcess[p, c] if S_t not in M.tech_storage
        for S_o in M.ProcessOutputsByInput[p, S_t, S_v, c]
    )

    vflow_out = sum(
        M.V_FlowOut[p, s, d, S_i, S_t, S_v, c]
        for S_t, S_v in M.commodityUStreamProcess[p, c]
        for S_i in M.ProcessInputsByOutput[p, S_t, S_v, c]
    )

    CommodityBalanceConstraintErrorCheck(vflow_out, vflow_in_ToStorage +  vflow_in_ToNonStorage, p, s, d, c)

    expr = vflow_out == vflow_in_ToStorage +  vflow_in_ToNonStorage
    return expr


def ResourceExtraction_Constraint(M, p, r):
    r"""

The ResourceExtraction constraint allows a modeler to specify an annual limit on
the amount of a particular resource Temoa may use in a period.

.. math::
   :label: ResourceExtraction

   \sum_{S, D, I, t \in T^r, V} \textbf{FO}_{p, s, d, i, t, v, c} \le RSC_{p, c}

   \forall \{p, c\} \in \Theta_{\text{ResourceExtraction}}
"""
    collected = sum(
        M.V_FlowOut[p, S_s, S_d, S_i, S_t, S_v, r]
        for S_i, S_t, S_v in M.ProcessByPeriodAndOutput.keys()
        for S_s in M.time_season
        for S_d in M.time_of_day
    )

    expr = collected <= M.ResourceBound[p, r]
    return expr


def BaseloadDiurnal_Constraint(M, p, s, d, t, v):
    r"""

Some electric generators cannot ramp output over a short period of time (e.g.,
hourly or daily). Temoa models this behavior by forcing technologies in the
:code:`tech_baseload` set to maintain a constant output across all times-of-day
within the same season. Note that the output of a baseload process can vary
between seasons.

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
   \forall \{p, s, d, t, v\} \in \Theta_{\text{BaseloadDiurnal}}
"""
    # Question: How to set the different times of day equal to each other?

    # Step 1: Acquire a "canonical" representation of the times of day
    l_times = sorted(M.time_of_day)  # i.e. a sorted Python list.
    # This is the commonality between invocations of this method.

    index = l_times.index(d)
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
    d_0 = l_times[0]

    # Step 3: the actual expression.  For baseload, must compute the /average/
    # activity over the segment.  By definition, average is
    #     (segment activity) / (segment length)
    # So:   (ActA / SegA) == (ActB / SegB)
    #   computationally, however, multiplication is cheaper than division, so:
    #       (ActA * SegB) == (ActB * SegA)
    expr = (
        M.V_Activity[p, s, d, t, v] * M.SegFrac[s, d_0]
        == M.V_Activity[p, s, d_0, t, v] * M.SegFrac[s, d]
    )
    return expr


def StorageEnergy_Constraint(M, p, s, d, t, v):
    r"""

This constraint tracks the amount of storage assuming ordered time slices.
The storage unit is initialized at a user-specified charge level (0-100%) in the
first time slice of each period, and then the charge level is updated each time
slice based on the amount of energy stored or discharged. At the end of the last
time slice associated with each period, the charge level must be zeroed out.
"""
    # This is the sum of all input=i sent TO storage tech t of vintage v with
    # output=o in p,s,d
    charge = sum(
        M.V_FlowIn[p, s, d, S_i, t, v, S_o] * M.Efficiency[S_i, t, v, S_o]
        for S_i in M.processInputs[p, t, v]
        for S_o in M.ProcessOutputsByInput[p, t, v, S_i]
    )

    # This is the sum of all output=o withdrawn FROM storage tech t of vintage v
    # with input=i in p,s,d
    discharge = sum(
        M.V_FlowOut[p, s, d, S_i, t, v, S_o]
        for S_o in M.processOutputs[p, t, v]
        for S_i in M.ProcessInputsByOutput[p, t, v, S_o]
    )

    stored_energy = charge - discharge

    # This storage formulation allows stored energy to carry over through
    # time of day and seasons, but must be zeroed out at the end of each period, i.e.,
    # the last time slice of the last season must zero out
    if d == M.time_of_day.last() and s == M.time_season.last():
        d_prev = M.time_of_day.prev(d)
        initial_storage = (
            M.StorageInit[t]
            * M.V_Capacity[t, v]
            * M.StorageDuration[t]
            * M.CapacityToActivity[t]
            * value(M.ProcessLifeFrac[p, t, v])
        )
        expr = M.V_StorageLevel[p, s, d_prev, t, v] + stored_energy == initial_storage

    # First time slice of the first season (i.e., start of period), starts at full charge
    elif d == M.time_of_day.first() and s == M.time_season.first():
        initial_storage = (
            M.StorageInit[t]
            * M.V_Capacity[t, v]
            * M.StorageDuration[t]
            * M.CapacityToActivity[t]
            * value(M.ProcessLifeFrac[p, t, v])
        )
        expr = M.V_StorageLevel[p, s, d, t, v] == initial_storage + stored_energy

    # First time slice of any season that is NOT the first season
    elif d == M.time_of_day.first():
        d_last = M.time_of_day.last()
        s_prev = M.time_season.prev(s)
        expr = (
            M.V_StorageLevel[p, s, d, t, v]
            == M.V_StorageLevel[p, s_prev, d_last, t, v] + stored_energy
        )

    # Any time slice that is NOT covered above (i.e., not the time slice ending
    # the period, or the first time slice of any season)
    else:
        d_prev = M.time_of_day.prev(d)
        expr = (
            M.V_StorageLevel[p, s, d, t, v]
            == M.V_StorageLevel[p, s, d_prev, t, v] + stored_energy
        )

    return expr


def StorageEnergyUpperBound_Constraint(M, p, s, d, t, v):
    r"""

This constraint ensures that the amount of energy stored does not exceed
the upper bound set by the energy capacity of the storage device.
"""
    energy_capacity = (
        M.V_Capacity[t, v]
        * M.StorageDuration[t]
        * M.CapacityToActivity[t]
        * value(M.ProcessLifeFrac[p, t, v])
    )
    expr = M.V_StorageLevel[p, s, d, t, v] <= energy_capacity

    return expr


def StorageChargeRate_Constraint(M, p, s, d, t, v):
    r"""

    This constraint ensures that the charge rate of the storage unit is
    limited by the power capacity (typically GW) of the storage unit.
"""
    # Calculate energy charge in each time slice
    slice_charge = sum(
        M.V_FlowIn[p, s, d, S_i, t, v, S_o] * M.Efficiency[S_i, t, v, S_o]
        for S_i in M.processInputs[p, t, v]
        for S_o in M.ProcessOutputsByInput[p, t, v, S_i]
    )

    # Maximum energy charge in each time slice
    max_charge = (
        M.V_Capacity[t, v]
        * M.CapacityToActivity[t]
        * M.SegFrac[s, d]
        * value(M.ProcessLifeFrac[p, t, v])
    )

    # Energy charge cannot exceed the power capacity of the storage unit
    expr = slice_charge <= max_charge

    return expr


def StorageDischargeRate_Constraint(M, p, s, d, t, v):
    r"""

	This constraint ensures that the discharge rate of the storage unit
	is limited by the power capacity (typically GW) of the storage unit.
"""
    # Calculate energy discharge in each time slice
    slice_discharge = sum(
        M.V_FlowOut[p, s, d, S_i, t, v, S_o]
        for S_o in M.processOutputs[p, t, v]
        for S_i in M.ProcessInputsByOutput[p, t, v, S_o]
    )

    # Maximum energy discharge in each time slice
    max_discharge = (
        M.V_Capacity[t, v]
        * M.CapacityToActivity[t]
        * M.SegFrac[s, d]
        * value(M.ProcessLifeFrac[p, t, v])
    )

    # Energy discharge cannot exceed the capacity of the storage unit
    expr = slice_discharge <= max_discharge

    return expr


def StorageThroughput_Constraint(M, p, s, d, t, v):
    r"""

It is not enough to only limit the charge and discharge rate separately. We also 
need to ensure that the maximum throughput (charge + discharge) does not exceed 
the capacity (typically GW) of the storage unit.
"""
    discharge = sum(
        M.V_FlowOut[p, s, d, S_i, t, v, S_o]
        for S_o in M.processOutputs[p, t, v]
        for S_i in M.ProcessInputsByOutput[p, t, v, S_o]
    )

    charge = sum(
        M.V_FlowIn[p, s, d, S_i, t, v, S_o] * M.Efficiency[S_i, t, v, S_o]
        for S_i in M.processInputs[p, t, v]
        for S_o in M.ProcessOutputsByInput[p, t, v, S_i]
    )

    throughput = charge + discharge
    max_throughput = (
        M.V_Capacity[t, v]
        * M.CapacityToActivity[t]
        * M.SegFrac[s, d]
        * value(M.ProcessLifeFrac[p, t, v])
    )
    expr = throughput <= max_throughput
    return expr


def RampUpDay_Constraint(M, p, s, d, t, v):
    # M.time_of_day is a sorted set, and M.time_of_day.first() returns the first
    # element in the set, similarly, M.time_of_day.last() returns the last element.
    # M.time_of_day.prev(d) function will return the previous element before s, and
    # M.time_of_day.next(d) function will return the next element after s.

    r"""

The ramp rate constraint is utilized to limit the rate of electricity generation 
increase and decrease between two adjacent time slices in order to account for 
physical limits associated with thermal power plants. Note that this constraint 
only applies to technologies with ramp capability, which is defined in the set 
:math:`\textbf{T}^{ramp}`. We assume for simplicity the rate limits for both 
ramp up and down are equal and they do not vary with technology vintage. The 
ramp rate limits (:math:`r_t`) for technology :math:`t` should be expressed in 
percentage of its rated capacity.

Note that when :math:`d_{nd}` is the last time-of-day, :math:`d_{nd + 1} \not \in 
\textbf{D}`, i.e., if one time slice is the last time-of-day in a season and the 
other time slice is the first time-of-day in the next season, the ramp rate 
limits between these two time slices can not be expressed by :eq:`ramp_up_day`. 
Therefore, the ramp rate constraints between two adjacent seasons are 
represented in :eq:`ramp_up_season`. 

In Equation :eq:`ramp_up_day` and :eq:`ramp_up_season`, we assume 
:math:`\textbf{S} = \{s_i, i = 1, 2, \cdots, ns\}` and 
:math:`\textbf{D} = \{d_i, i=1, 2, \cdots, nd\}`.

.. math::
   \frac{ 
       \textbf{ACT}_{p, s, d_{i + 1}, t, v} 
       }{
       SEG_{s, d_{i + 1}} \cdot C2A_t 
       }
   -
   \frac{ 
       \textbf{ACT}_{p, s, d_i, t, v} 
       }{
       SEG_{s, d_i} \cdot C2A_t 
       }
   \leq
   r_t \cdot \textbf{CAPAVL}_{p,t}
   \\
   \forall 
   p \in \textbf{P}^o,
   s \in \textbf{S},
   d_i, d_{i + 1} \in \textbf{D},
   t \in \textbf{T}^{ramp},
   v \in \textbf{V}
   :label: ramp_up_day
"""

    if d != M.time_of_day.first():
        d_prev = M.time_of_day.prev(d)
        expr_left = (
            M.V_Activity[p, s, d, t, v] / value(M.SegFrac[s, d])
            - M.V_Activity[p, s, d_prev, t, v] / value(M.SegFrac[s, d_prev])
        ) / value(M.CapacityToActivity[t])
        expr_right = M.V_Capacity[t, v] * value(M.RampUp[t])
        expr = expr_left <= expr_right
    else:
        return Constraint.Skip

    return expr


def RampDownDay_Constraint(M, p, s, d, t, v):
    r"""

Similar to Equation :eq:`ramp_up_day`, we use Equation :eq:`ramp_down_day` to
limit ramp down rates between any two adjacent time slices.

.. math::
   \frac{ 
       \textbf{ACT}_{p, s, d_{i + 1}, t, v} 
       }{
       SEG_{s, d_{i + 1}} \cdot C2A_t 
       }
   -
   \frac{ 
       \textbf{ACT}_{p, s, d_i, t, v} 
       }{
       SEG_{s, d_i} \cdot C2A_t 
       }
   \geq
   -r_t \cdot \textbf{CAPAVL}_{p,t}
   \\
   \forall 
   p \in \textbf{P}^o,
   s \in \textbf{S},
   d_i, d_{i + 1} \in \textbf{D},
   t \in \textbf{T}^{ramp},
   v \in \textbf{V}
   :label: ramp_down_day
"""
    if d != M.time_of_day.first():
        d_prev = M.time_of_day.prev(d)
        expr_left = (
            M.V_Activity[p, s, d, t, v] / value(M.SegFrac[s, d])
            - M.V_Activity[p, s, d_prev, t, v] / value(M.SegFrac[s, d_prev])
        ) / value(M.CapacityToActivity[t])
        expr_right = -(M.V_Capacity[t, v] * value(M.RampDown[t]))
        expr = expr_left >= expr_right
    else:
        return Constraint.Skip

    return expr


def RampUpSeason_Constraint(M, p, s, t, v):
    r"""

Note that :math:`d_1` and :math:`d_{nd}` represent the first and last time-of-day, 
respectively.

.. math::
   \frac{ 
       \textbf{ACT}_{p, s_{i + 1}, d_1, t, v} 
       }{
       SEG_{s_{i + 1}, d_1} \cdot C2A_t 
       }
   -
   \frac{ 
       \textbf{ACT}_{p, s_i, d_{nd}, t, v} 
       }{
       SEG_{s_i, d_{nd}} \cdot C2A_t 
       }
   \leq
   r_t \cdot \textbf{CAPAVL}_{p,t}
   \\
   \forall 
   p \in \textbf{P}^o,
   s_i, s_{i + 1} \in \textbf{S},
   d_1, d_{nd} \in \textbf{D},
   t \in \textbf{T}^{ramp},
   v \in \textbf{V}
   :label: ramp_up_season
"""
    if s != M.time_season.first():
        s_prev = M.time_season.prev(s)
        d_first = M.time_of_day.first()
        d_last = M.time_of_day.last()
        expr_left = (
            M.V_Activity[p, s, d_first, t, v] / M.SegFrac[s, d_first]
            - M.V_Activity[p, s_prev, d_last, t, v] / M.SegFrac[s_prev, d_last]
        ) / value(M.CapacityToActivity[t])
        expr_right = M.V_Capacity[t, v] * value(M.RampUp[t])
        expr = expr_left <= expr_right
    else:
        return Constraint.Skip

    return expr


def RampDownSeason_Constraint(M, p, s, t, v):
    r"""

Similar to Equation :eq:`ramp_up_season`, we use Equation :eq:`ramp_down_season`
to limit ramp down rates between any two adjacent seasons.

.. math::
   \frac{ 
       \textbf{ACT}_{p, s_{i + 1}, d_1, t, v} 
       }{
       SEG_{s_{i + 1}, d_1} \cdot C2A_t 
       }
   -
   \frac{ 
       \textbf{ACT}_{p, s_i, d_{nd}, t, v} 
       }{
       SEG_{s_i, d_{nd}} \cdot C2A_t 
       }
   \geq
   -r_t \cdot \textbf{CAPAVL}_{p,t}
   \\
   \forall 
   p \in \textbf{P}^o,
   s_i, s_{i + 1} \in \textbf{S},
   d_1, d_{nd} \in \textbf{D},
   t \in \textbf{T}^{ramp},
   v \in \textbf{V}
   :label: ramp_down_season
"""
    if s != M.time_season.first():
        s_prev = M.time_season.prev(s)
        d_first = M.time_of_day.first()
        d_last = M.time_of_day.last()
        expr_left = (
            M.V_Activity[p, s, d_first, t, v] / value(M.SegFrac[s, d_first])
            - M.V_Activity[p, s_prev, d_last, t, v] / value(M.SegFrac[s_prev, d_last])
        ) / value(M.CapacityToActivity[t])
        expr_right = -(M.V_Capacity[t, v] * value(M.RampDown[t]))
        expr = expr_left >= expr_right
    else:
        return Constraint.Skip

    return expr


def RampUpPeriod_Constraint(M, p, t, v):

    # if p != M.time_future.first():
    # 	p_prev  = M.time_future.prev(p)
    # 	s_first = M.time_season.first()
    # 	s_last  = M.time_season.last()
    # 	d_first = M.time_of_day.first()
    # 	d_last  = M.time_of_day.last()
    # 	expr_left = (
    # 		M.V_Activity[ p, s_first, d_first, t, v ] -
    # 		M.V_Activity[ p_prev, s_last, d_last, t, v ]
    # 		)
    # 	expr_right = (
    # 		M.V_Capacity[t, v]*
    # 		value( M.RampUp[t] )*
    # 		value( M.CapacityToActivity[ t ] )*
    # 		value( M.SegFrac[s, d])
    # 		)
    # 	expr = (expr_left <= expr_right)
    # else:
    # 	return Constraint.Skip

    # return expr

    return Constraint.Skip  # We don't need inter-period ramp up/down constraint.


def RampDownPeriod_Constraint(M, p, t, v):

    # if p != M.time_future.first():
    # 	p_prev  = M.time_future.prev(p)
    # 	s_first = M.time_season.first()
    # 	s_last  = M.time_season.last()
    # 	d_first = M.time_of_day.first()
    # 	d_last  = M.time_of_day.last()
    # 	expr_left = (
    # 		M.V_Activity[ p, s_first, d_first, t, v ] -
    # 		M.V_Activity[ p_prev, s_last, d_last, t, v ]
    # 		)
    # 	expr_right = (
    # 		-1*
    # 		M.V_Capacity[t, v]*
    # 		value( M.RampDown[t] )*
    # 		value( M.CapacityToActivity[ t ] )*
    # 		value( M.SegFrac[s, d])
    # 		)
    # 	expr = (expr_left >= expr_right)
    # else:
    # 	return Constraint.Skip

    # return expr

    return Constraint.Skip  # We don't need inter-period ramp up/down constraint.


def ReserveMargin_Constraint(M, p, s, d):
    r"""

During each period :math:`p`, the sum of the available capacity of all reserve 
technologies :math:`\sum_{t \in T^{res}} \textbf{CAPAVL}_{p,t}`, which are 
defined in the set :math:`\textbf{T}^{res}`, should exceed the peak load by 
:math:`RES_z`, the regional reserve margin. Note that the reserve 
margin is expressed in percentage of the peak load. Generally speaking, in 
a database we may not know the peak demand before running the model, therefore, 
we write this equation for all the time-slices defined in the database in each region.

.. math::
   \sum_{t \in T^{res}} {
      CC_t \cdot
      \textbf{CAPAVL}_{p,t} \cdot
      SEG_{s^*,d^*} \cdot C2A_t }
   \geq
   \sum_{t \in T^{res}} { 
      \sum_{t \in v^{vintage}} \textbf{ACT}_{p, s, d, t, v}} \cdot
      (1 + RES_z)
   \\
   \forall
   p \in \textbf{P}^o,
   z \in \textbf{C}^{zone}
   :label: reserve_margin
"""
    if not M.tech_reserve:  # If reserve set empty, skip the constraint
        return Constraint.Skip

    cap_avail = sum(
        value(M.CapacityCredit[p, t])
        * M.V_CapacityAvailableByPeriodAndTech[p, t]
        * value(M.CapacityToActivity[t])
        * value(M.SegFrac[s, d])
        for t in M.tech_reserve
        # Make sure (p,t) combinations are defined
        if (p,t) in M.activeCapacityAvailable_pt
    )

    # In most Temoa input databases, demand is endogenous, so we use electricity
    # generation instead.
    total_generation = sum(
        M.V_Activity[p, s, d, t, S_v]
        for (t,S_v) in M.processReservePeriods[p]
    )

    cap_target = total_generation * (1 + value(M.PlanningReserveMargin))

    return cap_avail >= cap_target


def EmissionLimit_Constraint(M, p, e):
    r"""

A modeler can track emissions through use of the :code:`commodity_emissions`
set and :code:`EmissionActivity` parameter.  The :math:`EAC` parameter is
analogous to the efficiency table, tying emissions to a unit of activity.  The
EmissionLimit constraint allows the modeler to assign an upper bound per period
to each emission commodity.

.. math::
   :label: EmissionLimit

   \sum_{S,D,I,T,V,O|{e,i,t,v,o} \in EAC_{ind}} \left (
       EAC_{e, i, t, v, o} \cdot \textbf{FO}_{p, s, d, i, t, v, o}
     \right )
     \le
     ELM_{p, e}

   \\
   \forall \{p, e\} \in \Theta_{\text{EmissionLimit}}
"""
    emission_limit = M.EmissionLimit[p, e]

    actual_emissions = sum(
        M.V_FlowOut[p, S_s, S_d, S_i, S_t, S_v, S_o]
        * M.EmissionActivity[e, S_i, S_t, S_v, S_o]
        for tmp_e, S_i, S_t, S_v, S_o in M.EmissionActivity.sparse_iterkeys()
        if tmp_e == e
        # EmissionsActivity not indexed by p, so make sure (p,t,v) combos valid
        if (p, S_t, S_v) in M.processInputs.keys()
        for S_s in M.time_season
        for S_d in M.time_of_day
    )

    if int is type(actual_emissions):
        msg = (
            "Warning: No technology produces emission '%s', though limit was "
            "specified as %s.\n"
        )
        SE.write(msg % (e, emission_limit))
        return Constraint.Skip

    expr = actual_emissions <= emission_limit
    return expr


def GrowthRateConstraint_rule(M, p, t):
    r"""

This constraint sets an upper bound growth rate on technology-specific capacity.

.. math::
   :label: GrowthRate

   CAPAVL_{p_{i},t} \le GRM \cdot CAPAVL_{p_{i-1},t} + GRS,

   \\
   \forall \{p, t\} \in \Theta_{\text{GrowthRate}}

where :math:`GRM` is the maximum growth rate, and should be specified as 
:math:`(1+r)` and :math:`GRS` is the growth rate seed, which has units of 
capacity. Without the seed, any technology with zero capacity in the first time 
period would be restricted to zero capacity for the remainder of the time 
horizon.
"""
    GRS = value(M.GrowthRateSeed[t])
    GRM = value(M.GrowthRateMax[t])
    CapPT = M.V_CapacityAvailableByPeriodAndTech

    periods = sorted(set(p_ for p_, t_ in CapPT if t_ == t))

    if p not in periods:
        return Constraint.Skip

    if p == periods[0]:
        expr = CapPT[p, t] <= GRS

    else:
        p_prev = periods.index(p)
        p_prev = periods[p_prev - 1]

        expr = CapPT[p, t] <= GRM * CapPT[p_prev, t] + GRS

    return expr


def MaxActivity_Constraint(M, p, t):
    r"""

The MaxActivity sets an upper bound on the activity from a specific technology. 
Note that the indices for these constraints are period and tech, not tech 
and vintage.

.. math::
   :label: MaxActivity

   \sum_{S,D,V} \textbf{ACT}_{p,s,d,t,v} \le MAXACT_{p, t}

   \forall \{p, t\} \in \Theta_{\text{MaxActivity}}
"""
    activity_pt = sum(
        M.V_Activity[p, S_s, S_d, t, S_v]
        for S_s in M.time_season
        for S_d in M.time_of_day
        for S_v in M.processVintages[p, t]
    )
    max_act = value(M.MaxActivity[p, t])
    expr = activity_pt <= max_act
    return expr


def MinActivity_Constraint(M, p, t):
    r"""

The MinActivity sets a lower bound on the activity from a specific technology.
Note that the indices for these constraints are period and tech, not tech and
vintage.

.. math::
   :label: MinActivity

   \sum_{S,D,V} \textbf{ACT}_{p,s,d,t,v} \ge MINACT_{p, t}

   \forall \{p, t\} \in \Theta_{\text{MinActivity}}
"""
    activity_pt = sum(
        M.V_Activity[p, S_s, S_d, t, S_v]
        for S_s in M.time_season
        for S_d in M.time_of_day
        for S_v in M.processVintages[p, t]
    )
    min_act = value(M.MinActivity[p, t])
    expr = activity_pt >= min_act
    return expr


def MinActivityGroup_Constraint(M, p, g):
    r"""

The MinActivityGroup constraint sets a minimum activity limit for a user-defined
technology group. Each technology within each group is multiplied by a
weighting function, which determines what technology activity share can count
towards the constraint.

.. math::
   :label: MinActivityGroup

   \sum_{S,D,T,V} \textbf{ACT}_{p,s,d,t,v} \cdot WEIGHT_t \ge MGGT_{p, g}

   \forall \{p, g\} \in \Theta_{\text{MinActivityGroup}}

where :math:`g` represents the assigned technology group and :math:`MGGT` 
refers to the :code:`MinGenGroupTarget` parameter.
"""
    activity_p = sum(
        M.V_Activity[p, S_s, S_d, S_t, S_v]
        * M.MinGenGroupWeight[S_t, g]
        for S_t in M.tech_groups
        for S_s in M.time_season
        for S_d in M.time_of_day
        for S_v in M.processVintages[p, S_t]
    )
    min_act = value(M.MinGenGroupTarget[p, g])
    expr = activity_p >= min_act
    return expr


def MaxCapacity_Constraint(M, p, t):
    r"""

The MaxCapacity constraint sets a limit on the maximum available capacity of a
given technology. Note that the indices for these constraints are period and
tech, not tech and vintage.

.. math::
   :label: MaxCapacity

   \textbf{CAPAVL}_{p, t} \le MAX_{p, t}

   \forall \{p, t\} \in \Theta_{\text{MaxCapacity}}
"""
    max_cap = value(M.MaxCapacity[p, t])
    expr = M.V_CapacityAvailableByPeriodAndTech[p, t] <= max_cap
    return expr


def MaxCapacitySet_Constraint(M, p):
    r""" See MaxCapacity_Constraint """
    max_cap = value(M.MaxCapacitySum[p])
    aggcap = sum(
        M.V_CapacityAvailableByPeriodAndTech[p, t] for t in M.tech_capacity_max
    )
    expr = aggcap <= max_cap
    return expr


def MinCapacity_Constraint(M, p, t):
    r"""

The MinCapacity constraint sets a limit on the minimum available capacity of a
given technology. Note that the indices for these constraints are period and
tech, not tech and vintage.

.. math::
   :label: MinCapacityCapacityAvailableByPeriodAndTech

   \textbf{CAPAVL}_{p, t} \ge MIN_{p, t}

   \forall \{p, t\} \in \Theta_{\text{MinCapacity}}
"""
    min_cap = value(M.MinCapacity[p, t])
    expr = M.V_CapacityAvailableByPeriodAndTech[p, t] >= min_cap
    return expr


def MinCapacitySet_Constraint(M, p):
    r""" See MinCapacity_Constraint """
    min_cap = value(M.MinCapacitySum[p])
    aggcap = sum(
        M.V_CapacityAvailableByPeriodAndTech[p, t] for t in M.tech_capacity_min
    )
    expr = aggcap >= min_cap
    return expr


def TechInputSplit_Constraint(M, p, s, d, i, t, v):
    r"""

Allows users to specify fixed or minimum shares of commodity inputs to a process 
producing a single output. These shares can vary by model time period. See 
TechOutputSplit_Constraint for an analogous explanation.
"""
    inp = sum(
        M.V_FlowOut[p, s, d, i, t, v, S_o] / value(M.Efficiency[i, t, v, S_o])
        for S_o in M.ProcessOutputsByInput[p, t, v, i]
    )

    total_inp = sum(
        M.V_FlowOut[p, s, d, S_i, t, v, S_o] / value(M.Efficiency[S_i, t, v, S_o])
        for S_i in M.processInputs[p, t, v]
        for S_o in M.ProcessOutputsByInput[p, t, v, i]
    )

    expr = inp >= M.TechInputSplit[p, i, t] * total_inp
    return expr


def TechOutputSplit_Constraint(M, p, s, d, t, v, o):
    r"""

Some processes take a single input and make multiple outputs, and the user would like to 
specify either a constant or time-varying ratio of outputs per unit input.  The most 
canonical example is an oil refinery.  Crude oil is used to produce many different refined 
products. In many cases, the modeler would like to specify a minimum share of each refined 
product produced by the refinery.

For example, a hypothetical (and highly simplified) refinery might have a crude oil input 
that produces 4 parts diesel, 3 parts gasoline, and 2 parts kerosene.  The relative 
ratios to the output then are:

.. math::

   d = \tfrac{4}{9} \cdot \text{total output}, \qquad
   g = \tfrac{3}{9} \cdot \text{total output}, \qquad
   k = \tfrac{2}{9} \cdot \text{total output}

Note that it is possible to specify output shares that sum to less than unity. In such 
cases, the model optimizes the remaining share. In addition, it is possible to change the 
specified shares by model time period. The constraint is formulated as follows:

.. math::
   :label: TechOutputSplit

     \sum_{I} \textbf{FO}_{p, s, d, i, t, v, o}
   \geq
     SPL_{p, t, o} \cdot \textbf{ACT}_{p, s, d, t, v}

   \forall \{p, s, d, t, v, o\} \in \Theta_{\text{TechOutputSplit}}
"""
    out = sum(
        M.V_FlowOut[p, s, d, S_i, t, v, o]
        for S_i in M.ProcessInputsByOutput[p, t, v, o]
    )

    expr = out >= M.TechOutputSplit[p, t, o] * M.V_Activity[p, s, d, t, v]
    return expr


# ---------------------------------------------------------------
# Define rule-based parameters
# ---------------------------------------------------------------
def ParamModelLoanLife_rule(M, t, v):
    loan_length = value(M.LifetimeLoanProcess[t, v])
    mll = min(loan_length, max(M.time_future) - v)

    return mll


def ParamModelProcessLife_rule(M, p, t, v):
    life_length = value(M.LifetimeProcess[t, v])
    tpl = min(v + life_length - p, value(M.PeriodLength[p]))

    return tpl


def ParamPeriodLength(M, p):
    # This specifically does not use time_optimize because this function is
    # called /over/ time_optimize.
    periods = sorted(M.time_future)

    i = periods.index(p)

    # The +1 won't fail, because this rule is called over time_optimize, which
    # lacks the last period in time_future.
    length = periods[i + 1] - periods[i]

    return length


def ParamPeriodRate(M, p):
    """\
        
The "Period Rate" is a multiplier against the costs incurred within a period to
bring the time-value back to the base year.  The parameter PeriodRate is not
directly specified by the modeler, but is a convenience calculation based on the
GlobalDiscountRate and the length of each period.  One may refer to this
(pseudo) parameter via M.PeriodRate[ a_period ]
"""
    rate_multiplier = sum(
        (1 + M.GlobalDiscountRate) ** (M.time_optimize.first() - p - y)
        for y in range(0, M.PeriodLength[p])
    )

    return value(rate_multiplier)


def ParamProcessLifeFraction_rule(M, p, t, v):
    """\

Calculate the fraction of period p that process :math:`<t, v>` operates.

For most processes and periods, this will likely be one, but for any process
that will cease operation (rust out, be decommissioned, etc.) between periods,
calculate the fraction of the period that the technology is able to
create useful output.
"""
    eol_year = v + value(M.LifetimeProcess[t, v])
    frac = eol_year - p
    period_length = value(M.PeriodLength[p])
    if frac >= period_length:
        # try to avoid floating point round-off errors for the common case.
        return 1

        # number of years into final period loan is complete

    frac /= float(period_length)
    return frac


def ParamLoanAnnualize_rule(M, t, v):
    dr = value(M.DiscountRate[t, v])
    lln = value(M.LifetimeLoanProcess[t, v])
    if not dr:
        return 1.0 / lln
    annualized_rate = dr / (1.0 - (1.0 + dr) ** (-lln))

    return annualized_rate
