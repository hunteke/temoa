
verbose = True
force = True

dirname    = 'temoa_island_markoved'
modelpath  = '../temoa_model.py'
dotdatpath = '../data_files/temoa_island.dat'
stochasticset = 'time_optimize'
stochastic_points = (2020, 2025, 2030, 2035)
stochastic_indices = {'Demand': 0, 'CostMarginal': 0}
types = (
  'DDU', 'DUU',
  'UDD', 'UDU',
  'UUD', 'UUU',
)
conditional_probability = dict(
  #HedgingStrategy = (('DDU', 15./352), ('DUU', 9./352), ('UDD', 9./32), ('UDU', 9./88), ('UUD', 5./44), ('UUU', 153./352)),
  HedgingStrategy = (('DDU', 1./38), ('DUU', 3./38), ('UDD', 9./38), ('UDU', 4./38), ('UUD', 4./38), ('UUU', 17./38)),
  DDU = (('UDU', 1),),
  DUU = (('DUU', 2./ 3), ('UUU', 1./ 3)),
  UDD = (('UDD', 7./ 9), ('UDU', 1./ 9), ('UUD', 1./ 9)),
  UDU = (('UDD', 1./ 3), ('UUU', 2./ 3)),
  UUD = (('UDD', 1./ 4), ('UDU', 1./ 4), ('UUD', 2./ 4)),
  UUU = (('DDU', 1./17), ('DUU', 1./17), ('UUD', 1./17), ('UUU', 14./17)),
)

rates = {
  'Demand' : dict(
    HedgingStrategyDDU = (('*,*,r_cooling', 1.00495), ('*,*,r_heating', 1.00495), ('*,*,r_lighting', 1.00495), ('*,*,r_wheating', 1.00495)),
    HedgingStrategyDUU = (('*,*,r_cooling', 1.00495), ('*,*,r_heating', 1.00495), ('*,*,r_lighting', 1.00495), ('*,*,r_wheating', 1.00495)),
    HedgingStrategyUDD = (('*,*,r_cooling', 1.00495), ('*,*,r_heating', 1.00495), ('*,*,r_lighting', 1.00495), ('*,*,r_wheating', 1.00495)),
    HedgingStrategyUDU = (('*,*,r_cooling', 1.00495), ('*,*,r_heating', 1.00495), ('*,*,r_lighting', 1.00495), ('*,*,r_wheating', 1.00495)),
    HedgingStrategyUUD = (('*,*,r_cooling', 1.00495), ('*,*,r_heating', 1.00495), ('*,*,r_lighting', 1.00495), ('*,*,r_wheating', 1.00495)),
    HedgingStrategyUUU = (('*,*,r_cooling', 1.00495), ('*,*,r_heating', 1.00495), ('*,*,r_lighting', 1.00495), ('*,*,r_wheating', 1.00495)),
    DDUUDU = (('*,*,r_cooling', 1.00495), ('*,*,r_heating', 1.00495), ('*,*,r_lighting', 1.00495), ('*,*,r_wheating', 1.00495)),
    DUUDUU = (('*,*,r_cooling', 0.99466), ('*,*,r_heating', 0.99466), ('*,*,r_lighting', 0.99466), ('*,*,r_wheating', 0.99466)),
    DUUUUU = (('*,*,r_cooling', 1.00189), ('*,*,r_heating', 1.00189), ('*,*,r_lighting', 1.00189), ('*,*,r_wheating', 1.00189)),
    UDDUDD = (('*,*,r_cooling', 1.01602), ('*,*,r_heating', 1.01602), ('*,*,r_lighting', 1.01602), ('*,*,r_wheating', 1.01602)),
    UDDUDU = (('*,*,r_cooling', 1.01718), ('*,*,r_heating', 1.01718), ('*,*,r_lighting', 1.01718), ('*,*,r_wheating', 1.01718)),
    UDDUUD = (('*,*,r_cooling', 1.01755), ('*,*,r_heating', 1.01755), ('*,*,r_lighting', 1.01755), ('*,*,r_wheating', 1.01755)),
    UDUUDD = (('*,*,r_cooling', 1.01277), ('*,*,r_heating', 1.01277), ('*,*,r_lighting', 1.01277), ('*,*,r_wheating', 1.01277)),
    UDUUUU = (('*,*,r_cooling', 1.02045), ('*,*,r_heating', 1.02045), ('*,*,r_lighting', 1.02045), ('*,*,r_wheating', 1.02045)),
    UUDUDD = (('*,*,r_cooling', 1.00928), ('*,*,r_heating', 1.00928), ('*,*,r_lighting', 1.00928), ('*,*,r_wheating', 1.00928)),
    UUDUDU = (('*,*,r_cooling', 1.01536), ('*,*,r_heating', 1.01536), ('*,*,r_lighting', 1.01536), ('*,*,r_wheating', 1.01536)),
    UUDUUD = (('*,*,r_cooling', 1.00851), ('*,*,r_heating', 1.00851), ('*,*,r_lighting', 1.00851), ('*,*,r_wheating', 1.00851)),
    UUUDDU = (('*,*,r_cooling', 0.99972), ('*,*,r_heating', 0.99972), ('*,*,r_lighting', 0.99972), ('*,*,r_wheating', 0.99972)),
    UUUDUU = (('*,*,r_cooling', 0.99811), ('*,*,r_heating', 0.99811), ('*,*,r_lighting', 0.99811), ('*,*,r_wheating', 0.99811)),
    UUUUUD = (('*,*,r_cooling', 1.00370), ('*,*,r_heating', 1.00370), ('*,*,r_lighting', 1.00370), ('*,*,r_wheating', 1.00370)),
    UUUUUU = (('*,*,r_cooling', 1.01252), ('*,*,r_heating', 1.01252), ('*,*,r_lighting', 1.01252), ('*,*,r_wheating', 1.01252)),
  ),
  'CostMarginal' : dict(
    HedgingStrategyDDU = (('imp_natgas,*', 0.95851), ('imp_oil,*', 1.05404)),
    HedgingStrategyDUU = (('imp_natgas,*', 0.95851), ('imp_oil,*', 1.05404)),
    HedgingStrategyUDD = (('imp_natgas,*', 0.95851), ('imp_oil,*', 1.05404)),
    HedgingStrategyUDU = (('imp_natgas,*', 0.95851), ('imp_oil,*', 1.05404)),
    HedgingStrategyUUD = (('imp_natgas,*', 0.95851), ('imp_oil,*', 1.05404)),
    HedgingStrategyUUU = (('imp_natgas,*', 0.95851), ('imp_oil,*', 1.05404)),
    DDUUDU = (('imp_natgas,*', 0.95851), ('imp_oil,*', 1.05404)),
    DUUDUU = (('imp_natgas,*', 1.09834), ('imp_oil,*', 1.12885)),
    DUUUUU = (('imp_natgas,*', 1.08055), ('imp_oil,*', 1.05921)),
    UDDUDD = (('imp_natgas,*', 0.97620), ('imp_oil,*', 0.92748)),
    UDDUDU = (('imp_natgas,*', 0.96486), ('imp_oil,*', 1.01777)),
    UDDUUD = (('imp_natgas,*', 1.01319), ('imp_oil,*', 0.98969)),
    UDUUDD = (('imp_natgas,*', 0.97908), ('imp_oil,*', 0.97672)),
    UDUUUU = (('imp_natgas,*', 1.01937), ('imp_oil,*', 1.11640)),
    UUDUDD = (('imp_natgas,*', 0.98418), ('imp_oil,*', 0.86917)),
    UUDUDU = (('imp_natgas,*', 0.99185), ('imp_oil,*', 1.00967)),
    UUDUUD = (('imp_natgas,*', 1.01229), ('imp_oil,*', 0.89315)),
    UUUDDU = (('imp_natgas,*', 0.99952), ('imp_oil,*', 1.04516)),
    UUUDUU = (('imp_natgas,*', 1.08050), ('imp_oil,*', 1.25541)),
    UUUUUD = (('imp_natgas,*', 1.04847), ('imp_oil,*', 0.97251)),
    UUUUUU = (('imp_natgas,*', 1.05870), ('imp_oil,*', 1.12725)),
  )
}
