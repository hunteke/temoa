
verbose = True
force = True

modelpath  = '../energysystem-process-Coopr3/temoa_model/temoa_model.py'
dotdatpath = '../energysystem-datfiles/temoa_island.dat'
stochasticset = 'time_optimize'
stochastic_points = (2020, 2025, 2030, 2035)
stochastic_indices = {'Demand': 0, 'CostMarginal': 0}
types = (
  'DemD_NatD_OilD', 'DemD_NatD_OilU',
  'DemD_NatU_OilD', 'DemD_NatU_OilU',
  'DemU_NatD_OilD', 'DemU_NatD_OilU',
  'DemU_NatU_OilD', 'DemU_NatU_OilU',
)
conditional_probability = dict(
  DemD_NatD_OilD = 0.0952,
  DemD_NatD_OilU = 0.0238,
  DemD_NatU_OilD = 0.0952,
  DemD_NatU_OilU = 0.1429,
  DemU_NatD_OilD = 0.1429,
  DemU_NatD_OilU = 0.1667,
  DemU_NatU_OilD = 0.0952,
  DemU_NatU_OilU = 0.2381,
)

rates = {
  'Demand' : dict(
    DemD_NatD_OilD = (('*,*,r_cooling', 0.99174), ('*,*,r_heating', 0.99174), ('*,*,r_lighting', 0.99174) ,('*,*,r_wheating', 0.99174)),
    DemD_NatD_OilU = (('*,*,r_cooling', 0.95275), ('*,*,r_heating', 0.95275), ('*,*,r_lighting', 0.95275) ,('*,*,r_wheating', 0.95275)),
    DemD_NatU_OilD = (('*,*,r_cooling', 0.98525), ('*,*,r_heating', 0.98525), ('*,*,r_lighting', 0.98525) ,('*,*,r_wheating', 0.98525)),
    DemD_NatU_OilU = (('*,*,r_cooling', 0.98086), ('*,*,r_heating', 0.98086), ('*,*,r_lighting', 0.98086) ,('*,*,r_wheating', 0.98086)),
    DemU_NatD_OilD = (('*,*,r_cooling', 1.03415), ('*,*,r_heating', 1.03415), ('*,*,r_lighting', 1.03415) ,('*,*,r_wheating', 1.03415)),
    DemU_NatD_OilU = (('*,*,r_cooling', 1.03879), ('*,*,r_heating', 1.03879), ('*,*,r_lighting', 1.03879) ,('*,*,r_wheating', 1.03879)),
    DemU_NatU_OilD = (('*,*,r_cooling', 1.03762), ('*,*,r_heating', 1.03762), ('*,*,r_lighting', 1.03762) ,('*,*,r_wheating', 1.03762)),
    DemU_NatU_OilU = (('*,*,r_cooling', 1.02335), ('*,*,r_heating', 1.02335), ('*,*,r_lighting', 1.02335) ,('*,*,r_wheating', 1.02335)),
    ),
  'CostMarginal' : dict(
    DemD_NatD_OilD = (('imp_natgas,*', 0.93990), ('imp_oil,*', 0.68706)),
    DemD_NatD_OilU = (('imp_natgas,*', 0.99014), ('imp_oil,*', 1.21704)),
    DemD_NatU_OilD = (('imp_natgas,*', 1.10940), ('imp_oil,*', 0.88880)),
    DemD_NatU_OilU = (('imp_natgas,*', 1.06994), ('imp_oil,*', 1.34811)),
    DemU_NatD_OilD = (('imp_natgas,*', 0.94335), ('imp_oil,*', 0.91011)),
    DemU_NatD_OilU = (('imp_natgas,*', 0.94433), ('imp_oil,*', 1.16201)),
    DemU_NatU_OilD = (('imp_natgas,*', 1.06591), ('imp_oil,*', 0.92133)),
    DemU_NatU_OilU = (('imp_natgas,*', 1.07795), ('imp_oil,*', 1.18608)),
    )
}
