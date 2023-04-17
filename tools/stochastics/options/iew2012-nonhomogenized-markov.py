
verbose = True
force = True

dirname    = 'temoa_island_markoved'
modelpath  = '../temoa_model.py'
dotdatpath = '../data_files/iew2012.dat'
stochasticset = 'time_optimize'
stochastic_points = (2020, 2025, 2030, 2035)
stochastic_indices = {'CostMarginal': 0}
types = (
  'DDD', 'DDU', 'DUD', 'DUU',
  'UDD', 'UDU', 'UUU',
)

conditional_probability = dict(
  HedgingStrategy = (('DDD', 13./57), ('DDU', 1./57), ('DUD', 12./57), ('DUU', 14./57), ('UDD', 3./57 ), ('UDU', 2./57 ), ('UUU', 12./57)),
  DDD = (('DDD', 8./13), ('DDU', 1./13), ('DUD', 1./13), ('DUU', 2./13), ('UDD', 1./13)),
  DDU = (('DDD', 1),),
  DUD = (('DDD', 4./12), ('DUD', 7./12), ('DUU',1./12)),
  DUU = (('DUD',  3./14), ('DUU', 10./14), ('UUU',  1./14)),
  UDD = (('UDD', 2./3), ('UUU', 1./3)),
  UDU = (('UDU', 1),),
  UUU = (('DUU', 1./12), ('UDU', 1./12), ('UUU', 10./12)),
)

rates = {
  'CostMarginal' : dict(
    HedgingStrategyDDD = (('imp_coal', 1.06637), ('imp_natgas,*', 0.88132), ('imp_oil,*', 1.05582)),
    HedgingStrategyDDU = (('imp_coal', 1.06637), ('imp_natgas,*', 0.88132), ('imp_oil,*', 1.05582)),
    HedgingStrategyDUD = (('imp_coal', 1.06637), ('imp_natgas,*', 0.88132), ('imp_oil,*', 1.05582)),
    HedgingStrategyDUU = (('imp_coal', 1.06637), ('imp_natgas,*', 0.88132), ('imp_oil,*', 1.05582)),
    HedgingStrategyUDD = (('imp_coal', 1.06637), ('imp_natgas,*', 0.88132), ('imp_oil,*', 1.05582)),
    HedgingStrategyUDU = (('imp_coal', 1.06637), ('imp_natgas,*', 0.88132), ('imp_oil,*', 1.05582)),
    HedgingStrategyUUU = (('imp_coal', 1.06637), ('imp_natgas,*', 0.88132), ('imp_oil,*', 1.05582)),
    DDDDDD = (('imp_coal,*', 0.95886), ('imp_natgas,*', 0.93415), ('imp_oil,*', 0.91485)),
    DDDDDU = (('imp_coal,*', 0.94783), ('imp_natgas,*', 0.93143), ('imp_oil,*', 1.01982)),
    DDDDUD = (('imp_coal,*', 0.95210), ('imp_natgas,*', 1.00764), ('imp_oil,*', 0.99502)),
    DDDDUU = (('imp_coal,*', 0.95412), ('imp_natgas,*', 1.02703), ('imp_oil,*', 1.00843)),
    DDDUDD = (('imp_coal,*', 1.03169), ('imp_natgas,*', 0.97375), ('imp_oil,*', 0.98145)),
    DDUDDD = (('imp_coal,*', 0.95059), ('imp_natgas,*', 0.97436), ('imp_oil,*', 0.97492)),
    DUDDDD = (('imp_coal,*', 0.95935), ('imp_natgas,*', 0.98153), ('imp_oil,*', 0.92444)),
    DUDDUD = (('imp_coal,*', 0.96920), ('imp_natgas,*', 1.03930), ('imp_oil,*', 0.98458)),
    DUDDUU = (('imp_coal,*', 0.97144), ('imp_natgas,*', 1.06985), ('imp_oil,*', 1.00170)),
    DUUDUD = (('imp_coal,*', 0.96475), ('imp_natgas,*', 1.03622), ('imp_oil,*', 0.98506)),
    DUUDUU = (('imp_coal,*', 0.97600), ('imp_natgas,*', 1.11657), ('imp_oil,*', 1.09607)),
    DUUUUU = (('imp_coal,*', 1.01655), ('imp_natgas,*', 1.16025), ('imp_oil,*', 1.15942)),
    UDDUDD = (('imp_coal,*', 1.05568), ('imp_natgas,*', 0.98233), ('imp_oil,*', 0.98602)),
    UDDUUU = (('imp_coal,*', 1.07542), ('imp_natgas,*', 1.01397), ('imp_oil,*', 1.00729)),
    UDUUDU = (('imp_coal,*', 1.06637), ('imp_natgas,*', 0.88132), ('imp_oil,*', 1.05582)),
    UUUDUU = (('imp_coal,*', 0.98426), ('imp_natgas,*', 1.20240), ('imp_oil,*', 1.18666)),
    UUUUDU = (('imp_coal,*', 1.08067), ('imp_natgas,*', 0.92897), ('imp_oil,*', 1.04542)),
    UUUUUU = (('imp_coal,*', 1.10292), ('imp_natgas,*', 1.14894), ('imp_oil,*', 1.13962)),
  )
}
