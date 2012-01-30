
verbose = True
force = False

dirname    = 'utopia_demand'
modelpath  = '../energysystem-process-Coopr3/temoa_model/temoa_model.py'
dotdatpath = '../energysystem-datfiles/utopia.dat'
stochasticset = 'time_optimize'
stochastic_indices = {'Demand': 0, 'CostInvest': 1}

# CL, CA, CH = coal "[lower, average, high]" rate
# _Low, _Average, _High = demand "[low, average, high]" rate
types = (
  'CL_Low', 'CL_Average', 'CL_High',
  'CA_Low', 'CA_Average', 'CA_High',
  'CH_Low', 'CH_Average', 'CH_High',
)

# for this toy problem, all branches are equally likely, so 1/9
conditional_probability = dict(
  CL_Low     = 0.1111111111111111111,
  CA_Low     = 0.1111111111111111111,
  CH_Low     = 0.1111111111111111111,
  CL_Average = 0.1111111111111111111,
  CA_Average = 0.1111111111111111111,
  CH_Average = 0.1111111111111111111,
  CL_High    = 0.1111111111111111111,
  CA_High    = 0.1111111111111111111,
  CH_High    = 0.1111111111111111111,
)
rates = {
  'Demand' : dict(
    CL_Low     = (('*,*,RH', 0.89),('*,*,RL', 1.21),('*,*,TX', 1.10)),
    CA_Low     = (('*,*,RH', 0.89),('*,*,RL', 1.21),('*,*,TX', 1.10)),
    CH_Low     = (('*,*,RH', 0.89),('*,*,RL', 1.21),('*,*,TX', 1.10)),
    CL_Average = (('*,*,RH', 1.01),('*,*,RL', 1.61),('*,*,TX', 1.30)),
    CA_Average = (('*,*,RH', 1.01),('*,*,RL', 1.61),('*,*,TX', 1.30)),
    CH_Average = (('*,*,RH', 1.01),('*,*,RL', 1.61),('*,*,TX', 1.30)),
    CL_High    = (('*,*,RH', 1.13),('*,*,RL', 2.39),('*,*,TX', 1.40)),
    CA_High    = (('*,*,RH', 1.13),('*,*,RL', 2.39),('*,*,TX', 1.40)),
    CH_High    = (('*,*,RH', 1.13),('*,*,RL', 2.39),('*,*,TX', 1.40)),
    ),
  'CostInvest' : dict(
    CL_Low     = (('E01,*', 1.8),('E21,*', 1.2),),
    CL_Average = (('E01,*', 1.8),('E21,*', 1.2),),
    CL_High    = (('E01,*', 1.8),('E21,*', 1.2),),
    CA_Low     = (('E01,*', 2.0),('E21,*', 0.7),),
    CA_Average = (('E01,*', 2.0),('E21,*', 0.7),),
    CA_High    = (('E01,*', 2.0),('E21,*', 0.7),),
    CH_Low     = (('E01,*', 2.2),('E21,*', 0.2),),
    CH_Average = (('E01,*', 2.2),('E21,*', 0.2),),
    CH_High    = (('E01,*', 2.2),('E21,*', 0.2),),
    ),
}
