BEGIN TRANSACTION;

-------------------------------------------------
CREATE TABLE time_period_labels (
  t_period_labels text primary key,
  t_period_labels_desc text);
INSERT INTO "time_period_labels" VALUES('e', 'existing vintages');
INSERT INTO "time_period_labels" VALUES('f', 'future');

CREATE TABLE time_periods (
  t_periods integer primary key,
  flag text,
  FOREIGN KEY(flag) REFERENCES time_period_labels(t_period_labels));  

INSERT INTO "time_periods" VALUES(1910,'e');
INSERT INTO "time_periods" VALUES(1915,'e');
INSERT INTO "time_periods" VALUES(1920,'e');
INSERT INTO "time_periods" VALUES(1925,'e');
INSERT INTO "time_periods" VALUES(1930,'e');
INSERT INTO "time_periods" VALUES(1935,'e');
INSERT INTO "time_periods" VALUES(1940,'e');
INSERT INTO "time_periods" VALUES(1945,'e');
INSERT INTO "time_periods" VALUES(1950,'e');
INSERT INTO "time_periods" VALUES(1955,'e');
INSERT INTO "time_periods" VALUES(1960,'e');
INSERT INTO "time_periods" VALUES(1965,'e');
INSERT INTO "time_periods" VALUES(1970,'e');
INSERT INTO "time_periods" VALUES(1975,'e');
INSERT INTO "time_periods" VALUES(1980,'e');
INSERT INTO "time_periods" VALUES(1985,'e');
INSERT INTO "time_periods" VALUES(1990,'e');
INSERT INTO "time_periods" VALUES(1995,'e');
INSERT INTO "time_periods" VALUES(2000,'e');
INSERT INTO "time_periods" VALUES(2005,'e');
INSERT INTO "time_periods" VALUES(2010,'e');

INSERT INTO "time_periods" VALUES(2015,'f');
INSERT INTO "time_periods" VALUES(2020,'f');
INSERT INTO "time_periods" VALUES(2025,'f');
INSERT INTO "time_periods" VALUES(2030,'f');
INSERT INTO "time_periods" VALUES(2035,'f');
INSERT INTO "time_periods" VALUES(2040,'f');
INSERT INTO "time_periods" VALUES(2045,'f');
INSERT INTO "time_periods" VALUES(2050,'f');
INSERT INTO "time_periods" VALUES(2055,'f');

-------------------------------------------------
CREATE TABLE time_season (
  t_season text primary key );

INSERT INTO "time_season" VALUES('s001');
INSERT INTO "time_season" VALUES('s002');
INSERT INTO "time_season" VALUES('s003');
INSERT INTO "time_season" VALUES('s004');

-------------------------------------------------
CREATE TABLE time_of_day (
  t_day text primary key );

INSERT INTO "time_of_day" VALUES('tod01');
INSERT INTO "time_of_day" VALUES('tod02');
INSERT INTO "time_of_day" VALUES('tod03');
INSERT INTO "time_of_day" VALUES('tod04');
INSERT INTO "time_of_day" VALUES('tod05');
INSERT INTO "time_of_day" VALUES('tod06');
INSERT INTO "time_of_day" VALUES('tod07');
INSERT INTO "time_of_day" VALUES('tod08');
INSERT INTO "time_of_day" VALUES('tod09');
INSERT INTO "time_of_day" VALUES('tod10');
INSERT INTO "time_of_day" VALUES('tod11');
INSERT INTO "time_of_day" VALUES('tod12');
INSERT INTO "time_of_day" VALUES('tod13');
INSERT INTO "time_of_day" VALUES('tod14');
INSERT INTO "time_of_day" VALUES('tod15');
INSERT INTO "time_of_day" VALUES('tod16');
INSERT INTO "time_of_day" VALUES('tod17');
INSERT INTO "time_of_day" VALUES('tod18');
INSERT INTO "time_of_day" VALUES('tod19');
INSERT INTO "time_of_day" VALUES('tod20');
INSERT INTO "time_of_day" VALUES('tod21');
INSERT INTO "time_of_day" VALUES('tod22');
INSERT INTO "time_of_day" VALUES('tod23');
INSERT INTO "time_of_day" VALUES('tod24');

-------------------------------------------------
CREATE TABLE technology_labels (
  tech_labels text primary key,
  tech_labels_desc text);
INSERT INTO "technology_labels" VALUES('r', 'resource technology');
INSERT INTO "technology_labels" VALUES('p', 'production technology');
INSERT INTO "technology_labels" VALUES('pb', 'baseload production technology');
INSERT INTO "technology_labels" VALUES('ps', 'storage production technology');

-------------------------------------------------
-- Assume baseload techs include coal plants, combined NG plants and nuclear plants
CREATE TABLE technologies (
  tech text primary key,
  flag text,
  sector text,
  tech_desc text,
  FOREIGN KEY(flag) REFERENCES technology_labels(tech_labels),
  FOREIGN KEY(sector) REFERENCES sector_labels(sector));

   INSERT INTO "technologies" VALUES('IMPELCNGCEA',     'r', 'supply',      '# Import NG to combustion cycle');
   INSERT INTO "technologies" VALUES('IMPELCNGAEA',	    'r', 'supply',      '# Import NG to combined cycle');
   INSERT INTO "technologies" VALUES('IMPELCDSLEA',	    'r', 'supply',      '# Import diesel');
   INSERT INTO "technologies" VALUES('IMPURNA',	        'r', 'supply',      '# Import uranium');
   INSERT INTO "technologies" VALUES('IMPELCBIGCCEA',   'r', 'supply',      '# Import biomass to IGCC');
   INSERT INTO "technologies" VALUES('IMPELCBIOSTM',	'r', 'supply',      '# Import biomass to steam');
   INSERT INTO "technologies" VALUES('IMPELCGEO',		'r', 'supply',      '# Import geothermal');
   INSERT INTO "technologies" VALUES('IMPSOL',			'r', 'supply',      '# Import solar');
   INSERT INTO "technologies" VALUES('IMPWND',          'r', 'supply',      '# Import wind');
   INSERT INTO "technologies" VALUES('IMPELCHYD',       'r', 'supply',      '# Import hydro');
   INSERT INTO "technologies" VALUES('IMPLFGICEEA',     'r', 'supply',      '# Import landfill gas to ICE');
   INSERT INTO "technologies" VALUES('IMPLFGGTREA',     'r', 'supply',      '# Import landfill gas to gas turbines');
   
   INSERT INTO "technologies" VALUES('ENGACC05',        'pb','electric',    '# Natural Gas - Combined-Cycle (Turbine)');
   INSERT INTO "technologies" VALUES('ENGACT05',        'p', 'electric',    '# Natural Gas - Combustion Turbine');
   INSERT INTO "technologies" VALUES('ENGAACC',         'pb','electric',    '# Natural Gas - Advanced Combined-Cycle (Turbine)');
   INSERT INTO "technologies" VALUES('ENGAACT',         'p', 'electric',    '# Natural Gas - Advanced Combustion Turbine');
   INSERT INTO "technologies" VALUES('ENGACCCCS',       'pb','electric',    '# Natural Gas Combined Cycle -- CO2 Capture');
   INSERT INTO "technologies" VALUES('ENGACCR',         'pb','electric',    '# Residual natural Gas Combined-Cycle');
   INSERT INTO "technologies" VALUES('ENGACTR',         'p', 'electric',    '# Residual natural Gas Combustion Turbine');
   INSERT INTO "technologies" VALUES('ECOALSTM',        'pb','electric',    '# Pulverized Coal Steam - 2010');
   INSERT INTO "technologies" VALUES('ECOALIGCC',       'pb','electric',    '# Integrated Coal Gasif. Combined Cycle');
   INSERT INTO "technologies" VALUES('ECOALIGCCS',      'pb','electric',    '# Integrated Coal Gasif. Combined Cycle -- CO2 Capt.');
   INSERT INTO "technologies" VALUES('ECOASTMR',        'pb','electric',    '# Residual Coal Steam');
   INSERT INTO "technologies" VALUES('EDSLCTR',         'p', 'electric',    '# Residual diesel Oil Combustion Turbine');
   INSERT INTO "technologies" VALUES('EURNALWR',        'pb','electric',    '# Residual Nuclear LWRs');
   INSERT INTO "technologies" VALUES('EURNALWR15',      'pb','electric',    '# Nuclear LWRs in 2015');
   INSERT INTO "technologies" VALUES('EBIOIGCC',        'p', 'electric',    '# Biomass Integrated Gasification Combined-Cycle');
   INSERT INTO "technologies" VALUES('EBIOSTMR',        'p', 'electric',    '# Residual wood/Biomass Steam');
   INSERT INTO "technologies" VALUES('EGEOBCFS',        'p', 'electric',    '# Geothermal - Binary Cycle and Flashed Steam');
   INSERT INTO "technologies" VALUES('ESOLPVCEN',       'p', 'electric',    '# Solar PV Centralized Generation');
   INSERT INTO "technologies" VALUES('ESOLSTCEN',       'p', 'electric',    '# Solar Thermal Centralized Generation');
   INSERT INTO "technologies" VALUES('ESOLPVR',         'p', 'electric',    '# Solar Photovoltaic');
   INSERT INTO "technologies" VALUES('EWNDON',          'p', 'electric',    '# Wind Generation onshore');
   INSERT INTO "technologies" VALUES('EWNDOFS',         'p', 'electric',    '# Wind Generation offshore');
   INSERT INTO "technologies" VALUES('EHYDCONR',        'p', 'electric',    '# Residual hydroelectric, Conventional');
   INSERT INTO "technologies" VALUES('EHYDREVR',        'ps','electric',    '# Residual hydroelectric, Reversible');
   INSERT INTO "technologies" VALUES('ELFGICER',        'p', 'electric',    '# Redidual landfill gas to electricity: engines');
   INSERT INTO "technologies" VALUES('ELFGGTR',         'p', 'electric',    '# Redidual landfill gas to electricity: gas turbines');
   INSERT INTO "technologies" VALUES('EHYDGS',          'p', 'electric',    '# Gulf Stream energy');
   
   INSERT INTO "technologies" VALUES('ELC2DMD',         'p', 'residential', '# Dummy ELC to ELCDMD');

-- Emission control technologies
   INSERT INTO "technologies" VALUES('E_BLND_BITSUBLIG_COALSTM_R',   'p','electric','#blending tech to collect bit subbit and lig coal for existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_BLND_BIT_COALSTM_R',         'p','electric','#blending tech to collect bit coal for existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_LNBSNCR_COAB_R',             'p','electric','#Existing LNB w/SNCR retrofit for nox removal from BIT before existing coal STM');
   INSERT INTO "technologies" VALUES('E_LNBSNCR_COAB_N',             'p','electric','#new LNB combined with SNCR retrofit for nox removal from bituminous before existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_LNBSCR_COAB_R',              'p','electric','#existing LNB combined with SCR retrofit for nox removal from bituminous before existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_LNBSCR_COAB_N',              'p','electric','#new LNB combined with SCR retrofit for nox removal from bituminous before existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_PTNOXSCR_COAB',              'p','electric','#nox passthrough tech for bituminous coal after LNB retrofit or passthrough and before existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_SNCR_COAB_R',                'p','electric','#existing SNCR retrofit for nox removal from bituminous before existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_SNCR_COAB_N',                'p','electric','#new SNCR retrofit for nox removal from bituminous before existing coal steam plant');
-- INSERT INTO "technologies" VALUES('E_SCR_COAB_R',                 'p','electric','#existing SCR retrofit for nox removal from bituminous before existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_SCR_COAB_N',                 'p','electric','#new SCR retrofit for nox removal from bituminous before existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_PTNOXLNB_COAB',              'p','electric','#nox passthrough tech for bituminous coal after so2 or co2 passthrough and before SCR or SNCR or passthrough');
   INSERT INTO "technologies" VALUES('E_LNB_COAB_R',                 'p','electric','#existing LNB retrofit tech for nox removal from bituminous before existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_LNB_COAB_N',                 'p','electric','#new LNB retrofit tech for nox removal from bituminous before existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_CCR_COAB',                   'p','electric','#co2 capture retrofit tech for bituminous coal to existing power plant located after FGD or passthrough and before LNB');
   INSERT INTO "technologies" VALUES('E_PTCO2_COAB',                 'p','electric','#co2 passthrough tech for bituminous coal after FGD and before LNB');
-- INSERT INTO "technologies" VALUES('E_FGD_COABH_R',                'p','electric','#existing FGD retrofit tech for so2 removal from bit high sulfur before existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_FGD_COABH_N',                'p','electric','#new FGD retrofit tech for so2 removal from bit high sulfur before existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_FGD_COABM_R',                'p','electric','#existing FGD retrofit tech for so2 removal from bit medium sulfur before existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_FGD_COABM_N',                'p','electric','#new FGD retrofit tech for so2 removal from bit medium sulfur before existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_FGD_COABL_R',                'p','electric','#existing FGD retrofit tech for so2 removal from bit low sulfur before existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_FGD_COABL_N',                'p','electric','#new FGD retrofit tech for so2 removal from bit low sulfur before existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_PTSO2_COABH',                'p','electric','#passthrough tech with no so2 removal from bit high sulfur before existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_PTSO2_COABM',                'p','electric','#passthrough tech with no so2 removal from bit medium sulfur before existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_PTSO2_COABL',                'p','electric','#passthrough tech with no so2 removal from bit low sulfur before existing coal steam plant');
   INSERT INTO "technologies" VALUES('E_EA_COAB',                    'p','electric','#co2 emission accounting tech for coal bituminous');
   INSERT INTO "technologies" VALUES('E_CCR_COALIGCC_N',             'p','electric','#co2 capture retrofit tech before coal IGCC plant');
   INSERT INTO "technologies" VALUES('E_BLND_BITSUBLIG_COALIGCC_N',  'p','electric','#blending tech to collect bit subbit and lig coal for new coal IGCC plant');
   INSERT INTO "technologies" VALUES('E_BLND_BITHML_COALIGCC_N',     'p','electric','#blending tech to collect high medium low sulfur bit coal for new coal IGCC plant');
   INSERT INTO "technologies" VALUES('E_CCR_COALSTM_N',              'p','electric','#co2 capture retrofit tech before new coal steam plant');
   INSERT INTO "technologies" VALUES('E_BLND_BITSUBLIG_COALSTM_N',   'p','electric','#blending tech to collect bit subbit and lig coal for new coal steam plant');
   INSERT INTO "technologies" VALUES('E_BLND_BITHML_COALSTM_N',      'p','electric','#blending tech to collect high medium low sulfur bit coal for new coal steam plant');

-- Sammaneh's importing techs
   INSERT INTO "technologies" VALUES('IMPELCCOAB',                   'r','supply',   '#imported bituminous coal');

-------------------------------------------------
CREATE TABLE commodity_labels (
  comm_labels text primary key,
  comm_labels_desc text);
INSERT INTO "commodity_labels" VALUES('p', 'physical commodity');
INSERT INTO "commodity_labels" VALUES('e', 'emissions commodity');
INSERT INTO "commodity_labels" VALUES('d', 'demand commodity');

-------------------------------------------------
CREATE TABLE commodities (
  comm_name text primary key,
  flag text,  
  comm_desc text,
  FOREIGN KEY(flag) REFERENCES commodity_labels(comm_labels));
INSERT INTO "commodities" VALUES('ethos',		'p', '# dummy commodity to supply inputs (makes graph easier to read)');
INSERT INTO "commodities" VALUES('COALSTMCC',	'p', '# Coal');
INSERT INTO "commodities" VALUES('COALIGCCCC',	'p', '# Coal');
INSERT INTO "commodities" VALUES('COALIGCC',	'p', '# Coal');
-- INSERT INTO "commodities" VALUES('COALSTMN',	'p', '# Coal');
INSERT INTO "commodities" VALUES('COALSTM',		'p', '# Coal');
INSERT INTO "commodities" VALUES('ELCNGCEA',	'p', '# NG');
INSERT INTO "commodities" VALUES('ELCNGAEA',	'p', '# NG');
-- INSERT INTO "commodities" VALUES('ELCNGSEA',	'p', '# NG');
INSERT INTO "commodities" VALUES('ELCDSLEA',	'p', '# Diesel');
-- INSERT INTO "commodities" VALUES('ELCRFLEA',	'p', '# Residual fuel oil');
INSERT INTO "commodities" VALUES('URNA',		'p', '# Uranium');
INSERT INTO "commodities" VALUES('ELCBIGCCEA',	'p', '# Biomass to IGCC');
INSERT INTO "commodities" VALUES('ELCBIOSTM',	'p', '# Biomass to steam');
INSERT INTO "commodities" VALUES('ELCGEO',		'p', '# Geothermal');
INSERT INTO "commodities" VALUES('SOL',	        'p', '# Solar');
INSERT INTO "commodities" VALUES('WND',			'p', '# Wind');
INSERT INTO "commodities" VALUES('ELCHYD',		'p', '# Hydro');
-- INSERT INTO "commodities" VALUES('ELCMSWEA',	'p', '# Solid waste');
INSERT INTO "commodities" VALUES('ELC',			'p', '# Electricity, physical');
INSERT INTO "commodities" VALUES('ELCDMD',		'd', '# Electricity, demand');
INSERT INTO "commodities" VALUES('LFGICEEA',    'p', '# Landfill gas to ICE');
INSERT INTO "commodities" VALUES('LFGGTREA',    'p', '# Landfill gas to gas turbines');

-- Emission commodities
INSERT INTO "commodities" VALUES('co2_ELC',           'e','# CO2 emissions from the electric sector');
INSERT INTO "commodities" VALUES('so2_ELC',           'e','# SO2 emissions from the electric sector');
INSERT INTO "commodities" VALUES('nox_ELC',           'e','# NOX emissions from the electric sector');
INSERT INTO "commodities" VALUES('co2_SUP',           'e','# CO2 emissions from the supply sector');
INSERT INTO "commodities" VALUES('so2_SUP',           'e','# SO2 emissions from the supply sector');
INSERT INTO "commodities" VALUES('nox_SUP',           'e','# NOX emissions from the supply sector');

-- Emission control technologies related intermediate commodities
INSERT INTO "commodities" VALUES('COALSTM_R_B',       'p','# Existing BIT coal steam to the blending tech');
INSERT INTO "commodities" VALUES('COAB_R',            'p','# Existing BIT coal after SCR/SNCR or SCR PT to the bit blending technology for existing coal steam');
INSERT INTO "commodities" VALUES('COAB_R_SCR_PT',     'p','# existing bituminous coal after LNB retrofit or passthrough to the SCR SNCSR nox retrofit or passthrough');
INSERT INTO "commodities" VALUES('COAB_R_LNB',        'p','# existing bituminous coal after co2 capture to the LNB retrofit');
INSERT INTO "commodities" VALUES('COAB_R_LNB_PT',     'p','# existing bituminous coal after so2 or co2 passthrough to the LNB nox retrofit or passthrough');
INSERT INTO "commodities" VALUES('COAB_R_CC',         'p','# existing bituminous coal after so2 removal to the co2 capture retrofit or passthrough');
INSERT INTO "commodities" VALUES('COABH_R',           'p','# bituminous high sulfur to the blending tech then existing coal plant');
INSERT INTO "commodities" VALUES('COABM_R',           'p','# bituminous medium sulfur to the blending tech then existing coal plant');
INSERT INTO "commodities" VALUES('COABL_R',           'p','# bituminous low sulfur to the blending tech then existing coal plant');
INSERT INTO "commodities" VALUES('COAB_EA',           'p','# bituminous coal to co2 emission accounting tech');
INSERT INTO "commodities" VALUES('COALIGCC_N_CC',     'p','# coal IGCC to co2 emission capture retrofit');
INSERT INTO "commodities" VALUES('COALIGCC_N_B',        'p','# bituminous new coal IGCC to the blending tech');
INSERT INTO "commodities" VALUES('COABH_IGCC_N',        'p','# bituminous high sulfur to the blending tech then new coal IGCC plant');
INSERT INTO "commodities" VALUES('COABM_IGCC_N',        'p','# bituminous medium sulfur to the blending tech then new coal IGCC plant');
INSERT INTO "commodities" VALUES('COABL_IGCC_N',        'p','# bituminous low sulfur to the blending tech then new coal IGCC plant');
INSERT INTO "commodities" VALUES('COALSTM_N_CC',      'p','# new coal to co2 emission capture retrofit');
INSERT INTO "commodities" VALUES('COALSTM_N_B',       'p','# bituminous new coal steam to the blending tech');
INSERT INTO "commodities" VALUES('COABH_N',           'p','# bituminous high sulfur to the blending tech then new coal steam plant');
INSERT INTO "commodities" VALUES('COABL_N',           'p','# bituminous low sulfur to the blending tech then new coal steam plant');
INSERT INTO "commodities" VALUES('COABM_N',           'p','# bituminous medium sulfur to the blending tech then new coal steam plant');

-------------------------------------------------
CREATE TABLE SegFrac (
   season_name text,
   time_of_day_name text,
   segfrac real check (segfrac>=0 AND segfrac<=1),
   segfrac_notes text,
   PRIMARY KEY(season_name, time_of_day_name), --here's where I define primary key as a combo of columns
   FOREIGN KEY(season_name) REFERENCES time_season(t_season),
   FOREIGN KEY(time_of_day_name) REFERENCES time_of_day(t_day) );

-- Below is based on 4 seasons and 24 tods
INSERT INTO "SegFrac" VALUES('s001', 'tod01', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod02', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod03', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod04', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod05', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod06', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod07', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod08', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod09', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod10', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod11', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod12', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod13', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod14', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod15', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod16', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod17', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod18', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod19', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod20', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod21', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod22', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod23', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s001', 'tod24', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod01', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod02', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod03', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod04', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod05', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod06', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod07', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod08', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod09', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod10', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod11', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod12', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod13', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod14', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod15', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod16', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod17', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod18', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod19', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod20', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod21', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod22', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod23', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s002', 'tod24', 0.01050228,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod01', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod02', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod03', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod04', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod05', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod06', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod07', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod08', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod09', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod10', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod11', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod12', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod13', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod14', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod15', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod16', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod17', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod18', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod19', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod20', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod21', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod22', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod23', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s003', 'tod24', 0.01038813,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod01', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod02', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod03', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod04', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod05', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod06', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod07', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod08', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod09', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod10', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod11', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod12', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod13', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod14', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod15', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod16', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod17', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod18', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod19', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod20', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod21', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod22', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod23', 0.01027397,'');
INSERT INTO "SegFrac" VALUES('s004', 'tod24', 0.01027397,'');

-------------------------------------------------
CREATE TABLE Efficiency (
  input_comm text,
  tech text,
  vintage integer,
  output_comm text,
  efficiency real check (efficiency>0),
  eff_notes text,
  PRIMARY KEY(input_comm, tech, vintage, output_comm),
  FOREIGN KEY(input_comm) REFERENCES commodities(comm_name), 
  FOREIGN KEY(tech) REFERENCES technologies(tech),
  FOREIGN KEY(vintage) REFERENCES time_periods(t_periods), 
  FOREIGN KEY(output_comm) REFERENCES commodities(comm_name) );

   INSERT INTO "Efficiency" VALUES('ethos','IMPELCNGCEA',	2015,'ELCNGCEA',	1.00,'');
   INSERT INTO "Efficiency" VALUES('ethos','IMPELCNGAEA',	2015,'ELCNGAEA',	1.00,'');
-- INSERT INTO "Efficiency" VALUES('ethos','IMPELCNGSEA',	2015,'ELCNGSEA',	1.00,'');
   INSERT INTO "Efficiency" VALUES('ethos','IMPELCDSLEA',	2015,'ELCDSLEA',	1.00,'');
-- INSERT INTO "Efficiency" VALUES('ethos','IMPELCRFLEA',	2015,'ELCRFLEA',	1.00,'');
   INSERT INTO "Efficiency" VALUES('ethos','IMPURNA',		2015,'URNA',		1.00,'');
   INSERT INTO "Efficiency" VALUES('ethos','IMPELCBIGCCEA', 2015,'ELCBIGCCEA',	1.00,'');
   INSERT INTO "Efficiency" VALUES('ethos','IMPELCBIOSTM',	2015,'ELCBIOSTM',	1.00,'');
   INSERT INTO "Efficiency" VALUES('ethos','IMPELCGEO',	    2015,'ELCGEO',		1.00,'');
   INSERT INTO "Efficiency" VALUES('ethos','IMPSOL',		2015,'SOL',			1.00,'');
   INSERT INTO "Efficiency" VALUES('ethos','IMPWND',		2015,'WND',			1.00,'');
   INSERT INTO "Efficiency" VALUES('ethos','IMPELCHYD',	    2015,'ELCHYD',		1.00,'');
-- INSERT INTO "Efficiency" VALUES('ethos','IMPELCMSWEA',	2015,'ELCMSWEA',	1.00,'');
   INSERT INTO "Efficiency" VALUES('ethos','IMPLFGICEEA',	2015,'LFGICEEA',	1.00,'');
   INSERT INTO "Efficiency" VALUES('ethos','IMPLFGGTREA',	2015,'LFGGTREA',	1.00,'');

-- Natural gas, both existing and future
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACC05',	2015,'ELC',0.484,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGACT05',	2015,'ELC',0.313,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGAACC',	2015,'ELC',0.531,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGAACT',	2015,'ELC',0.350,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACCCCS',	2015,'ELC',0.455,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACC05',	2020,'ELC',0.493,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGACT05',	2020,'ELC',0.345,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGAACC',	2020,'ELC',0.535,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGAACT',	2020,'ELC',0.373,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACCCCS',	2020,'ELC',0.455,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACC05',	2025,'ELC',0.502,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGACT05',	2025,'ELC',0.385,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGAACC',	2025,'ELC',0.539,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGAACT',	2025,'ELC',0.399,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACCCCS',	2025,'ELC',0.455,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACC05',	2030,'ELC',0.502,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGACT05',	2030,'ELC',0.385,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGAACC',	2030,'ELC',0.539,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGAACT',	2030,'ELC',0.399,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACCCCS',	2030,'ELC',0.455,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACC05',	2035,'ELC',0.502,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGACT05',	2035,'ELC',0.385,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGAACC',	2035,'ELC',0.539,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGAACT',	2035,'ELC',0.399,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACCCCS',	2035,'ELC',0.455,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACC05',	2040,'ELC',0.502,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGACT05',	2040,'ELC',0.385,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGAACC',	2040,'ELC',0.539,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGAACT',	2040,'ELC',0.399,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACCCCS',	2040,'ELC',0.455,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACC05',	2045,'ELC',0.502,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGACT05',	2045,'ELC',0.385,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGAACC',	2045,'ELC',0.539,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGAACT',	2045,'ELC',0.399,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACCCCS',	2045,'ELC',0.455,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACC05',	2050,'ELC',0.502,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGACT05',	2050,'ELC',0.385,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGAACC',	2050,'ELC',0.539,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGAACT',	2050,'ELC',0.399,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACCCCS',	2050,'ELC',0.455,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACCR',	1970,'ELC',0.422,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACCR',	1975,'ELC',0.422,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACCR',	1980,'ELC',0.422,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACCR',	1985,'ELC',0.422,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACCR',	1990,'ELC',0.422,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACCR',	1995,'ELC',0.422,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACCR',	2000,'ELC',0.422,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGCEA','ENGACCR',	2005,'ELC',0.422,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGACTR',	1970,'ELC',0.248,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGACTR',	1975,'ELC',0.248,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGACTR',	1980,'ELC',0.248,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGACTR',	1985,'ELC',0.248,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGACTR',	1990,'ELC',0.248,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGACTR',	1995,'ELC',0.248,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGACTR',	2000,'ELC',0.248,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCNGAEA','ENGACTR',	2005,'ELC',0.248,'# MARKAL 2014 v1.1');

-- INSERT INTO "Efficiency" VALUES('ELCNGSEA','ENGASTMR',	2015,'ELC',0.286,'# From Samaneh NUSTD');

-- Coal, both existing and future
INSERT INTO "Efficiency" VALUES('COALSTMCC',	'ECOALSTM',		2015,'ELC',0.388,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALIGCCCC',	'ECOALIGCCS',	2015,'ELC',0.392,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALIGCC',		'ECOALIGCC',	2015,'ELC',0.411,'# MARKAL 2014 v1.1');
-- INSERT INTO "Efficiency" VALUES('COALSTMN',		'ECOALOXYCS',	2015,'ELC',0.411,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('COALSTMCC',	'ECOALSTM',		2020,'ELC',0.389,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALIGCCCC',	'ECOALIGCCS',	2020,'ELC',0.423,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALIGCC',		'ECOALIGCC',	2020,'ELC',0.411,'# MARKAL 2014 v1.1');
-- INSERT INTO "Efficiency" VALUES('COALSTMN',		'ECOALOXYCS',	2020,'ELC',0.411,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('COALSTMCC',	'ECOALSTM',		2025,'ELC',0.390,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALIGCCCC',	'ECOALIGCCS',	2025,'ELC',0.458,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALIGCC',		'ECOALIGCC',	2025,'ELC',0.411,'# MARKAL 2014 v1.1');
-- INSERT INTO "Efficiency" VALUES('COALSTMN',		'ECOALOXYCS',	2025,'ELC',0.411,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('COALSTMCC',	'ECOALSTM',		2030,'ELC',0.390,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALIGCCCC',	'ECOALIGCCS',	2030,'ELC',0.458,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALIGCC',		'ECOALIGCC',	2030,'ELC',0.411,'# MARKAL 2014 v1.1');
-- INSERT INTO "Efficiency" VALUES('COALSTMN',		'ECOALOXYCS',	2030,'ELC',0.411,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('COALSTMCC',	'ECOALSTM',		2035,'ELC',0.390,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALIGCCCC',	'ECOALIGCCS',	2035,'ELC',0.458,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALIGCC',		'ECOALIGCC',	2035,'ELC',0.411,'# MARKAL 2014 v1.1');
-- INSERT INTO "Efficiency" VALUES('COALSTMN',		'ECOALOXYCS',	2035,'ELC',0.411,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('COALSTMCC',	'ECOALSTM',		2040,'ELC',0.390,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALIGCCCC',	'ECOALIGCCS',	2040,'ELC',0.458,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALIGCC',		'ECOALIGCC',	2040,'ELC',0.411,'# MARKAL 2014 v1.1');
-- INSERT INTO "Efficiency" VALUES('COALSTMN',		'ECOALOXYCS',	2040,'ELC',0.411,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('COALSTMCC',	'ECOALSTM',		2045,'ELC',0.390,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALIGCCCC',	'ECOALIGCCS',	2045,'ELC',0.458,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALIGCC',		'ECOALIGCC',	2045,'ELC',0.411,'# MARKAL 2014 v1.1');
-- INSERT INTO "Efficiency" VALUES('COALSTMN',		'ECOALOXYCS',	2045,'ELC',0.411,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('COALSTMCC',	'ECOALSTM',		2050,'ELC',0.390,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALIGCCCC',	'ECOALIGCCS',	2050,'ELC',0.458,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALIGCC',		'ECOALIGCC',	2050,'ELC',0.411,'# MARKAL 2014 v1.1');
-- INSERT INTO "Efficiency" VALUES('COALSTMN',		'ECOALOXYCS',	2050,'ELC',0.411,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('COALSTM',		'ECOASTMR',		1970,'ELC',0.388,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALSTM',		'ECOASTMR',		1975,'ELC',0.388,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALSTM',		'ECOASTMR',		1980,'ELC',0.388,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALSTM',		'ECOASTMR',		1985,'ELC',0.388,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALSTM',		'ECOASTMR',		1990,'ELC',0.388,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALSTM',		'ECOASTMR',		1995,'ELC',0.388,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALSTM',		'ECOASTMR',		2000,'ELC',0.388,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('COALSTM',		'ECOASTMR',		2005,'ELC',0.388,'# MARKAL 2014 v1.1');

-- Oil, existing only
-- INSERT INTO "Efficiency" VALUES('ELCDSLEA',	'EDSLCCR',	1925,'ELC',0.322,'# From Samaneh NUSTD');
-- INSERT INTO "Efficiency" VALUES('ELCDSLEA',	'EDSLCCR',	1970,'ELC',0.322,'# From Samaneh NUSTD');

INSERT INTO "Efficiency" VALUES('ELCDSLEA',	'EDSLCTR',	1970,'ELC',0.224,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCDSLEA',	'EDSLCTR',	1975,'ELC',0.224,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCDSLEA',	'EDSLCTR',	1980,'ELC',0.224,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCDSLEA',	'EDSLCTR',	1985,'ELC',0.224,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCDSLEA',	'EDSLCTR',	1990,'ELC',0.224,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCDSLEA',	'EDSLCTR',	1995,'ELC',0.224,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCDSLEA',	'EDSLCTR',	2000,'ELC',0.224,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCDSLEA',	'EDSLCTR',	2005,'ELC',0.224,'# MARKAL 2014 v1.1');

-- INSERT INTO "Efficiency" VALUES('ELCRFLEA',	'ERFLSTMR',	2015,'ELC',0.260,'# From Samaneh NUSTD');

-- Nuclear, both existing and future
INSERT INTO "Efficiency" VALUES('URNA',	'EURNALWR',		2005,'ELC',1.427,'# PJ/ton, MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('URNA',	'EURNALWR15',	2015,'ELC',1.534,'# PJ/ton, MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('URNA',	'EURNALWR15',	2020,'ELC',1.534,'# PJ/ton, MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('URNA',	'EURNALWR15',	2025,'ELC',1.534,'# PJ/ton, MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('URNA',	'EURNALWR15',	2030,'ELC',1.534,'# PJ/ton, MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('URNA',	'EURNALWR15',	2035,'ELC',1.534,'# PJ/ton, MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('URNA',	'EURNALWR15',	2040,'ELC',1.534,'# PJ/ton, MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('URNA',	'EURNALWR15',	2045,'ELC',1.534,'# PJ/ton, MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('URNA',	'EURNALWR15',	2050,'ELC',1.534,'# PJ/ton, MARKAL 2014 v1.1');

-- Biomass, both existing and future
INSERT INTO "Efficiency" VALUES('ELCBIGCCEA',	'EBIOIGCC',	2015,'ELC',0.253,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCBIGCCEA',	'EBIOIGCC',	2020,'ELC',0.253,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCBIGCCEA',	'EBIOIGCC',	2025,'ELC',0.253,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCBIGCCEA',	'EBIOIGCC',	2030,'ELC',0.253,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCBIGCCEA',	'EBIOIGCC',	2035,'ELC',0.253,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCBIGCCEA',	'EBIOIGCC',	2040,'ELC',0.253,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCBIGCCEA',	'EBIOIGCC',	2045,'ELC',0.253,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCBIGCCEA',	'EBIOIGCC',	2050,'ELC',0.253,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('ELCBIOSTM',	'EBIOSTMR',	2005,'ELC',0.219,'# MARKAL 2014 v1.1');

-- Geothermal, future only
INSERT INTO "Efficiency" VALUES('ELCGEO',	'EGEOBCFS',	2015,'ELC',0.351,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCGEO',	'EGEOBCFS',	2020,'ELC',0.351,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCGEO',	'EGEOBCFS',	2025,'ELC',0.351,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCGEO',	'EGEOBCFS',	2030,'ELC',0.351,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCGEO',	'EGEOBCFS',	2035,'ELC',0.351,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCGEO',	'EGEOBCFS',	2040,'ELC',0.351,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCGEO',	'EGEOBCFS',	2045,'ELC',0.351,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('ELCGEO',	'EGEOBCFS',	2050,'ELC',0.351,'# MARKAL 2014 v1.1');

-- INSERT INTO "Efficiency" VALUES('ELCGEO',	'EGEOR',	2015,'ELC',0.162,'# From Samaneh NUSTD');

-- Solar, both existing and future
INSERT INTO "Efficiency" VALUES('SOL',	'ESOLPVCEN',	2015,'ELC',1.000,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('SOL',	'ESOLSTCEN',	2015,'ELC',1.000,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('SOL',	'ESOLPVCEN',	2020,'ELC',1.000,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('SOL',	'ESOLSTCEN',	2020,'ELC',1.000,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('SOL',	'ESOLPVCEN',	2025,'ELC',1.000,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('SOL',	'ESOLSTCEN',	2025,'ELC',1.000,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('SOL',	'ESOLPVCEN',	2030,'ELC',1.000,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('SOL',	'ESOLSTCEN',	2030,'ELC',1.000,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('SOL',	'ESOLPVCEN',	2035,'ELC',1.000,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('SOL',	'ESOLSTCEN',	2035,'ELC',1.000,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('SOL',	'ESOLPVCEN',	2040,'ELC',1.000,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('SOL',	'ESOLSTCEN',	2040,'ELC',1.000,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('SOL',	'ESOLPVCEN',	2045,'ELC',1.000,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('SOL',	'ESOLSTCEN',	2045,'ELC',1.000,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('SOL',	'ESOLPVCEN',	2050,'ELC',1.000,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('SOL',	'ESOLSTCEN',	2050,'ELC',1.000,'# MARKAL 2014 v1.1');

-- INSERT INTO "Efficiency" VALUES('SOL',	'ESOLTHR',		2015,'ELC',0.328,'# From Samaneh NUSTD');

INSERT INTO "Efficiency" VALUES('SOL',	'ESOLPVR',		2005,'ELC',0.351,'# MARKAL 2014 v1.1'); 

-- Wind, future only
-- INSERT INTO "Efficiency" VALUES('WND',	'EWNDR',	2015,'ELC',0.338,'# From Samaneh NUSTD');

INSERT INTO "Efficiency" VALUES('WND',	'EWNDON',	2015,'ELC',1.000,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('WND',	'EWNDOFS',	2015,'ELC',1.000,'# MARKAL 2014 v1.1');
-- INSERT INTO "Efficiency" VALUES('WND',	'EWNDOFD',	2015,'ELC',1.000,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('WND',	'EWNDON',	2020,'ELC',1.000,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('WND',	'EWNDOFS',	2020,'ELC',1.000,'# MARKAL 2014 v1.1');
-- INSERT INTO "Efficiency" VALUES('WND',	'EWNDOFD',	2020,'ELC',1.000,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('WND',	'EWNDON',	2025,'ELC',1.000,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('WND',	'EWNDOFS',	2025,'ELC',1.000,'# MARKAL 2014 v1.1');
-- INSERT INTO "Efficiency" VALUES('WND',	'EWNDOFD',	2025,'ELC',1.000,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('WND',	'EWNDON',	2030,'ELC',1.000,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('WND',	'EWNDOFS',	2030,'ELC',1.000,'# MARKAL 2014 v1.1');
-- INSERT INTO "Efficiency" VALUES('WND',	'EWNDOFD',	2030,'ELC',1.000,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('WND',	'EWNDON',	2035,'ELC',1.000,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('WND',	'EWNDOFS',	2035,'ELC',1.000,'# MARKAL 2014 v1.1');
-- INSERT INTO "Efficiency" VALUES('WND',	'EWNDOFD',	2035,'ELC',1.000,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('WND',	'EWNDON',	2040,'ELC',1.000,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('WND',	'EWNDOFS',	2040,'ELC',1.000,'# MARKAL 2014 v1.1');
-- INSERT INTO "Efficiency" VALUES('WND',	'EWNDOFD',	2040,'ELC',1.000,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('WND',	'EWNDON',	2045,'ELC',1.000,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('WND',	'EWNDOFS',	2045,'ELC',1.000,'# MARKAL 2014 v1.1');
-- INSERT INTO "Efficiency" VALUES('WND',	'EWNDOFD',	2045,'ELC',1.000,'# MARKAL 2014 v1.1');

INSERT INTO "Efficiency" VALUES('WND',	'EWNDON',	2050,'ELC',1.000,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('WND',	'EWNDOFS',	2050,'ELC',1.000,'# MARKAL 2014 v1.1');
-- INSERT INTO "Efficiency" VALUES('WND',	'EWNDOFD',	2050,'ELC',1.000,'# MARKAL 2014 v1.1');

-- Hydro, existing only
INSERT INTO "Efficiency" VALUES('ELCHYD',	'EHYDCONR',		2005,'ELC',0.351,'# MARKAL 2014 v1.1');

-- Pumped hydro, existing only
INSERT INTO "Efficiency" VALUES('ELC',		'EHYDREVR',		2005,'ELC',0.351,'# MARKAL 2014 v1.1');

-- MSW, existing only
-- INSERT INTO "Efficiency" VALUES('ELCMSWEA',	'EMSWSTMR',		1995,'ELC',0.328,'# From Samaneh NUSTD');
-- INSERT INTO "Efficiency" VALUES('ELCMSWEA',	'EMSWSTMR',		2015,'ELC',0.328,'# From Samaneh NUSTD');

-- LFG, both existing and future
INSERT INTO "Efficiency" VALUES('LFGICEEA', 'ELFGICER',     2005,'ELC',0.360,'# MARKAL 2014 v1.1');
INSERT INTO "Efficiency" VALUES('LFGGTREA', 'ELFGGTR',      2005,'ELC',0.300,'# MARKAL 2014 v1.1');

-- Gulf Stream energy
INSERT INTO "Efficiency" VALUES('ELCHYD',   'EHYDGS',       2015,'ELC',0.351, '');
INSERT INTO "Efficiency" VALUES('ELCHYD',   'EHYDGS',       2020,'ELC',0.351, '');
INSERT INTO "Efficiency" VALUES('ELCHYD',   'EHYDGS',       2025,'ELC',0.351, '');
INSERT INTO "Efficiency" VALUES('ELCHYD',   'EHYDGS',       2030,'ELC',0.351, '');
INSERT INTO "Efficiency" VALUES('ELCHYD',   'EHYDGS',       2035,'ELC',0.351, '');
INSERT INTO "Efficiency" VALUES('ELCHYD',   'EHYDGS',       2040,'ELC',0.351, '');
INSERT INTO "Efficiency" VALUES('ELCHYD',   'EHYDGS',       2045,'ELC',0.351, '');
INSERT INTO "Efficiency" VALUES('ELCHYD',   'EHYDGS',       2050,'ELC',0.351, '');

-- Dummy electricity to demand tech
INSERT INTO "Efficiency" VALUES('ELC',		'ELC2DMD',		2015,'ELCDMD',1.000,'#');
INSERT INTO "Efficiency" VALUES('ELC',		'ELC2DMD',		2020,'ELCDMD',1.000,'#');
INSERT INTO "Efficiency" VALUES('ELC',		'ELC2DMD',		2025,'ELCDMD',1.000,'#');
INSERT INTO "Efficiency" VALUES('ELC',		'ELC2DMD',		2030,'ELCDMD',1.000,'#');
INSERT INTO "Efficiency" VALUES('ELC',		'ELC2DMD',		2035,'ELCDMD',1.000,'#');
INSERT INTO "Efficiency" VALUES('ELC',		'ELC2DMD',		2040,'ELCDMD',1.000,'#');
INSERT INTO "Efficiency" VALUES('ELC',		'ELC2DMD',		2045,'ELCDMD',1.000,'#');
INSERT INTO "Efficiency" VALUES('ELC',		'ELC2DMD',		2050,'ELCDMD',1.000,'#');

-- Emission control technologies
-- For Existing bituminous coal-fired steam turbine, note here the new NUSTD naming convention was used
INSERT INTO "Efficiency" VALUES('COALSTM_R_B', 'E_BLND_BITSUBLIG_COALSTM_R', 2015,'COALSTM',1,'#'); -- 'COALSTM' was MARKAL name, NUSTD name is 'COALSTM_R' 
INSERT INTO "Efficiency" VALUES('COALSTM_R_B', 'E_BLND_BITSUBLIG_COALSTM_R', 2020,'COALSTM',1,'#'); -- 'COALSTM' was MARKAL name, NUSTD name is 'COALSTM_R'
INSERT INTO "Efficiency" VALUES('COALSTM_R_B', 'E_BLND_BITSUBLIG_COALSTM_R', 2025,'COALSTM',1,'#'); -- 'COALSTM' was MARKAL name, NUSTD name is 'COALSTM_R'
INSERT INTO "Efficiency" VALUES('COALSTM_R_B', 'E_BLND_BITSUBLIG_COALSTM_R', 2030,'COALSTM',1,'#'); -- 'COALSTM' was MARKAL name, NUSTD name is 'COALSTM_R'
INSERT INTO "Efficiency" VALUES('COALSTM_R_B', 'E_BLND_BITSUBLIG_COALSTM_R', 2035,'COALSTM',1,'#'); -- 'COALSTM' was MARKAL name, NUSTD name is 'COALSTM_R'
INSERT INTO "Efficiency" VALUES('COALSTM_R_B', 'E_BLND_BITSUBLIG_COALSTM_R', 2040,'COALSTM',1,'#'); -- 'COALSTM' was MARKAL name, NUSTD name is 'COALSTM_R'
INSERT INTO "Efficiency" VALUES('COALSTM_R_B', 'E_BLND_BITSUBLIG_COALSTM_R', 2045,'COALSTM',1,'#'); -- 'COALSTM' was MARKAL name, NUSTD name is 'COALSTM_R'
INSERT INTO "Efficiency" VALUES('COALSTM_R_B', 'E_BLND_BITSUBLIG_COALSTM_R', 2050,'COALSTM',1,'#'); -- 'COALSTM' was MARKAL name, NUSTD name is 'COALSTM_R'

INSERT INTO "Efficiency" VALUES('COAB_R', 'E_BLND_BIT_COALSTM_R', 2015,'COALSTM_R_B',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R', 'E_BLND_BIT_COALSTM_R', 2020,'COALSTM_R_B',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R', 'E_BLND_BIT_COALSTM_R', 2025,'COALSTM_R_B',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R', 'E_BLND_BIT_COALSTM_R', 2030,'COALSTM_R_B',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R', 'E_BLND_BIT_COALSTM_R', 2035,'COALSTM_R_B',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R', 'E_BLND_BIT_COALSTM_R', 2040,'COALSTM_R_B',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R', 'E_BLND_BIT_COALSTM_R', 2045,'COALSTM_R_B',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R', 'E_BLND_BIT_COALSTM_R', 2050,'COALSTM_R_B',1,'');

INSERT INTO "Efficiency" VALUES('COAB_R_LNB',   'E_LNBSNCR_COAB_R',2010,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT','E_LNBSNCR_COAB_R',2010,'COAB_R',1,'');

INSERT INTO "Efficiency" VALUES('COAB_R_LNB',           'E_LNBSNCR_COAB_N',     2015,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',           'E_LNBSNCR_COAB_N',     2020,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',           'E_LNBSNCR_COAB_N',     2025,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',           'E_LNBSNCR_COAB_N',     2030,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',           'E_LNBSNCR_COAB_N',     2035,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',           'E_LNBSNCR_COAB_N',     2040,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',           'E_LNBSNCR_COAB_N',     2045,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',           'E_LNBSNCR_COAB_N',     2050,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNBSNCR_COAB_N',     2015,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNBSNCR_COAB_N',     2020,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNBSNCR_COAB_N',     2025,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNBSNCR_COAB_N',     2030,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNBSNCR_COAB_N',     2035,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNBSNCR_COAB_N',     2040,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNBSNCR_COAB_N',     2045,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNBSNCR_COAB_N',     2050,'COAB_R',1,'');

-- Existing LNB + SCR
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',              'E_LNBSCR_COAB_R',     2010,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNBSCR_COAB_R',     2010,'COAB_R',1,'');

-- Future LNB + SCR
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',              'E_LNBSCR_COAB_N',     2015,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',              'E_LNBSCR_COAB_N',     2020,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',              'E_LNBSCR_COAB_N',     2025,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',              'E_LNBSCR_COAB_N',     2030,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',              'E_LNBSCR_COAB_N',     2035,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',              'E_LNBSCR_COAB_N',     2040,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',              'E_LNBSCR_COAB_N',     2045,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',              'E_LNBSCR_COAB_N',     2050,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNBSCR_COAB_N',     2015,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNBSCR_COAB_N',     2020,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNBSCR_COAB_N',     2025,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNBSCR_COAB_N',     2030,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNBSCR_COAB_N',     2035,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNBSCR_COAB_N',     2040,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNBSCR_COAB_N',     2045,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNBSCR_COAB_N',     2050,'COAB_R',1,'');

-- NOx SCR/SNCR control pass through
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_PTNOXSCR_COAB',      2015,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_PTNOXSCR_COAB',      2020,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_PTNOXSCR_COAB',      2025,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_PTNOXSCR_COAB',      2030,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_PTNOXSCR_COAB',      2035,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_PTNOXSCR_COAB',      2040,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_PTNOXSCR_COAB',      2045,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_PTNOXSCR_COAB',      2050,'COAB_R',1,'');

-- Existing SNCR
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_SNCR_COAB_R',        2010,'COAB_R',1,'');

-- Future SNCR
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_SNCR_COAB_N',        2015,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_SNCR_COAB_N',        2020,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_SNCR_COAB_N',        2025,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_SNCR_COAB_N',        2030,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_SNCR_COAB_N',        2035,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_SNCR_COAB_N',        2040,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_SNCR_COAB_N',        2045,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_SNCR_COAB_N',        2050,'COAB_R',1,'');

-- Existing SCR
-- INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_SCR_COAB_R',        2010,'COAB_R',1,'');

-- Future SCR
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_SCR_COAB_N',        2015,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_SCR_COAB_N',        2020,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_SCR_COAB_N',        2025,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_SCR_COAB_N',        2030,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_SCR_COAB_N',        2035,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_SCR_COAB_N',        2040,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_SCR_COAB_N',        2045,'COAB_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_SCR_PT',           'E_SCR_COAB_N',        2050,'COAB_R',1,'');

-- Pass through LNB
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_PTNOXLNB_COAB',     2015,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_PTNOXLNB_COAB',     2020,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_PTNOXLNB_COAB',     2025,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_PTNOXLNB_COAB',     2030,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_PTNOXLNB_COAB',     2035,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_PTNOXLNB_COAB',     2040,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_PTNOXLNB_COAB',     2045,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_PTNOXLNB_COAB',     2050,'COAB_R_SCR_PT',1,'');

-- Existing LNB
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',              'E_LNB_COAB_R',     2010,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNB_COAB_R',     2010,'COAB_R_SCR_PT',1,'');

-- Future LNB
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',              'E_LNB_COAB_N',     2015,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',              'E_LNB_COAB_N',     2020,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',              'E_LNB_COAB_N',     2025,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',              'E_LNB_COAB_N',     2030,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',              'E_LNB_COAB_N',     2035,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',              'E_LNB_COAB_N',     2040,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',              'E_LNB_COAB_N',     2045,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB',              'E_LNB_COAB_N',     2050,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNB_COAB_N',     2015,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNB_COAB_N',     2020,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNB_COAB_N',     2025,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNB_COAB_N',     2030,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNB_COAB_N',     2035,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNB_COAB_N',     2040,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNB_COAB_N',     2045,'COAB_R_SCR_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_LNB_PT',           'E_LNB_COAB_N',     2050,'COAB_R_SCR_PT',1,'');

-- CO2 control for existing coal
INSERT INTO "Efficiency" VALUES('COAB_R_CC',           'E_CCR_COAB',     2015,'COAB_R_LNB',0.65,'');
INSERT INTO "Efficiency" VALUES('COAB_R_CC',           'E_CCR_COAB',     2020,'COAB_R_LNB',0.65,'');
INSERT INTO "Efficiency" VALUES('COAB_R_CC',           'E_CCR_COAB',     2025,'COAB_R_LNB',0.65,'');
INSERT INTO "Efficiency" VALUES('COAB_R_CC',           'E_CCR_COAB',     2030,'COAB_R_LNB',0.65,'');
INSERT INTO "Efficiency" VALUES('COAB_R_CC',           'E_CCR_COAB',     2035,'COAB_R_LNB',0.65,'');
INSERT INTO "Efficiency" VALUES('COAB_R_CC',           'E_CCR_COAB',     2040,'COAB_R_LNB',0.65,'');
INSERT INTO "Efficiency" VALUES('COAB_R_CC',           'E_CCR_COAB',     2045,'COAB_R_LNB',0.65,'');
INSERT INTO "Efficiency" VALUES('COAB_R_CC',           'E_CCR_COAB',     2050,'COAB_R_LNB',0.65,'');

-- CO2 control pass through
INSERT INTO "Efficiency" VALUES('COAB_R_CC',           'E_PTCO2_COAB',     2015,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_CC',           'E_PTCO2_COAB',     2020,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_CC',           'E_PTCO2_COAB',     2025,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_CC',           'E_PTCO2_COAB',     2030,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_CC',           'E_PTCO2_COAB',     2035,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_CC',           'E_PTCO2_COAB',     2040,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_CC',           'E_PTCO2_COAB',     2045,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COAB_R_CC',           'E_PTCO2_COAB',     2050,'COAB_R_LNB_PT',1,'');

-- Existing SO2 for high sulfur coal
-- INSERT INTO "Efficiency" VALUES('COABH_R',           'E_FGD_COABH_R',     2010,'COAB_R_CC',1,'');

-- Future SO2 for high sulfur coal
INSERT INTO "Efficiency" VALUES('COABH_R',           'E_FGD_COABH_N',     2015,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABH_R',           'E_FGD_COABH_N',     2020,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABH_R',           'E_FGD_COABH_N',     2025,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABH_R',           'E_FGD_COABH_N',     2030,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABH_R',           'E_FGD_COABH_N',     2035,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABH_R',           'E_FGD_COABH_N',     2040,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABH_R',           'E_FGD_COABH_N',     2045,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABH_R',           'E_FGD_COABH_N',     2050,'COAB_R_CC',1,'');

-- Existing SO2 for median sulfur coal
INSERT INTO "Efficiency" VALUES('COABM_R',           'E_FGD_COABM_R',     2010,'COAB_R_CC',1,'');

-- Future SO2 for median sulfur bit coal
INSERT INTO "Efficiency" VALUES('COABM_R',           'E_FGD_COABM_N',     2015,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABM_R',           'E_FGD_COABM_N',     2020,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABM_R',           'E_FGD_COABM_N',     2025,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABM_R',           'E_FGD_COABM_N',     2030,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABM_R',           'E_FGD_COABM_N',     2035,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABM_R',           'E_FGD_COABM_N',     2040,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABM_R',           'E_FGD_COABM_N',     2045,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABM_R',           'E_FGD_COABM_N',     2050,'COAB_R_CC',1,'');

-- Existing SO2 for low sulfur bit coal
INSERT INTO "Efficiency" VALUES('COABL_R',           'E_FGD_COABL_R',     2010,'COAB_R_CC',1,'');

-- Future SO2 for low sulfur bit coal
INSERT INTO "Efficiency" VALUES('COABL_R',           'E_FGD_COABL_N',     2015,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABL_R',           'E_FGD_COABL_N',     2020,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABL_R',           'E_FGD_COABL_N',     2025,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABL_R',           'E_FGD_COABL_N',     2030,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABL_R',           'E_FGD_COABL_N',     2035,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABL_R',           'E_FGD_COABL_N',     2040,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABL_R',           'E_FGD_COABL_N',     2045,'COAB_R_CC',1,'');
INSERT INTO "Efficiency" VALUES('COABL_R',           'E_FGD_COABL_N',     2050,'COAB_R_CC',1,'');

-- SO2 and CCR pass through for high sulfur bit coal
INSERT INTO "Efficiency" VALUES('COABH_R',           'E_PTSO2_COABH',     2015,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABH_R',           'E_PTSO2_COABH',     2020,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABH_R',           'E_PTSO2_COABH',     2025,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABH_R',           'E_PTSO2_COABH',     2030,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABH_R',           'E_PTSO2_COABH',     2035,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABH_R',           'E_PTSO2_COABH',     2040,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABH_R',           'E_PTSO2_COABH',     2045,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABH_R',           'E_PTSO2_COABH',     2050,'COAB_R_LNB_PT',1,'');

-- SO2 and CCR pass through for median sulfur bit coal
INSERT INTO "Efficiency" VALUES('COABM_R',           'E_PTSO2_COABM',     2015,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABM_R',           'E_PTSO2_COABM',     2020,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABM_R',           'E_PTSO2_COABM',     2025,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABM_R',           'E_PTSO2_COABM',     2030,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABM_R',           'E_PTSO2_COABM',     2035,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABM_R',           'E_PTSO2_COABM',     2040,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABM_R',           'E_PTSO2_COABM',     2045,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABM_R',           'E_PTSO2_COABM',     2050,'COAB_R_LNB_PT',1,'');

-- SO2 and CCR pass through for median sulfur bit coal
INSERT INTO "Efficiency" VALUES('COABL_R',           'E_PTSO2_COABL',     2015,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABL_R',           'E_PTSO2_COABL',     2020,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABL_R',           'E_PTSO2_COABL',     2025,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABL_R',           'E_PTSO2_COABL',     2030,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABL_R',           'E_PTSO2_COABL',     2035,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABL_R',           'E_PTSO2_COABL',     2040,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABL_R',           'E_PTSO2_COABL',     2045,'COAB_R_LNB_PT',1,'');
INSERT INTO "Efficiency" VALUES('COABL_R',           'E_PTSO2_COABL',     2050,'COAB_R_LNB_PT',1,'');

-- Emission accounting for sub coal
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2015,'COABH_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2020,'COABH_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2025,'COABH_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2030,'COABH_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2035,'COABH_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2040,'COABH_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2045,'COABH_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2050,'COABH_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2015,'COABM_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2020,'COABM_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2025,'COABM_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2030,'COABM_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2035,'COABM_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2040,'COABM_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2045,'COABM_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2050,'COABM_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2015,'COABL_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2020,'COABL_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2025,'COABL_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2030,'COABL_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2035,'COABL_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2040,'COABL_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2045,'COABL_R',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2050,'COABL_R',1,'');

INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2015,'COABH_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2020,'COABH_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2025,'COABH_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2030,'COABH_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2035,'COABH_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2040,'COABH_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2045,'COABH_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2050,'COABH_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2015,'COABM_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2020,'COABM_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2025,'COABM_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2030,'COABM_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2035,'COABM_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2040,'COABM_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2045,'COABM_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2050,'COABM_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2015,'COABL_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2020,'COABL_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2025,'COABL_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2030,'COABL_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2035,'COABL_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2040,'COABL_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2045,'COABL_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2050,'COABL_N',1,'');

INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2015,'COABH_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2020,'COABH_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2025,'COABH_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2030,'COABH_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2035,'COABH_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2040,'COABH_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2045,'COABH_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2050,'COABH_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2015,'COABM_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2020,'COABM_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2025,'COABM_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2030,'COABM_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2035,'COABM_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2040,'COABM_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2045,'COABM_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2050,'COABM_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2015,'COABL_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2020,'COABL_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2025,'COABL_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2030,'COABL_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2035,'COABL_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2040,'COABL_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2045,'COABL_IGCC_N',1,'');
INSERT INTO "Efficiency" VALUES('COAB_EA',           'E_EA_COAB',     2050,'COABL_IGCC_N',1,'');

-- IGCC CC
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_CC',           'E_CCR_COALIGCC_N',     2015,'COALIGCC',0.8,''); -- 'COALIGCC' in NUSTD: 'COALIGCC_N' 
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_CC',           'E_CCR_COALIGCC_N',     2020,'COALIGCC',0.8,''); -- 'COALIGCC' in NUSTD: 'COALIGCC_N'
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_CC',           'E_CCR_COALIGCC_N',     2025,'COALIGCC',0.8,''); -- 'COALIGCC' in NUSTD: 'COALIGCC_N'
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_CC',           'E_CCR_COALIGCC_N',     2030,'COALIGCC',0.8,''); -- 'COALIGCC' in NUSTD: 'COALIGCC_N'
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_CC',           'E_CCR_COALIGCC_N',     2035,'COALIGCC',0.8,''); -- 'COALIGCC' in NUSTD: 'COALIGCC_N'
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_CC',           'E_CCR_COALIGCC_N',     2040,'COALIGCC',0.8,''); -- 'COALIGCC' in NUSTD: 'COALIGCC_N'
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_CC',           'E_CCR_COALIGCC_N',     2045,'COALIGCC',0.8,''); -- 'COALIGCC' in NUSTD: 'COALIGCC_N'
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_CC',           'E_CCR_COALIGCC_N',     2050,'COALIGCC',0.8,''); -- 'COALIGCC' in NUSTD: 'COALIGCC_N'

-- Blending tech to collect BIT/SUB/LIG coal for new coal IGCC plant
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2015,'COALIGCC',1,''); -- 'COALIGCC' in NUSTD: 'COALIGCC_N' 
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2020,'COALIGCC',1,''); -- 'COALIGCC' in NUSTD: 'COALIGCC_N'
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2025,'COALIGCC',1,''); -- 'COALIGCC' in NUSTD: 'COALIGCC_N'
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2030,'COALIGCC',1,''); -- 'COALIGCC' in NUSTD: 'COALIGCC_N'
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2035,'COALIGCC',1,''); -- 'COALIGCC' in NUSTD: 'COALIGCC_N'
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2040,'COALIGCC',1,''); -- 'COALIGCC' in NUSTD: 'COALIGCC_N'
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2045,'COALIGCC',1,''); -- 'COALIGCC' in NUSTD: 'COALIGCC_N'
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2050,'COALIGCC',1,''); -- 'COALIGCC' in NUSTD: 'COALIGCC_N'

   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2015,'COALIGCC_N_CC',1,''); 
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2020,'COALIGCC_N_CC',1,'');
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2025,'COALIGCC_N_CC',1,'');
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2030,'COALIGCC_N_CC',1,'');
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2035,'COALIGCC_N_CC',1,'');
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2040,'COALIGCC_N_CC',1,'');
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2045,'COALIGCC_N_CC',1,'');
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2050,'COALIGCC_N_CC',1,'');

   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2015,'COALIGCCCC',1,''); -- 'COALIGCCCC' in NUSTD: 'COALIGCC_CCS_N' 
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2020,'COALIGCCCC',1,''); -- 'COALIGCCCC' in NUSTD: 'COALIGCC_CCS_N'
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2025,'COALIGCCCC',1,''); -- 'COALIGCCCC' in NUSTD: 'COALIGCC_CCS_N'
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2030,'COALIGCCCC',1,''); -- 'COALIGCCCC' in NUSTD: 'COALIGCC_CCS_N'
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2035,'COALIGCCCC',1,''); -- 'COALIGCCCC' in NUSTD: 'COALIGCC_CCS_N'
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2040,'COALIGCCCC',1,''); -- 'COALIGCCCC' in NUSTD: 'COALIGCC_CCS_N'
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2045,'COALIGCCCC',1,''); -- 'COALIGCCCC' in NUSTD: 'COALIGCC_CCS_N'
   INSERT INTO "Efficiency" VALUES('COALIGCC_N_B',           'E_BLND_BITSUBLIG_COALIGCC_N',     2050,'COALIGCCCC',1,''); -- 'COALIGCCCC' in NUSTD: 'COALIGCC_CCS_N'

-- Blending tech to collect h/m/l sulfur bit coal for new coal IGCC plant
INSERT INTO "Efficiency" VALUES('COABH_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2015,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABH_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2020,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABH_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2025,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABH_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2030,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABH_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2035,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABH_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2040,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABH_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2045,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABH_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2050,'COALIGCC_N_B',1,'');

INSERT INTO "Efficiency" VALUES('COABM_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2015,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABM_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2020,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABM_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2025,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABM_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2030,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABM_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2035,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABM_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2040,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABM_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2045,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABM_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2050,'COALIGCC_N_B',1,'');

INSERT INTO "Efficiency" VALUES('COABL_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2015,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABL_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2020,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABL_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2025,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABL_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2030,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABL_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2035,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABL_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2040,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABL_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2045,'COALIGCC_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABL_IGCC_N',           'E_BLND_BITHML_COALIGCC_N',     2050,'COALIGCC_N_B',1,'');

-- co2 capture retrofit tech before new coal steam plant
INSERT INTO "Efficiency" VALUES('COALSTM_N_CC',           'E_CCR_COALSTM_N',     2015,'COALSTMCC',0.7,''); -- 'COALSTMCC' in NUSTD: 'COALSTM_N' 
INSERT INTO "Efficiency" VALUES('COALSTM_N_CC',           'E_CCR_COALSTM_N',     2020,'COALSTMCC',0.7,''); -- 'COALSTMCC' in NUSTD: 'COALSTM_N'
INSERT INTO "Efficiency" VALUES('COALSTM_N_CC',           'E_CCR_COALSTM_N',     2025,'COALSTMCC',0.7,''); -- 'COALSTMCC' in NUSTD: 'COALSTM_N'
INSERT INTO "Efficiency" VALUES('COALSTM_N_CC',           'E_CCR_COALSTM_N',     2030,'COALSTMCC',0.7,''); -- 'COALSTMCC' in NUSTD: 'COALSTM_N'
INSERT INTO "Efficiency" VALUES('COALSTM_N_CC',           'E_CCR_COALSTM_N',     2035,'COALSTMCC',0.7,''); -- 'COALSTMCC' in NUSTD: 'COALSTM_N'
INSERT INTO "Efficiency" VALUES('COALSTM_N_CC',           'E_CCR_COALSTM_N',     2040,'COALSTMCC',0.7,''); -- 'COALSTMCC' in NUSTD: 'COALSTM_N'
INSERT INTO "Efficiency" VALUES('COALSTM_N_CC',           'E_CCR_COALSTM_N',     2045,'COALSTMCC',0.7,''); -- 'COALSTMCC' in NUSTD: 'COALSTM_N'
INSERT INTO "Efficiency" VALUES('COALSTM_N_CC',           'E_CCR_COALSTM_N',     2050,'COALSTMCC',0.7,''); -- 'COALSTMCC' in NUSTD: 'COALSTM_N'

-- Blending tech to collect BIT/SUB/LIG coal for new coal steam plant
INSERT INTO "Efficiency" VALUES('COALSTM_N_B',           'E_BLND_BITSUBLIG_COALSTM_N',     2015,'COALSTMCC',1,''); -- 'COALSTMCC' in NUSTD: 'COALSTM_N' 
INSERT INTO "Efficiency" VALUES('COALSTM_N_B',           'E_BLND_BITSUBLIG_COALSTM_N',     2020,'COALSTMCC',1,''); -- 'COALSTMCC' in NUSTD: 'COALSTM_N'
INSERT INTO "Efficiency" VALUES('COALSTM_N_B',           'E_BLND_BITSUBLIG_COALSTM_N',     2025,'COALSTMCC',1,''); -- 'COALSTMCC' in NUSTD: 'COALSTM_N'
INSERT INTO "Efficiency" VALUES('COALSTM_N_B',           'E_BLND_BITSUBLIG_COALSTM_N',     2030,'COALSTMCC',1,''); -- 'COALSTMCC' in NUSTD: 'COALSTM_N'
INSERT INTO "Efficiency" VALUES('COALSTM_N_B',           'E_BLND_BITSUBLIG_COALSTM_N',     2035,'COALSTMCC',1,''); -- 'COALSTMCC' in NUSTD: 'COALSTM_N'
INSERT INTO "Efficiency" VALUES('COALSTM_N_B',           'E_BLND_BITSUBLIG_COALSTM_N',     2040,'COALSTMCC',1,''); -- 'COALSTMCC' in NUSTD: 'COALSTM_N'
INSERT INTO "Efficiency" VALUES('COALSTM_N_B',           'E_BLND_BITSUBLIG_COALSTM_N',     2045,'COALSTMCC',1,''); -- 'COALSTMCC' in NUSTD: 'COALSTM_N'
INSERT INTO "Efficiency" VALUES('COALSTM_N_B',           'E_BLND_BITSUBLIG_COALSTM_N',     2050,'COALSTMCC',1,''); -- 'COALSTMCC' in NUSTD: 'COALSTM_N'

INSERT INTO "Efficiency" VALUES('COALSTM_N_B',           'E_BLND_BITSUBLIG_COALSTM_N',     2015,'COALSTM_N_CC',1,'');
INSERT INTO "Efficiency" VALUES('COALSTM_N_B',           'E_BLND_BITSUBLIG_COALSTM_N',     2020,'COALSTM_N_CC',1,'');
INSERT INTO "Efficiency" VALUES('COALSTM_N_B',           'E_BLND_BITSUBLIG_COALSTM_N',     2025,'COALSTM_N_CC',1,'');
INSERT INTO "Efficiency" VALUES('COALSTM_N_B',           'E_BLND_BITSUBLIG_COALSTM_N',     2030,'COALSTM_N_CC',1,'');
INSERT INTO "Efficiency" VALUES('COALSTM_N_B',           'E_BLND_BITSUBLIG_COALSTM_N',     2035,'COALSTM_N_CC',1,'');
INSERT INTO "Efficiency" VALUES('COALSTM_N_B',           'E_BLND_BITSUBLIG_COALSTM_N',     2040,'COALSTM_N_CC',1,'');
INSERT INTO "Efficiency" VALUES('COALSTM_N_B',           'E_BLND_BITSUBLIG_COALSTM_N',     2045,'COALSTM_N_CC',1,'');
INSERT INTO "Efficiency" VALUES('COALSTM_N_B',           'E_BLND_BITSUBLIG_COALSTM_N',     2050,'COALSTM_N_CC',1,'');

-- Blending tech to collect H/M/L sulfur bit coal for new coal steam plant
INSERT INTO "Efficiency" VALUES('COABH_N',           'E_BLND_BITHML_COALSTM_N',     2015,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABH_N',           'E_BLND_BITHML_COALSTM_N',     2020,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABH_N',           'E_BLND_BITHML_COALSTM_N',     2025,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABH_N',           'E_BLND_BITHML_COALSTM_N',     2030,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABH_N',           'E_BLND_BITHML_COALSTM_N',     2035,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABH_N',           'E_BLND_BITHML_COALSTM_N',     2040,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABH_N',           'E_BLND_BITHML_COALSTM_N',     2045,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABH_N',           'E_BLND_BITHML_COALSTM_N',     2050,'COALSTM_N_B',1,'');

INSERT INTO "Efficiency" VALUES('COABM_N',           'E_BLND_BITHML_COALSTM_N',     2015,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABM_N',           'E_BLND_BITHML_COALSTM_N',     2020,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABM_N',           'E_BLND_BITHML_COALSTM_N',     2025,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABM_N',           'E_BLND_BITHML_COALSTM_N',     2030,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABM_N',           'E_BLND_BITHML_COALSTM_N',     2035,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABM_N',           'E_BLND_BITHML_COALSTM_N',     2040,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABM_N',           'E_BLND_BITHML_COALSTM_N',     2045,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABM_N',           'E_BLND_BITHML_COALSTM_N',     2050,'COALSTM_N_B',1,'');

INSERT INTO "Efficiency" VALUES('COABL_N',           'E_BLND_BITHML_COALSTM_N',     2015,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABL_N',           'E_BLND_BITHML_COALSTM_N',     2020,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABL_N',           'E_BLND_BITHML_COALSTM_N',     2025,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABL_N',           'E_BLND_BITHML_COALSTM_N',     2030,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABL_N',           'E_BLND_BITHML_COALSTM_N',     2035,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABL_N',           'E_BLND_BITHML_COALSTM_N',     2040,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABL_N',           'E_BLND_BITHML_COALSTM_N',     2045,'COALSTM_N_B',1,'');
INSERT INTO "Efficiency" VALUES('COABL_N',           'E_BLND_BITHML_COALSTM_N',     2050,'COALSTM_N_B',1,'');

---------------
-- NUSTD importing tech
INSERT INTO "Efficiency" VALUES('ethos','IMPELCCOAB',  2015,'COAB_EA',        1.00,'');

-------------------------------------------------
CREATE TABLE CapacityFactorProcess (
   season_name text,
   time_of_day_name text,
   tech text,
   vintage integer,
   cf_process real check (cf_process >=0 AND cf_process <=1),
   cf_process_notes text,
   PRIMARY KEY(season_name, time_of_day_name, tech, vintage),
   FOREIGN KEY(season_name) REFERENCES time_season(t_season),
   FOREIGN KEY(time_of_day_name) REFERENCES time_of_day(t_day),
   FOREIGN KEY(tech) REFERENCES technologies(tech) );

INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod01',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod01',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod01',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod01',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod01',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod01',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod01',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod01',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod02',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod02',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod02',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod02',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod02',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod02',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod02',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod02',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod03',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod03',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod03',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod03',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod03',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod03',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod03',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod03',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod04',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod04',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod04',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod04',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod04',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod04',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod04',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod04',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod05',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod05',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod05',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod05',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod05',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod05',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod05',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod05',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod06',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod06',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod06',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod06',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod06',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod06',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod06',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod06',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod07',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod07',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod07',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod07',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod07',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod07',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod07',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod07',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod08',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod08',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod08',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod08',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod08',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod08',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod08',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod08',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod09',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod09',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod09',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod09',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod09',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod09',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod09',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod09',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod10',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod10',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod10',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod10',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod10',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod10',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod10',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod10',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod11',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod11',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod11',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod11',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod11',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod11',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod11',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod11',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod12',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod12',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod12',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod12',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod12',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod12',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod12',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod12',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod13',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod13',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod13',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod13',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod13',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod13',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod13',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod13',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod14',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod14',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod14',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod14',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod14',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod14',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod14',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod14',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod15',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod15',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod15',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod15',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod15',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod15',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod15',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod15',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod16',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod16',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod16',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod16',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod16',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod16',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod16',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod16',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod17',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod17',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod17',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod17',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod17',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod17',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod17',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod17',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod18',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod18',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod18',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod18',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod18',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod18',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod18',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod18',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod19',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod19',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod19',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod19',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod19',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod19',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod19',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod19',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod20',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod20',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod20',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod20',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod20',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod20',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod20',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod20',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod21',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod21',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod21',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod21',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod21',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod21',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod21',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod21',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod22',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod22',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod22',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod22',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod22',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod22',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod22',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod22',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod23',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod23',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod23',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod23',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod23',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod23',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod23',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod23',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod24',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod24',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod24',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod24',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod24',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod24',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod24',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s001', 'tod24',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod01',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod01',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod01',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod01',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod01',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod01',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod01',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod01',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod02',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod02',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod02',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod02',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod02',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod02',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod02',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod02',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod03',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod03',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod03',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod03',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod03',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod03',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod03',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod03',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod04',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod04',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod04',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod04',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod04',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod04',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod04',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod04',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod05',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod05',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod05',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod05',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod05',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod05',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod05',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod05',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod06',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod06',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod06',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod06',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod06',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod06',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod06',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod06',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod07',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod07',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod07',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod07',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod07',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod07',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod07',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod07',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod08',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod08',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod08',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod08',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod08',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod08',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod08',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod08',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod09',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod09',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod09',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod09',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod09',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod09',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod09',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod09',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod10',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod10',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod10',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod10',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod10',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod10',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod10',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod10',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod11',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod11',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod11',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod11',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod11',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod11',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod11',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod11',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod12',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod12',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod12',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod12',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod12',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod12',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod12',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod12',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod13',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod13',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod13',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod13',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod13',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod13',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod13',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod13',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod14',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod14',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod14',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod14',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod14',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod14',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod14',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod14',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod15',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod15',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod15',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod15',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod15',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod15',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod15',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod15',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod16',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod16',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod16',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod16',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod16',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod16',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod16',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod16',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod17',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod17',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod17',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod17',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod17',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod17',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod17',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod17',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod18',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod18',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod18',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod18',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod18',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod18',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod18',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod18',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod19',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod19',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod19',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod19',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod19',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod19',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod19',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod19',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod20',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod20',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod20',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod20',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod20',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod20',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod20',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod20',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod21',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod21',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod21',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod21',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod21',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod21',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod21',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod21',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod22',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod22',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod22',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod22',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod22',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod22',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod22',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod22',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod23',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod23',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod23',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod23',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod23',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod23',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod23',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod23',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod24',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod24',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod24',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod24',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod24',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod24',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod24',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s002', 'tod24',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod01',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod01',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod01',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod01',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod01',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod01',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod01',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod01',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod02',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod02',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod02',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod02',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod02',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod02',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod02',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod02',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod03',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod03',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod03',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod03',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod03',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod03',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod03',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod03',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod04',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod04',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod04',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod04',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod04',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod04',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod04',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod04',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod05',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod05',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod05',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod05',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod05',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod05',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod05',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod05',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod06',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod06',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod06',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod06',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod06',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod06',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod06',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod06',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod07',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod07',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod07',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod07',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod07',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod07',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod07',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod07',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod08',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod08',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod08',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod08',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod08',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod08',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod08',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod08',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod09',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod09',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod09',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod09',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod09',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod09',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod09',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod09',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod10',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod10',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod10',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod10',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod10',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod10',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod10',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod10',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod11',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod11',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod11',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod11',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod11',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod11',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod11',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod11',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod12',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod12',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod12',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod12',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod12',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod12',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod12',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod12',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod13',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod13',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod13',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod13',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod13',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod13',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod13',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod13',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod14',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod14',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod14',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod14',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod14',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod14',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod14',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod14',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod15',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod15',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod15',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod15',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod15',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod15',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod15',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod15',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod16',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod16',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod16',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod16',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod16',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod16',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod16',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod16',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod17',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod17',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod17',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod17',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod17',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod17',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod17',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod17',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod18',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod18',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod18',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod18',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod18',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod18',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod18',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod18',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod19',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod19',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod19',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod19',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod19',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod19',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod19',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod19',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod20',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod20',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod20',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod20',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod20',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod20',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod20',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod20',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod21',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod21',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod21',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod21',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod21',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod21',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod21',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod21',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod22',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod22',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod22',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod22',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod22',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod22',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod22',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod22',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod23',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod23',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod23',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod23',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod23',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod23',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod23',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod23',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod24',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod24',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod24',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod24',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod24',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod24',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod24',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s003', 'tod24',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod01',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod01',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod01',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod01',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod01',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod01',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod01',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod01',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod02',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod02',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod02',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod02',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod02',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod02',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod02',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod02',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod03',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod03',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod03',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod03',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod03',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod03',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod03',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod03',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod04',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod04',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod04',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod04',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod04',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod04',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod04',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod04',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod05',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod05',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod05',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod05',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod05',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod05',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod05',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod05',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod06',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod06',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod06',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod06',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod06',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod06',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod06',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod06',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod07',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod07',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod07',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod07',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod07',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod07',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod07',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod07',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod08',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod08',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod08',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod08',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod08',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod08',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod08',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod08',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod09',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod09',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod09',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod09',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod09',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod09',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod09',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod09',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod10',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod10',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod10',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod10',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod10',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod10',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod10',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod10',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod11',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod11',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod11',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod11',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod11',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod11',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod11',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod11',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod12',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod12',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod12',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod12',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod12',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod12',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod12',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod12',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod13',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod13',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod13',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod13',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod13',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod13',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod13',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod13',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod14',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod14',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod14',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod14',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod14',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod14',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod14',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod14',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod15',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod15',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod15',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod15',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod15',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod15',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod15',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod15',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod16',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod16',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod16',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod16',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod16',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod16',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod16',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod16',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod17',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod17',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod17',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod17',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod17',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod17',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod17',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod17',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod18',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod18',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod18',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod18',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod18',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod18',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod18',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod18',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod19',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod19',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod19',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod19',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod19',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod19',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod19',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod19',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod20',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod20',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod20',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod20',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod20',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod20',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod20',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod20',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod21',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod21',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod21',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod21',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod21',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod21',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod21',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod21',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod22',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod22',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod22',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod22',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod22',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod22',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod22',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod22',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod23',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod23',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod23',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod23',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod23',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod23',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod23',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod23',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod24',   'ESOLSTCEN', '2015', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod24',   'ESOLSTCEN', '2020', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod24',   'ESOLSTCEN', '2025', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod24',   'ESOLSTCEN', '2030', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod24',   'ESOLSTCEN', '2035', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod24',   'ESOLSTCEN', '2040', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod24',   'ESOLSTCEN', '2045', '0.0','# Hypothetical');
INSERT INTO "CapacityFactorProcess" VALUES('s004', 'tod24',   'ESOLSTCEN', '2050', '0.0','# Hypothetical');


-------------------------------------------------
CREATE TABLE CapacityFactorTech (
   season_name text,
   time_of_day_name text,
   tech text,
   cf_tech real check (cf_tech >=0 AND cf_tech <=1),
   cf_tech_notes text,
   PRIMARY KEY(season_name, time_of_day_name, tech),
   FOREIGN KEY(season_name) REFERENCES time_season(t_season),
   FOREIGN KEY(time_of_day_name) REFERENCES time_of_day(t_day),
   FOREIGN KEY(tech) REFERENCES technologies(tech) );



INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'ENGAACT', '0.9','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'ECOASTMR', '0.9','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'ECOALIGCCS', '0.9','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'ENGACC05', '0.9','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'EDSLCTR', '0.9','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'ECOALSTM', '0.9','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'ENGAACC', '0.9','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'ENGACCR', '0.9','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'ENGACCCCS', '0.9','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'EHYDCONR', '0.249','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'EHYDCONR', '0.24','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'EHYDCONR', '0.226','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'EHYDCONR', '0.316','# ');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'EHYDCONR', '0.316','# ');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'EWNDON', '0.519','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'EWNDON', '0.514','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'EWNDON', '0.505','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'EWNDON', '0.498','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'EWNDON', '0.488','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'EWNDON', '0.48', '# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'EWNDON', '0.443','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'EWNDON', '0.37', '# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'EWNDON', '0.338','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'EWNDON', '0.344','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'EWNDON', '0.356','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'EWNDON', '0.365','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'EWNDON', '0.372','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'EWNDON', '0.381','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'EWNDON', '0.396','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'EWNDON', '0.408','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'EWNDON', '0.416','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'EWNDON', '0.414','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'EWNDON', '0.445','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'EWNDON', '0.493','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'EWNDON', '0.517','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'EWNDON', '0.525','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'EWNDON', '0.524','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'EWNDON', '0.519','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'EWNDON', '0.296','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'EWNDON', '0.287','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'EWNDON', '0.282','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'EWNDON', '0.278','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'EWNDON', '0.27', '# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'EWNDON', '0.257','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'EWNDON', '0.19', '# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'EWNDON', '0.147','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'EWNDON', '0.146','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'EWNDON', '0.155','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'EWNDON', '0.168','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'EWNDON', '0.178','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'EWNDON', '0.192','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'EWNDON', '0.209','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'EWNDON', '0.227','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'EWNDON', '0.247','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'EWNDON', '0.262','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'EWNDON', '0.265','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'EWNDON', '0.265','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'EWNDON', '0.298','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'EWNDON', '0.313','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'EWNDON', '0.311','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'EWNDON', '0.306','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'EWNDON', '0.298','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'EWNDON', '0.438','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'EWNDON', '0.436','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'EWNDON', '0.433','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'EWNDON', '0.43', '# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'EWNDON', '0.427','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'EWNDON', '0.423','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'EWNDON', '0.416','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'EWNDON', '0.377','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'EWNDON', '0.314','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'EWNDON', '0.286','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'EWNDON', '0.286','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'EWNDON', '0.293','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'EWNDON', '0.295','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'EWNDON', '0.295','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'EWNDON', '0.297','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'EWNDON', '0.301','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'EWNDON', '0.302','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'EWNDON', '0.329','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'EWNDON', '0.373','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'EWNDON', '0.403','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'EWNDON', '0.422','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'EWNDON', '0.433','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'EWNDON', '0.437','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'EWNDON', '0.441','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'EWNDON', '0.537','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'EWNDON', '0.536','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'EWNDON', '0.532','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'EWNDON', '0.528','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'EWNDON', '0.521','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'EWNDON', '0.514','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'EWNDON', '0.507','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'EWNDON', '0.492','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'EWNDON', '0.435','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'EWNDON', '0.387','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'EWNDON', '0.373','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'EWNDON', '0.374','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'EWNDON', '0.38', '# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'EWNDON', '0.384','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'EWNDON', '0.385','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'EWNDON', '0.385','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'EWNDON', '0.39', '# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'EWNDON', '0.439','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'EWNDON', '0.478','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'EWNDON', '0.498','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'EWNDON', '0.512','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'EWNDON', '0.52', '# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'EWNDON', '0.528','# NREL Wind Integration National DataSet Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'EWNDON', '0.533','# NREL Wind Integration National DataSet Toolkit');

INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'EBIOIGCC', '0.9','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'EHYDGS', '0.7','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'ECOALIGCC', '0.9','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'EURNALWR', '0.9','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'ESOLPVCEN', '0.0006','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'ESOLPVCEN', '0.0386','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'ESOLPVCEN', '0.177','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'ESOLPVCEN', '0.342','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'ESOLPVCEN', '0.461','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'ESOLPVCEN', '0.532','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'ESOLPVCEN', '0.569','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'ESOLPVCEN', '0.572','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'ESOLPVCEN', '0.545','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'ESOLPVCEN', '0.49','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'ESOLPVCEN', '0.401','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'ESOLPVCEN', '0.277','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'ESOLPVCEN', '0.126','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'ESOLPVCEN', '0.0136','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'ESOLPVCEN', '0.0002','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'ESOLPVCEN', '0.0019','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'ESOLPVCEN', '0.0518','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'ESOLPVCEN', '0.19','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'ESOLPVCEN', '0.339','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'ESOLPVCEN', '0.446','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'ESOLPVCEN', '0.509','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'ESOLPVCEN', '0.541','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'ESOLPVCEN', '0.544','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'ESOLPVCEN', '0.519','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'ESOLPVCEN', '0.466','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'ESOLPVCEN', '0.386','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'ESOLPVCEN', '0.277','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'ESOLPVCEN', '0.151','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'ESOLPVCEN', '0.034','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'ESOLPVCEN', '0.0011','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'ESOLPVCEN', '0.0051','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'ESOLPVCEN', '0.0951','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'ESOLPVCEN', '0.256','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'ESOLPVCEN', '0.369','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'ESOLPVCEN', '0.431','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'ESOLPVCEN', '0.465','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'ESOLPVCEN', '0.466','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'ESOLPVCEN', '0.439','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'ESOLPVCEN', '0.379','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'ESOLPVCEN', '0.278','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'ESOLPVCEN', '0.137','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'ESOLPVCEN', '0.0245','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'ESOLPVCEN', '0.0006','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'ESOLPVCEN', '0.0081','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'ESOLPVCEN', '0.152','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'ESOLPVCEN', '0.301','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'ESOLPVCEN', '0.378','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'ESOLPVCEN', '0.426','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'ESOLPVCEN', '0.445','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'ESOLPVCEN', '0.434','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'ESOLPVCEN', '0.386','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'ESOLPVCEN', '0.283','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'ESOLPVCEN', '0.126','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'ESOLPVCEN', '0.0137','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'ESOLPVCEN', '0.0','# NREL Solar Integration Dataset');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'EHYDREVR', '0.5','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'ESOLPVR', '0.0006','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'ESOLPVR', '0.0386','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'ESOLPVR', '0.177','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'ESOLPVR', '0.342','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'ESOLPVR', '0.461','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'ESOLPVR', '0.532','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'ESOLPVR', '0.569','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'ESOLPVR', '0.572','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'ESOLPVR', '0.545','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'ESOLPVR', '0.49','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'ESOLPVR', '0.401','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'ESOLPVR', '0.277','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'ESOLPVR', '0.126','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'ESOLPVR', '0.0136','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'ESOLPVR', '0.0002','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'ESOLPVR', '0.0019','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'ESOLPVR', '0.0518','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'ESOLPVR', '0.19','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'ESOLPVR', '0.339','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'ESOLPVR', '0.446','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'ESOLPVR', '0.509','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'ESOLPVR', '0.541','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'ESOLPVR', '0.544','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'ESOLPVR', '0.519','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'ESOLPVR', '0.466','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'ESOLPVR', '0.386','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'ESOLPVR', '0.277','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'ESOLPVR', '0.151','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'ESOLPVR', '0.034','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'ESOLPVR', '0.0011','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'ESOLPVR', '0.0051','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'ESOLPVR', '0.0951','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'ESOLPVR', '0.256','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'ESOLPVR', '0.369','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'ESOLPVR', '0.431','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'ESOLPVR', '0.465','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'ESOLPVR', '0.466','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'ESOLPVR', '0.439','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'ESOLPVR', '0.379','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'ESOLPVR', '0.278','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'ESOLPVR', '0.137','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'ESOLPVR', '0.0245','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'ESOLPVR', '0.0006','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'ESOLPVR', '0.0081','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'ESOLPVR', '0.152','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'ESOLPVR', '0.301','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'ESOLPVR', '0.378','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'ESOLPVR', '0.426','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'ESOLPVR', '0.445','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'ESOLPVR', '0.434','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'ESOLPVR', '0.386','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'ESOLPVR', '0.283','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'ESOLPVR', '0.126','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'ESOLPVR', '0.0137','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'ESOLPVR', '0.0','# NREL Solar Integration Dataset');

INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'ELC2DMD', '1.0','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'EGEOBCFS', '0.9','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'EURNALWR15', '0.9','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'ELFGGTR', '0.9','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'ENGACT05', '0.9','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'EWNDOFS', '0.495','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'EWNDOFS', '0.499','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'EWNDOFS', '0.496','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'EWNDOFS', '0.493','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'EWNDOFS', '0.49','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'EWNDOFS', '0.487','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'EWNDOFS', '0.486','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'EWNDOFS', '0.483','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'EWNDOFS', '0.482','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'EWNDOFS', '0.478','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'EWNDOFS', '0.47','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'EWNDOFS', '0.463','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'EWNDOFS', '0.453','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'EWNDOFS', '0.44','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'EWNDOFS', '0.426','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'EWNDOFS', '0.418','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'EWNDOFS', '0.415','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'EWNDOFS', '0.42','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'EWNDOFS', '0.43','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'EWNDOFS', '0.442','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'EWNDOFS', '0.457','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'EWNDOFS', '0.469','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'EWNDOFS', '0.48','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'EWNDOFS', '0.489','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'EWNDOFS', '0.346','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'EWNDOFS', '0.34','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'EWNDOFS', '0.328','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'EWNDOFS', '0.313','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'EWNDOFS', '0.301','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'EWNDOFS', '0.292','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'EWNDOFS', '0.282','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'EWNDOFS', '0.272','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'EWNDOFS', '0.266','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'EWNDOFS', '0.258','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'EWNDOFS', '0.251','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'EWNDOFS', '0.243','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'EWNDOFS', '0.229','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'EWNDOFS', '0.219','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'EWNDOFS', '0.211','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'EWNDOFS', '0.212','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'EWNDOFS', '0.221','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'EWNDOFS', '0.238','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'EWNDOFS', '0.263','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'EWNDOFS', '0.291','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'EWNDOFS', '0.317','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'EWNDOFS', '0.336','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'EWNDOFS', '0.346','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'EWNDOFS', '0.346','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'EWNDOFS', '0.409','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'EWNDOFS', '0.414','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'EWNDOFS', '0.418','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'EWNDOFS', '0.415','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'EWNDOFS', '0.413','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'EWNDOFS', '0.412','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'EWNDOFS', '0.411','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'EWNDOFS', '0.409','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'EWNDOFS', '0.406','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'EWNDOFS', '0.401','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'EWNDOFS', '0.401','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'EWNDOFS', '0.397','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'EWNDOFS', '0.397','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'EWNDOFS', '0.393','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'EWNDOFS', '0.386','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'EWNDOFS', '0.376','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'EWNDOFS', '0.367','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'EWNDOFS', '0.364','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'EWNDOFS', '0.362','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'EWNDOFS', '0.365','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'EWNDOFS', '0.374','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'EWNDOFS', '0.382','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'EWNDOFS', '0.391','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'EWNDOFS', '0.403','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'EWNDOFS', '0.522','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'EWNDOFS', '0.527','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'EWNDOFS', '0.531','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'EWNDOFS', '0.534','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'EWNDOFS', '0.536','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'EWNDOFS', '0.539','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'EWNDOFS', '0.543','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'EWNDOFS', '0.545','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'EWNDOFS', '0.545','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'EWNDOFS', '0.543','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'EWNDOFS', '0.538','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'EWNDOFS', '0.533','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'EWNDOFS', '0.528','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'EWNDOFS', '0.52','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'EWNDOFS', '0.507','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'EWNDOFS', '0.492','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'EWNDOFS', '0.48','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'EWNDOFS', '0.472','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'EWNDOFS', '0.471','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'EWNDOFS', '0.473','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'EWNDOFS', '0.478','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'EWNDOFS', '0.487','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'EWNDOFS', '0.501','# NREL Wind Integration Nationa Dataset Toolkit');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'EWNDOFS', '0.514','# NREL Wind Integration Nationa Dataset Toolkit');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'ENGACTR', '0.9','# MARKAL 2014 v1.1');


INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod01', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod02', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod03', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod04', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod05', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod06', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod07', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod08', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod09', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod10', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod11', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod12', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod13', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod14', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod15', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod16', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod17', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod18', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod19', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod20', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod21', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod22', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod23', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s001', 'tod24', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod01', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod02', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod03', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod04', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod05', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod06', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod07', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod08', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod09', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod10', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod11', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod12', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod13', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod14', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod15', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod16', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod17', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod18', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod19', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod20', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod21', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod22', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod23', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s002', 'tod24', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod01', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod02', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod03', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod04', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod05', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod06', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod07', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod08', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod09', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod10', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod11', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod12', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod13', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod14', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod15', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod16', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod17', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod18', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod19', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod20', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod21', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod22', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod23', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s003', 'tod24', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod01', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod02', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod03', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod04', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod05', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod06', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod07', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod08', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod09', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod10', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod11', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod12', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod13', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod14', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod15', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod16', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod17', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod18', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod19', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod20', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod21', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod22', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod23', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');
INSERT INTO "CapacityFactorTech" VALUES('s004', 'tod24', 'ELFGICER', '0.9','# MARKAL 2014 v1.1');


-------------------------------------------------
CREATE TABLE CapacityToActivity (
   tech text primary key,
   c2a real,
   c2a_notes,
   FOREIGN KEY(tech) REFERENCES technologies(tech) );
INSERT INTO "CapacityToActivity" VALUES('ENGACC05',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('ENGACT05',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('ENGAACC',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('ENGAACT',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('ENGACCCCS',	31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('ENGACCR',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('ENGACTR',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('ECOALSTM',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('ECOALIGCC',	31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('ECOALIGCCS',	31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('ECOASTMR',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('EDSLCTR',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('EURNALWR',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('EURNALWR15',	31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('EBIOIGCC',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('EBIOSTMR',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('EGEOBCFS',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('ESOLPVCEN',	31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('ESOLSTCEN',	31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('ESOLPVR',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('EWNDON',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('EWNDOFS',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('EHYDCONR',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('EHYDREVR',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('ELFGICER',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('ELFGGTR',		31.54,'# GW to PJ');
INSERT INTO "CapacityToActivity" VALUES('EHYDGS',		31.54,'# GW to PJ');

-- Emission control
-- Group existing coal-fired steam turbine
   INSERT INTO "CapacityToActivity" VALUES('E_BLND_BITSUBLIG_COALSTM_R', 1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_BLND_BIT_COALSTM_R',       1,'');

   INSERT INTO "CapacityToActivity" VALUES('E_LNBSNCR_COAB_R',           1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_LNBSNCR_COAB_N',           1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_LNBSCR_COAB_R',            1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_LNBSCR_COAB_N',            1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_PTNOXSCR_COAB',            1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_SNCR_COAB_R',              1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_SNCR_COAB_N',              1,'');
-- INSERT INTO "CapacityToActivity" VALUES('E_SCR_COAB_R',               1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_SCR_COAB_N',               1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_PTNOXLNB_COAB',            1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_LNB_COAB_R',               1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_LNB_COAB_N',               1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_CCR_COAB',                 1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_PTCO2_COAB',               1,'');
-- INSERT INTO "CapacityToActivity" VALUES('E_FGD_COABH_R',              1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_FGD_COABH_N',              1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_FGD_COABM_R',              1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_FGD_COABM_N',              1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_FGD_COABL_R',              1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_FGD_COABL_N',              1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_PTSO2_COABH',              1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_PTSO2_COABM',              1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_PTSO2_COABL',              1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_EA_COAB',                  1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_CCR_COALIGCC_N',           1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_BLND_BITSUBLIG_COALIGCC_N',1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_BLND_BITHML_COALIGCC_N',   1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_CCR_COALSTM_N',            1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_BLND_BITSUBLIG_COALSTM_N', 1,'');
   INSERT INTO "CapacityToActivity" VALUES('E_BLND_BITHML_COALSTM_N',    1,'');

-------------------------------------------------
CREATE TABLE CostInvest (
   tech text,
   vintage integer,
   cost_invest real,
   cost_invest_units text,
   cost_invest_notes text,
   PRIMARY KEY(tech, vintage),
   FOREIGN KEY(tech) REFERENCES technologies(tech),
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods) );

-- New natural gas
INSERT INTO "CostInvest" VALUES('ENGACC05', 2015,923, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGACT05', 2015,979, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGAACC',  2015,1002,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGAACT',  2015,679, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGACCCCS',2015,2023,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ENGACC05', 2020,923, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGACT05', 2020,979, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGAACC',  2020,969, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGAACT',  2020,654, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGACCCCS',2020,1902,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ENGACC05', 2025,923, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGACT05', 2025,979, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGAACC',  2025,953, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGAACT',  2025,641, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGACCCCS',2025,1780,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ENGACC05', 2030,923, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGACT05', 2030,979, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGAACC',  2030,953, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGAACT',  2030,641, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGACCCCS',2030,1780,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ENGACC05', 2035,923, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGACT05', 2035,979, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGAACC',  2035,936, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGAACT',  2035,628, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGACCCCS',2035,1780,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ENGACC05', 2040,923, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGACT05', 2040,979, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGAACC',  2040,936, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGAACT',  2040,628, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGACCCCS',2040,1780,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ENGACC05', 2045,923, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGACT05', 2045,979, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGAACC',  2045,936, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGAACT',  2045,628, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGACCCCS',2045,1780,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ENGACC05', 2050,923, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGACT05', 2050,979, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGAACC',  2050,936, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGAACT',  2050,628, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ENGACCCCS',2050,1780,'M$/GW','# MARKAL 2014 v1.1');

-- New coal
INSERT INTO "CostInvest" VALUES('ECOALSTM',  2015,2898,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ECOALIGCC', 2015,3736,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ECOALIGCCS',2015,6494,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostInvest" VALUES('ECOALOXYCS',2015,6494,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ECOALSTM',  2020,2825,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ECOALIGCC', 2020,3590,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ECOALIGCCS',2020,6121,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostInvest" VALUES('ECOALOXYCS',2020,6494,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ECOALSTM',  2025,2789,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ECOALIGCC', 2025,3518,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ECOALIGCCS',2025,5747,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostInvest" VALUES('ECOALOXYCS',2025,6494,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ECOALSTM',  2030,2789,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ECOALIGCC', 2030,3518,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ECOALIGCCS',2030,5747,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostInvest" VALUES('ECOALOXYCS',2030,6494,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ECOALSTM',  2035,2753,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ECOALIGCC', 2035,3445,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ECOALIGCCS',2035,5747,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostInvest" VALUES('ECOALOXYCS',2035,6494,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ECOALSTM',  2040,2753,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ECOALIGCC', 2040,3445,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ECOALIGCCS',2040,5747,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostInvest" VALUES('ECOALOXYCS',2040,6494,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ECOALSTM',  2045,2753,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ECOALIGCC', 2045,3445,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ECOALIGCCS',2045,5747,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostInvest" VALUES('ECOALOXYCS',2045,6494,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ECOALSTM',  2050,2753,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ECOALIGCC', 2050,3445,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ECOALIGCCS',2050,5747,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostInvest" VALUES('ECOALOXYCS',2050,6494,'M$/GW','# MARKAL 2014 v1.1');

-- New nuclear
INSERT INTO "CostInvest" VALUES('EURNALWR15',2015,5048,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EURNALWR15',2020,4796,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EURNALWR15',2025,4670,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EURNALWR15',2030,4670,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EURNALWR15',2035,4543,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EURNALWR15',2040,4543,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EURNALWR15',2045,4543,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EURNALWR15',2050,4543,'M$/GW','# MARKAL 2014 v1.1');

-- New biomass
INSERT INTO "CostInvest" VALUES('EBIOIGCC',2015,3805,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EBIOIGCC',2020,3657,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EBIOIGCC',2025,3582,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EBIOIGCC',2030,3582,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EBIOIGCC',2035,3508,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EBIOIGCC',2040,3508,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EBIOIGCC',2045,3508,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EBIOIGCC',2050,3508,'M$/GW','# MARKAL 2014 v1.1');

-- New geothermal
INSERT INTO "CostInvest" VALUES('EGEOBCFS',2015,2517,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EGEOBCFS',2020,2391,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EGEOBCFS',2025,2328,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EGEOBCFS',2030,2328,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EGEOBCFS',2035,2266,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EGEOBCFS',2040,2266,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EGEOBCFS',2045,2266,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EGEOBCFS',2050,2266,'M$/GW','# MARKAL 2014 v1.1');

-- New solar
INSERT INTO "CostInvest" VALUES('ESOLPVCEN',2015,3167,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ESOLSTCEN',2015,3841,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ESOLPVCEN',2020,3167,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ESOLSTCEN',2020,3841,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ESOLPVCEN',2025,3167,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ESOLSTCEN',2025,3841,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ESOLPVCEN',2030,3167,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ESOLSTCEN',2030,3841,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ESOLPVCEN',2035,3167,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ESOLSTCEN',2035,3841,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ESOLPVCEN',2040,3167,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ESOLSTCEN',2040,3841,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ESOLPVCEN',2045,3167,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ESOLSTCEN',2045,3841,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('ESOLPVCEN',2050,3167,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('ESOLSTCEN',2050,3841,'M$/GW','# MARKAL 2014 v1.1');

-- New wind
INSERT INTO "CostInvest" VALUES('EWNDON', 2015,2244,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EWNDOFS',2015,4932,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostInvest" VALUES('EWNDOFD',2015,5034,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('EWNDON', 2020,2233,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EWNDOFS',2020,4439,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostInvest" VALUES('EWNDOFD',2020,4530,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('EWNDON', 2025,2221,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EWNDOFS',2025,3945,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostInvest" VALUES('EWNDOFD',2025,4027,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('EWNDON', 2030,2221,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EWNDOFS',2030,3945,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostInvest" VALUES('EWNDOFD',2030,4027,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('EWNDON', 2035,2221,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EWNDOFS',2035,3945,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostInvest" VALUES('EWNDOFD',2035,4027,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('EWNDON', 2040,2221,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EWNDOFS',2040,3945,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostInvest" VALUES('EWNDOFD',2040,4027,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('EWNDON', 2045,2221,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EWNDOFS',2045,3945,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostInvest" VALUES('EWNDOFD',2045,4027,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostInvest" VALUES('EWNDON', 2050,2221,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostInvest" VALUES('EWNDOFS',2050,3945,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostInvest" VALUES('EWNDOFD',2050,4027,'M$/GW','# MARKAL 2014 v1.1');

-- Gulf Stream Energy
INSERT INTO "CostInvest" VALUES('EHYDGS', 2015,9948,'M$/GW','# ');
INSERT INTO "CostInvest" VALUES('EHYDGS', 2020,9948,'M$/GW','# ');
INSERT INTO "CostInvest" VALUES('EHYDGS', 2025,9948,'M$/GW','# ');
INSERT INTO "CostInvest" VALUES('EHYDGS', 2030,9948,'M$/GW','# ');
INSERT INTO "CostInvest" VALUES('EHYDGS', 2035,9948,'M$/GW','# ');
INSERT INTO "CostInvest" VALUES('EHYDGS', 2040,9948,'M$/GW','# ');
INSERT INTO "CostInvest" VALUES('EHYDGS', 2045,9948,'M$/GW','# ');
INSERT INTO "CostInvest" VALUES('EHYDGS', 2050,9948,'M$/GW','# ');

-- Emission control technologies
-- Existing LNB + SCR for coal
INSERT INTO "CostInvest" VALUES('E_LNBSCR_COAB_N',2015,0.948,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNBSCR_COAB_N',2020,0.948,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNBSCR_COAB_N',2025,0.948,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNBSCR_COAB_N',2030,0.948,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNBSCR_COAB_N',2035,0.948,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNBSCR_COAB_N',2040,0.948,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNBSCR_COAB_N',2045,0.948,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNBSCR_COAB_N',2050,0.948,'#M$/PJout','');

-- Future LNB + SNCR for coal
INSERT INTO "CostInvest" VALUES('E_LNBSNCR_COAB_N',2015,0.303,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNBSNCR_COAB_N',2020,0.303,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNBSNCR_COAB_N',2025,0.303,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNBSNCR_COAB_N',2030,0.303,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNBSNCR_COAB_N',2035,0.303,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNBSNCR_COAB_N',2040,0.303,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNBSNCR_COAB_N',2045,0.303,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNBSNCR_COAB_N',2050,0.303,'#M$/PJout','');

-- Future SNCR
INSERT INTO "CostInvest" VALUES('E_SNCR_COAB_N',2015,0.079,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_SNCR_COAB_N',2020,0.079,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_SNCR_COAB_N',2025,0.079,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_SNCR_COAB_N',2030,0.079,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_SNCR_COAB_N',2035,0.079,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_SNCR_COAB_N',2040,0.079,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_SNCR_COAB_N',2045,0.079,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_SNCR_COAB_N',2050,0.079,'#M$/PJout','');

-- Future SCR
INSERT INTO "CostInvest" VALUES('E_SCR_COAB_N',2015,0.665,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_SCR_COAB_N',2020,0.665,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_SCR_COAB_N',2025,0.665,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_SCR_COAB_N',2030,0.665,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_SCR_COAB_N',2035,0.665,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_SCR_COAB_N',2040,0.665,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_SCR_COAB_N',2045,0.665,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_SCR_COAB_N',2050,0.665,'#M$/PJout','');

-- Future LNB
INSERT INTO "CostInvest" VALUES('E_LNB_COAB_N',2015,0.208,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNB_COAB_N',2020,0.208,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNB_COAB_N',2025,0.208,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNB_COAB_N',2030,0.208,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNB_COAB_N',2035,0.208,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNB_COAB_N',2040,0.208,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNB_COAB_N',2045,0.208,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_LNB_COAB_N',2050,0.208,'#M$/PJout','');

-- CO2 emission control for existing coal
INSERT INTO "CostInvest" VALUES('E_CCR_COAB',2015,15.11,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COAB',2020,15.11,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COAB',2025,15.11,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COAB',2030,15.11,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COAB',2035,15.11,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COAB',2040,15.11,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COAB',2045,15.11,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COAB',2050,15.11,'#M$/PJout','');

-- SO2 emission control for high sulfur coal
INSERT INTO "CostInvest" VALUES('E_FGD_COABH_N',2015,2.632,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABH_N',2020,2.632,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABH_N',2025,2.632,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABH_N',2030,2.632,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABH_N',2035,2.632,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABH_N',2040,2.632,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABH_N',2045,2.632,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABH_N',2050,2.632,'#M$/PJout','');

-- SO2 emission control for median sulfur coal
INSERT INTO "CostInvest" VALUES('E_FGD_COABM_N',2015,1.94,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABM_N',2020,1.94,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABM_N',2025,1.94,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABM_N',2030,1.94,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABM_N',2035,1.94,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABM_N',2040,1.94,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABM_N',2045,1.94,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABM_N',2050,1.94,'#M$/PJout','');

-- Future SO2 control for existing low sulfur bit coal
INSERT INTO "CostInvest" VALUES('E_FGD_COABL_N',2015,3.14,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABL_N',2020,3.14,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABL_N',2025,3.14,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABL_N',2030,3.14,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABL_N',2035,3.14,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABL_N',2040,3.14,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABL_N',2045,3.14,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_FGD_COABL_N',2050,3.14,'#M$/PJout','');

-- IGCC CC
INSERT INTO "CostInvest" VALUES('E_CCR_COALIGCC_N',2015,14.52,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COALIGCC_N',2020,14.52,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COALIGCC_N',2025,14.52,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COALIGCC_N',2030,14.52,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COALIGCC_N',2035,14.52,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COALIGCC_N',2040,14.52,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COALIGCC_N',2045,14.52,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COALIGCC_N',2050,14.52,'#M$/PJout','');

-- co2 capture retrofit tech before new coal steam plant
INSERT INTO "CostInvest" VALUES('E_CCR_COALSTM_N',2015,20,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COALSTM_N',2020,20,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COALSTM_N',2025,20,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COALSTM_N',2030,20,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COALSTM_N',2035,20,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COALSTM_N',2040,20,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COALSTM_N',2045,20,'#M$/PJout','');
INSERT INTO "CostInvest" VALUES('E_CCR_COALSTM_N',2050,20,'#M$/PJout','');

-------------------------------------------------
CREATE TABLE CostFixed (
   periods integer NOT NULL,
   tech text NOT NULL,
   vintage integer NOT NULL,
   cost_fixed real,
   cost_fixed_units text,
   cost_fixed_notes text,
   PRIMARY KEY(periods, tech, vintage),
   FOREIGN KEY(periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(tech) REFERENCES technologies(tech),
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods) );

-- Existing natural gas
   INSERT INTO "CostFixed" VALUES(2015,'ENGACTR', 1970,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2020,'ENGACTR', 1970,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2025,'ENGACTR', 1970,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2030,'ENGACTR', 1970,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2035,'ENGACTR', 1970,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'ENGACTR', 1970,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ENGACTR', 1970,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACTR', 1970,5.8, 'M$/GW','# MARKAL 2014 v1.1');

   INSERT INTO "CostFixed" VALUES(2015,'ENGACTR', 1975,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2020,'ENGACTR', 1975,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2025,'ENGACTR', 1975,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2030,'ENGACTR', 1975,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2035,'ENGACTR', 1975,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'ENGACTR', 1975,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ENGACTR', 1975,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACTR', 1975,5.8, 'M$/GW','# MARKAL 2014 v1.1');

   INSERT INTO "CostFixed" VALUES(2015,'ENGACTR', 1980,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2020,'ENGACTR', 1980,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2025,'ENGACTR', 1980,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2030,'ENGACTR', 1980,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2035,'ENGACTR', 1980,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'ENGACTR', 1980,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ENGACTR', 1980,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACTR', 1980,5.8, 'M$/GW','# MARKAL 2014 v1.1');

   INSERT INTO "CostFixed" VALUES(2015,'ENGACTR', 1985,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2020,'ENGACTR', 1985,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2025,'ENGACTR', 1985,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2030,'ENGACTR', 1985,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2035,'ENGACTR', 1985,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'ENGACTR', 1985,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ENGACTR', 1985,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACTR', 1985,5.8, 'M$/GW','# MARKAL 2014 v1.1');

   INSERT INTO "CostFixed" VALUES(2015,'ENGACTR', 1990,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2020,'ENGACTR', 1990,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2025,'ENGACTR', 1990,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2030,'ENGACTR', 1990,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2035,'ENGACTR', 1990,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'ENGACTR', 1990,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ENGACTR', 1990,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACTR', 1990,5.8, 'M$/GW','# MARKAL 2014 v1.1');

   INSERT INTO "CostFixed" VALUES(2015,'ENGACTR', 1995,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2020,'ENGACTR', 1995,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2025,'ENGACTR', 1995,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2030,'ENGACTR', 1995,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2035,'ENGACTR', 1995,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2040,'ENGACTR', 1995,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ENGACTR', 1995,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACTR', 1995,5.8, 'M$/GW','# MARKAL 2014 v1.1');

   INSERT INTO "CostFixed" VALUES(2015,'ENGACTR', 2000,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2020,'ENGACTR', 2000,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2025,'ENGACTR', 2000,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2030,'ENGACTR', 2000,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2035,'ENGACTR', 2000,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2040,'ENGACTR', 2000,5.8, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2045,'ENGACTR', 2000,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACTR', 2000,5.8, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ENGACTR', 2005,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ENGACTR', 2005,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ENGACTR', 2005,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGACTR', 2005,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGACTR', 2005,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACTR', 2005,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGACTR', 2005,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGACTR', 2005,5.8, 'M$/GW','# MARKAL 2014 v1.1');

   INSERT INTO "CostFixed" VALUES(2015,'ENGACCR', 1970,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2020,'ENGACCR', 1970,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2025,'ENGACCR', 1970,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2030,'ENGACCR', 1970,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2035,'ENGACCR', 1970,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'ENGACCR', 1970,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ENGACCR', 1970,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACCR', 1970,4.6, 'M$/GW','# MARKAL 2014 v1.1');

   INSERT INTO "CostFixed" VALUES(2015,'ENGACCR', 1975,4.6, 'M$/GW','# MARKAL 2014 v1.1');
   INSERT INTO "CostFixed" VALUES(2020,'ENGACCR', 1975,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2025,'ENGACCR', 1975,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2030,'ENGACCR', 1975,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2035,'ENGACCR', 1975,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'ENGACCR', 1975,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ENGACCR', 1975,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACCR', 1975,4.6, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ENGACCR', 1980,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ENGACCR', 1980,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ENGACCR', 1980,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2030,'ENGACCR', 1980,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2035,'ENGACCR', 1980,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'ENGACCR', 1980,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ENGACCR', 1980,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACCR', 1980,4.6, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ENGACCR', 1985,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ENGACCR', 1985,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ENGACCR', 1985,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGACCR', 1985,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2035,'ENGACCR', 1985,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'ENGACCR', 1985,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ENGACCR', 1985,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACCR', 1985,4.6, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ENGACCR', 1990,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ENGACCR', 1990,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ENGACCR', 1990,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGACCR', 1990,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGACCR', 1990,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'ENGACCR', 1990,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ENGACCR', 1990,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACCR', 1990,4.6, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ENGACCR', 1995,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ENGACCR', 1995,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ENGACCR', 1995,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGACCR', 1995,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGACCR', 1995,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACCR', 1995,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ENGACCR', 1995,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACCR', 1995,4.6, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ENGACCR', 2000,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ENGACCR', 2000,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ENGACCR', 2000,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGACCR', 2000,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGACCR', 2000,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACCR', 2000,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGACCR', 2000,4.6, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACCR', 2000,4.6, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ENGACCR', 2005,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ENGACCR', 2005,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ENGACCR', 2005,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGACCR', 2005,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGACCR', 2005,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACCR', 2005,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGACCR', 2005,4.6, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGACCR', 2005,4.6, 'M$/GW','# MARKAL 2014 v1.1');

-- Existing coal
   INSERT INTO "CostFixed" VALUES(2015,'ECOASTMR',1970,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2020,'ECOASTMR',1970,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2025,'ECOASTMR',1970,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2030,'ECOASTMR',1970,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2035,'ECOASTMR',1970,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'ECOASTMR',1970,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ECOASTMR',1970,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ECOASTMR',1970,33.0,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ECOASTMR',1975,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ECOASTMR',1975,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2025,'ECOASTMR',1975,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2030,'ECOASTMR',1975,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2035,'ECOASTMR',1975,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'ECOASTMR',1975,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ECOASTMR',1975,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ECOASTMR',1975,33.0,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ECOASTMR',1980,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ECOASTMR',1980,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ECOASTMR',1980,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2030,'ECOASTMR',1980,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2035,'ECOASTMR',1980,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'ECOASTMR',1980,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ECOASTMR',1980,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ECOASTMR',1980,33.0,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ECOASTMR',1985,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ECOASTMR',1985,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ECOASTMR',1985,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ECOASTMR',1985,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2035,'ECOASTMR',1985,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'ECOASTMR',1985,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ECOASTMR',1985,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ECOASTMR',1985,33.0,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ECOASTMR',1990,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ECOASTMR',1990,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ECOASTMR',1990,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ECOASTMR',1990,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ECOASTMR',1990,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'ECOASTMR',1990,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ECOASTMR',1990,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ECOASTMR',1990,33.0,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ECOASTMR',1995,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ECOASTMR',1995,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ECOASTMR',1995,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ECOASTMR',1995,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ECOASTMR',1995,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ECOASTMR',1995,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ECOASTMR',1995,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ECOASTMR',1995,33.0,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ECOASTMR',2000,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ECOASTMR',2000,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ECOASTMR',2000,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ECOASTMR',2000,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ECOASTMR',2000,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ECOASTMR',2000,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ECOASTMR',2000,33.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ECOASTMR',2000,33.0,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ECOASTMR',2005,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ECOASTMR',2005,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ECOASTMR',2005,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ECOASTMR',2005,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ECOASTMR',2005,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ECOASTMR',2005,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ECOASTMR',2005,33.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ECOASTMR',2005,33.0,'M$/GW','# MARKAL 2014 v1.1');

-- Existing oil
-- INSERT INTO "CostFixed" VALUES(2015,'EDSLCCR', 1925,3.18,  'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2020,'EDSLCCR', 1925,3.18,  'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2025,'EDSLCCR', 1925,3.18,  'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2030,'EDSLCCR', 1925,3.18,  'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2035,'EDSLCCR', 1925,3.18,  'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2040,'EDSLCCR', 1925,3.18,  'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2045,'EDSLCCR', 1925,3.18,  'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2050,'EDSLCCR', 1925,3.18,  'M$/GW','# From Samaneh NUSTD');
   
-- INSERT INTO "CostFixed" VALUES(2015,'EDSLCCR', 1970,3.18,  'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2020,'EDSLCCR', 1970,3.18,  'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2025,'EDSLCCR', 1970,3.18,  'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2030,'EDSLCCR', 1970,3.18,  'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2035,'EDSLCCR', 1970,3.18,  'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2040,'EDSLCCR', 1970,3.18,  'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2045,'EDSLCCR', 1970,3.18,  'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2050,'EDSLCCR', 1970,3.18,  'M$/GW','# From Samaneh NUSTD');

   INSERT INTO "CostFixed" VALUES(2015,'EDSLCTR', 1970,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2020,'EDSLCTR', 1970,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2025,'EDSLCTR', 1970,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2030,'EDSLCTR', 1970,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2035,'EDSLCTR', 1970,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'EDSLCTR', 1970,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'EDSLCTR', 1970,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'EDSLCTR', 1970,5.8, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'EDSLCTR', 1975,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'EDSLCTR', 1975,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2025,'EDSLCTR', 1975,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2030,'EDSLCTR', 1975,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2035,'EDSLCTR', 1975,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'EDSLCTR', 1975,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'EDSLCTR', 1975,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'EDSLCTR', 1975,5.8, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'EDSLCTR', 1980,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'EDSLCTR', 1980,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EDSLCTR', 1980,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2030,'EDSLCTR', 1980,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2035,'EDSLCTR', 1980,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'EDSLCTR', 1980,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'EDSLCTR', 1980,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'EDSLCTR', 1980,5.8, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'EDSLCTR', 1985,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'EDSLCTR', 1985,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EDSLCTR', 1985,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EDSLCTR', 1985,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2035,'EDSLCTR', 1985,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'EDSLCTR', 1985,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'EDSLCTR', 1985,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'EDSLCTR', 1985,5.8, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'EDSLCTR', 1990,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'EDSLCTR', 1990,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EDSLCTR', 1990,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EDSLCTR', 1990,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EDSLCTR', 1990,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2040,'EDSLCTR', 1990,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'EDSLCTR', 1990,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'EDSLCTR', 1990,5.8, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'EDSLCTR', 1995,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'EDSLCTR', 1995,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EDSLCTR', 1995,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EDSLCTR', 1995,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EDSLCTR', 1995,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EDSLCTR', 1995,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'EDSLCTR', 1995,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'EDSLCTR', 1995,5.8, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'EDSLCTR', 2000,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'EDSLCTR', 2000,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EDSLCTR', 2000,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EDSLCTR', 2000,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EDSLCTR', 2000,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EDSLCTR', 2000,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EDSLCTR', 2000,5.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'EDSLCTR', 2000,5.8, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'EDSLCTR', 2005,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'EDSLCTR', 2005,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EDSLCTR', 2005,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EDSLCTR', 2005,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EDSLCTR', 2005,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EDSLCTR', 2005,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EDSLCTR', 2005,5.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EDSLCTR', 2005,5.8, 'M$/GW','# MARKAL 2014 v1.1');

-- INSERT INTO "CostFixed" VALUES(2015,'ERFLSTMR',2015,18.857,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2020,'ERFLSTMR',2015,18.857,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2025,'ERFLSTMR',2015,18.857,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2030,'ERFLSTMR',2015,18.857,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2035,'ERFLSTMR',2015,18.857,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2040,'ERFLSTMR',2015,18.857,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2045,'ERFLSTMR',2015,18.857,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2050,'ERFLSTMR',2015,18.857,'M$/GW','# From Samaneh NUSTD');

-- Existing nuclear
INSERT INTO "CostFixed" VALUES(2015,'EURNALWR',2005,83.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'EURNALWR',2005,83.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EURNALWR',2005,83.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EURNALWR',2005,83.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EURNALWR',2005,83.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EURNALWR',2005,83.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EURNALWR',2005,83.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EURNALWR',2005,83.4,'M$/GW','# MARKAL 2014 v1.1');

-- Existing biomass
INSERT INTO "CostFixed" VALUES(2015,'EBIOSTMR',2005,12.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'EBIOSTMR',2005,12.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EBIOSTMR',2005,12.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EBIOSTMR',2005,12.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EBIOSTMR',2005,12.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EBIOSTMR',2005,12.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EBIOSTMR',2005,12.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EBIOSTMR',2005,12.5,'M$/GW','# MARKAL 2014 v1.1');

-- Existing geothermal
-- INSERT INTO "CostFixed" VALUES(2015,'EGEOR',2015,11.964,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2020,'EGEOR',2015,11.964,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2025,'EGEOR',2015,11.964,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2030,'EGEOR',2015,11.964,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2035,'EGEOR',2015,11.964,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2040,'EGEOR',2015,11.964,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2045,'EGEOR',2015,11.964,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2050,'EGEOR',2015,11.964,'M$/GW','# From Samaneh NUSTD');

-- Existing solar
-- INSERT INTO "CostFixed" VALUES(2015,'ESOLTHR',2015,12.0,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2020,'ESOLTHR',2015,12.0,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2025,'ESOLTHR',2015,12.0,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2030,'ESOLTHR',2015,12.0,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2035,'ESOLTHR',2015,12.0,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2040,'ESOLTHR',2015,12.0,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2045,'ESOLTHR',2015,12.0,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2050,'ESOLTHR',2015,12.0,'M$/GW','# From Samaneh NUSTD');

INSERT INTO "CostFixed" VALUES(2015,'ESOLPVR',2005,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ESOLPVR',2005,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ESOLPVR',2005,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ESOLPVR',2005,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ESOLPVR',2005,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ESOLPVR',2005,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ESOLPVR',2005,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ESOLPVR',2005,25.0,'M$/GW','# MARKAL 2014 v1.1');

-- Existing wind
-- INSERT INTO "CostFixed" VALUES(2015,'EWNDR',   2015,13.649,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2020,'EWNDR',   2015,13.649,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2025,'EWNDR',   2015,13.649,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2030,'EWNDR',   2015,13.649,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2035,'EWNDR',   2015,13.649,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2040,'EWNDR',   2015,13.649,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2045,'EWNDR',   2015,13.649,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2050,'EWNDR',   2015,13.649,'M$/GW','# From Samaneh NUSTD');

-- Existing hydro
INSERT INTO "CostFixed" VALUES(2015,'EHYDCONR',2005,9.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'EHYDCONR',2005,9.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EHYDCONR',2005,9.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EHYDCONR',2005,9.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EHYDCONR',2005,9.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EHYDCONR',2005,9.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EHYDCONR',2005,9.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EHYDCONR',2005,9.7,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'EHYDREVR',2005,14.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'EHYDREVR',2005,14.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EHYDREVR',2005,14.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EHYDREVR',2005,14.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EHYDREVR',2005,14.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EHYDREVR',2005,14.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EHYDREVR',2005,14.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EHYDREVR',2005,14.4,'M$/GW','# MARKAL 2014 v1.1');

-- Existing solid waste
-- INSERT INTO "CostFixed" VALUES(2020,'EMSWSTMR',1995,13.046,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2025,'EMSWSTMR',1995,13.046,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2030,'EMSWSTMR',1995,13.046,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2035,'EMSWSTMR',1995,13.046,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2040,'EMSWSTMR',1995,13.046,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2045,'EMSWSTMR',1995,13.046,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2050,'EMSWSTMR',1995,13.046,'M$/GW','# From Samaneh NUSTD');
 
-- INSERT INTO "CostFixed" VALUES(2020,'EMSWSTMR',2015,13.046,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2025,'EMSWSTMR',2015,13.046,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2030,'EMSWSTMR',2015,13.046,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2035,'EMSWSTMR',2015,13.046,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2040,'EMSWSTMR',2015,13.046,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2045,'EMSWSTMR',2015,13.046,'M$/GW','# From Samaneh NUSTD');
-- INSERT INTO "CostFixed" VALUES(2050,'EMSWSTMR',2015,13.046,'M$/GW','# From Samaneh NUSTD');

--Existing landfill gas
INSERT INTO "CostFixed" VALUES(2015,'ELFGICER',2005,197.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ELFGICER',2005,197.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ELFGICER',2005,197.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ELFGICER',2005,197.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ELFGICER',2005,197.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ELFGICER',2005,197.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ELFGICER',2005,197.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ELFGICER',2005,197.5,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ELFGGTR', 2005,159.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ELFGGTR', 2005,159.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ELFGGTR', 2005,159.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ELFGGTR', 2005,159.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ELFGGTR', 2005,159.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ELFGGTR', 2005,159.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ELFGGTR', 2005,159.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ELFGGTR', 2005,159.2,'M$/GW','# MARKAL 2014 v1.1');

-- I stand in between the present and the future
-- Future natural gas
INSERT INTO "CostFixed" VALUES(2015,'ENGACC05', 2015,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ENGACC05', 2015,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ENGACC05', 2015,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGACC05', 2015,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGACC05', 2015,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACC05', 2015,14.0, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ENGACC05', 2015,14.0, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACC05', 2015,14.0, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2020,'ENGACC05', 2020,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ENGACC05', 2020,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGACC05', 2020,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGACC05', 2020,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACC05', 2020,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGACC05', 2020,14.0, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACC05', 2020,14.0, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2025,'ENGACC05', 2025,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGACC05', 2025,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGACC05', 2025,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACC05', 2025,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGACC05', 2025,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGACC05', 2025,14.0, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2030,'ENGACC05', 2030,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGACC05', 2030,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACC05', 2030,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGACC05', 2030,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGACC05', 2030,14.0, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2035,'ENGACC05', 2035,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACC05', 2035,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGACC05', 2035,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGACC05', 2035,14.0, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2040,'ENGACC05', 2040,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGACC05', 2040,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGACC05', 2040,14.0, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2045,'ENGACC05', 2045,14.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGACC05', 2045,14.0, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2050,'ENGACC05', 2050,14.0, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ENGACT05', 2015,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ENGACT05', 2015,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ENGACT05', 2015,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGACT05', 2015,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGACT05', 2015,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACT05', 2015,7.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ENGACT05', 2015,7.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACT05', 2015,7.8, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2020,'ENGACT05', 2020,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ENGACT05', 2020,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGACT05', 2020,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGACT05', 2020,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACT05', 2020,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGACT05', 2020,7.8, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACT05', 2020,7.8, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2025,'ENGACT05', 2025,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGACT05', 2025,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGACT05', 2025,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACT05', 2025,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGACT05', 2025,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGACT05', 2025,7.8, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2030,'ENGACT05', 2030,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGACT05', 2030,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACT05', 2030,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGACT05', 2030,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGACT05', 2030,7.8, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2035,'ENGACT05', 2035,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACT05', 2035,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGACT05', 2035,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGACT05', 2035,7.8, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2040,'ENGACT05', 2040,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGACT05', 2040,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGACT05', 2040,7.8, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2045,'ENGACT05', 2045,7.8, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGACT05', 2045,7.8, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2050,'ENGACT05', 2050,7.8, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ENGAACC',  2015,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ENGAACC',  2015,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ENGAACC',  2015,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGAACC',  2015,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGAACC',  2015,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGAACC',  2015,16.3,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ENGAACC',  2015,16.3,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGAACC',  2015,16.3,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2020,'ENGAACC',  2020,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ENGAACC',  2020,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGAACC',  2020,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGAACC',  2020,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGAACC',  2020,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGAACC',  2020,16.3,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGAACC',  2020,16.3,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2025,'ENGAACC',  2025,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGAACC',  2025,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGAACC',  2025,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGAACC',  2025,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGAACC',  2025,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGAACC',  2025,16.3,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2030,'ENGAACC',  2030,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGAACC',  2030,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGAACC',  2030,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGAACC',  2030,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGAACC',  2030,16.3,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2035,'ENGAACC',  2035,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGAACC',  2035,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGAACC',  2035,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGAACC',  2035,16.3,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2040,'ENGAACC',  2040,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGAACC',  2040,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGAACC',  2040,16.3,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2045,'ENGAACC',  2045,16.3,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGAACC',  2045,16.3,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2050,'ENGAACC',  2050,16.3,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ENGAACT',  2015,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ENGAACT',  2015,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ENGAACT',  2015,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGAACT',  2015,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGAACT',  2015,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGAACT',  2015,7.5, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ENGAACT',  2015,7.5, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGAACT',  2015,7.5, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2020,'ENGAACT',  2020,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ENGAACT',  2020,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGAACT',  2020,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGAACT',  2020,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGAACT',  2020,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGAACT',  2020,7.5, 'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGAACT',  2020,7.5, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2025,'ENGAACT',  2025,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGAACT',  2025,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGAACT',  2025,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGAACT',  2025,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGAACT',  2025,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGAACT',  2025,7.5, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2030,'ENGAACT',  2030,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGAACT',  2030,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGAACT',  2030,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGAACT',  2030,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGAACT',  2030,7.5, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2035,'ENGAACT',  2035,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGAACT',  2035,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGAACT',  2035,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGAACT',  2035,7.5, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2040,'ENGAACT',  2040,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGAACT',  2040,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGAACT',  2040,7.5, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2045,'ENGAACT',  2045,7.5, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGAACT',  2045,7.5, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2050,'ENGAACT',  2050,7.5, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ENGACCCCS',2015,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ENGACCCCS',2015,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ENGACCCCS',2015,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGACCCCS',2015,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGACCCCS',2015,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACCCCS',2015,34.7,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ENGACCCCS',2015,34.7,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACCCCS',2015,34.7,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2020,'ENGACCCCS',2020,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ENGACCCCS',2020,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGACCCCS',2020,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGACCCCS',2020,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACCCCS',2020,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGACCCCS',2020,34.7,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ENGACCCCS',2020,34.7,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2025,'ENGACCCCS',2025,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ENGACCCCS',2025,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGACCCCS',2025,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACCCCS',2025,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGACCCCS',2025,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGACCCCS',2025,34.7,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2030,'ENGACCCCS',2030,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ENGACCCCS',2030,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACCCCS',2030,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGACCCCS',2030,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGACCCCS',2030,34.7,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2035,'ENGACCCCS',2035,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ENGACCCCS',2035,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGACCCCS',2035,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGACCCCS',2035,34.7,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2040,'ENGACCCCS',2040,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ENGACCCCS',2040,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGACCCCS',2040,34.7,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2045,'ENGACCCCS',2045,34.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ENGACCCCS',2045,34.7,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2050,'ENGACCCCS',2050,34.7,'M$/GW','# MARKAL 2014 v1.1');

-- Future coal
INSERT INTO "CostFixed" VALUES(2015,'ECOALSTM',  2015,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ECOALSTM',  2015,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ECOALSTM',  2015,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ECOALSTM',  2015,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ECOALSTM',  2015,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ECOALSTM',  2015,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ECOALSTM',  2015,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ECOALSTM',  2015,33.0, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2020,'ECOALSTM',  2020,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ECOALSTM',  2020,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ECOALSTM',  2020,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ECOALSTM',  2020,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ECOALSTM',  2020,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ECOALSTM',  2020,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ECOALSTM',  2020,33.0, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2025,'ECOALSTM',  2025,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ECOALSTM',  2025,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ECOALSTM',  2025,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ECOALSTM',  2025,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ECOALSTM',  2025,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ECOALSTM',  2025,33.0, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2030,'ECOALSTM',  2030,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ECOALSTM',  2030,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ECOALSTM',  2030,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ECOALSTM',  2030,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ECOALSTM',  2030,33.0, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2035,'ECOALSTM',  2035,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ECOALSTM',  2035,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ECOALSTM',  2035,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ECOALSTM',  2035,33.0, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2040,'ECOALSTM',  2040,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ECOALSTM',  2040,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ECOALSTM',  2040,33.0, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2045,'ECOALSTM',  2045,33.0, 'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ECOALSTM',  2045,33.0, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2050,'ECOALSTM',  2050,33.0, 'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ECOALIGCC', 2015,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ECOALIGCC', 2015,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ECOALIGCC', 2015,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ECOALIGCC', 2015,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ECOALIGCC', 2015,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ECOALIGCC', 2015,54.5,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ECOALIGCC', 2015,54.5,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ECOALIGCC', 2015,54.5,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2020,'ECOALIGCC', 2020,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ECOALIGCC', 2020,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ECOALIGCC', 2020,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ECOALIGCC', 2020,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ECOALIGCC', 2020,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ECOALIGCC', 2020,54.5,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ECOALIGCC', 2020,54.5,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2025,'ECOALIGCC', 2025,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ECOALIGCC', 2025,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ECOALIGCC', 2025,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ECOALIGCC', 2025,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ECOALIGCC', 2025,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ECOALIGCC', 2025,54.5,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2030,'ECOALIGCC', 2030,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ECOALIGCC', 2030,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ECOALIGCC', 2030,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ECOALIGCC', 2030,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ECOALIGCC', 2030,54.5,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2035,'ECOALIGCC', 2035,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ECOALIGCC', 2035,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ECOALIGCC', 2035,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ECOALIGCC', 2035,54.5,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2040,'ECOALIGCC', 2040,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ECOALIGCC', 2040,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ECOALIGCC', 2040,54.5,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2045,'ECOALIGCC', 2045,54.5,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ECOALIGCC', 2045,54.5,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2050,'ECOALIGCC', 2050,54.5,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'ECOALIGCCS',2015,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ECOALIGCCS',2015,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ECOALIGCCS',2015,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ECOALIGCCS',2015,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ECOALIGCCS',2015,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ECOALIGCCS',2015,79.4,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ECOALIGCCS',2015,79.4,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ECOALIGCCS',2015,79.4,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2020,'ECOALIGCCS',2020,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ECOALIGCCS',2020,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ECOALIGCCS',2020,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ECOALIGCCS',2020,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ECOALIGCCS',2020,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ECOALIGCCS',2020,79.4,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ECOALIGCCS',2020,79.4,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2025,'ECOALIGCCS',2025,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ECOALIGCCS',2025,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ECOALIGCCS',2025,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ECOALIGCCS',2025,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ECOALIGCCS',2025,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ECOALIGCCS',2025,79.4,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2030,'ECOALIGCCS',2030,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ECOALIGCCS',2030,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ECOALIGCCS',2030,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ECOALIGCCS',2030,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ECOALIGCCS',2030,79.4,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2035,'ECOALIGCCS',2035,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ECOALIGCCS',2035,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ECOALIGCCS',2035,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ECOALIGCCS',2035,79.4,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2040,'ECOALIGCCS',2040,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ECOALIGCCS',2040,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ECOALIGCCS',2040,79.4,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2045,'ECOALIGCCS',2045,79.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ECOALIGCCS',2045,79.4,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2050,'ECOALIGCCS',2050,79.4,'M$/GW','# MARKAL 2014 v1.1');

-- Future nuclear
INSERT INTO "CostFixed" VALUES(2015,'EURNALWR15',2015,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'EURNALWR15',2015,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EURNALWR15',2015,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EURNALWR15',2015,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EURNALWR15',2015,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EURNALWR15',2015,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EURNALWR15',2015,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EURNALWR15',2015,98.9,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2020,'EURNALWR15',2020,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EURNALWR15',2020,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EURNALWR15',2020,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EURNALWR15',2020,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EURNALWR15',2020,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EURNALWR15',2020,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EURNALWR15',2020,98.9,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2025,'EURNALWR15',2025,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EURNALWR15',2025,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EURNALWR15',2025,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EURNALWR15',2025,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EURNALWR15',2025,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EURNALWR15',2025,98.9,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2030,'EURNALWR15',2030,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EURNALWR15',2030,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EURNALWR15',2030,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EURNALWR15',2030,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EURNALWR15',2030,98.9,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2035,'EURNALWR15',2035,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EURNALWR15',2035,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EURNALWR15',2035,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EURNALWR15',2035,98.9,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2040,'EURNALWR15',2040,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EURNALWR15',2040,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EURNALWR15',2040,98.9,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2045,'EURNALWR15',2045,98.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EURNALWR15',2045,98.9,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2050,'EURNALWR15',2050,98.9,'M$/GW','# MARKAL 2014 v1.1');

-- Future biomass
INSERT INTO "CostFixed" VALUES(2015,'EBIOIGCC',2015,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'EBIOIGCC',2015,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EBIOIGCC',2015,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EBIOIGCC',2015,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EBIOIGCC',2015,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EBIOIGCC',2015,112.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'EBIOIGCC',2015,112.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'EBIOIGCC',2015,112.0,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2020,'EBIOIGCC',2020,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EBIOIGCC',2020,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EBIOIGCC',2020,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EBIOIGCC',2020,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EBIOIGCC',2020,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EBIOIGCC',2020,112.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'EBIOIGCC',2020,112.0,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2025,'EBIOIGCC',2025,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EBIOIGCC',2025,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EBIOIGCC',2025,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EBIOIGCC',2025,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EBIOIGCC',2025,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EBIOIGCC',2025,112.0,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2030,'EBIOIGCC',2030,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EBIOIGCC',2030,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EBIOIGCC',2030,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EBIOIGCC',2030,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EBIOIGCC',2030,112.0,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2035,'EBIOIGCC',2035,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EBIOIGCC',2035,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EBIOIGCC',2035,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EBIOIGCC',2035,112.0,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2040,'EBIOIGCC',2040,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EBIOIGCC',2040,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EBIOIGCC',2040,112.0,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2045,'EBIOIGCC',2045,112.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EBIOIGCC',2045,112.0,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2050,'EBIOIGCC',2050,112.0,'M$/GW','# MARKAL 2014 v1.1');

-- Future geothermal
INSERT INTO "CostFixed" VALUES(2015,'EGEOBCFS',2015,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'EGEOBCFS',2015,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EGEOBCFS',2015,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EGEOBCFS',2015,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EGEOBCFS',2015,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EGEOBCFS',2015,119.7,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'EGEOBCFS',2015,119.7,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'EGEOBCFS',2015,119.7,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2020,'EGEOBCFS',2020,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EGEOBCFS',2020,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EGEOBCFS',2020,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EGEOBCFS',2020,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EGEOBCFS',2020,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EGEOBCFS',2020,119.7,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'EGEOBCFS',2020,119.7,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2025,'EGEOBCFS',2025,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EGEOBCFS',2025,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EGEOBCFS',2025,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EGEOBCFS',2025,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EGEOBCFS',2025,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EGEOBCFS',2025,119.7,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2030,'EGEOBCFS',2030,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EGEOBCFS',2030,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EGEOBCFS',2030,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EGEOBCFS',2030,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EGEOBCFS',2030,119.7,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2035,'EGEOBCFS',2035,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EGEOBCFS',2035,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EGEOBCFS',2035,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EGEOBCFS',2035,119.7,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2040,'EGEOBCFS',2040,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EGEOBCFS',2040,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EGEOBCFS',2040,119.7,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2045,'EGEOBCFS',2045,119.7,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EGEOBCFS',2045,119.7,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2050,'EGEOBCFS',2050,119.7,'M$/GW','# MARKAL 2014 v1.1');

-- Future solar
INSERT INTO "CostFixed" VALUES(2015,'ESOLPVCEN',2015,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ESOLPVCEN',2015,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ESOLPVCEN',2015,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ESOLPVCEN',2015,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ESOLPVCEN',2015,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ESOLPVCEN',2015,25.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ESOLPVCEN',2015,25.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ESOLPVCEN',2015,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2015,'ESOLSTCEN',2015,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ESOLSTCEN',2015,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ESOLSTCEN',2015,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ESOLSTCEN',2015,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ESOLSTCEN',2015,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ESOLSTCEN',2015,68.2,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'ESOLSTCEN',2015,68.2,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ESOLSTCEN',2015,68.2,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2020,'ESOLPVCEN',2020,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ESOLPVCEN',2020,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ESOLPVCEN',2020,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ESOLPVCEN',2020,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ESOLPVCEN',2020,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ESOLPVCEN',2020,25.0,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ESOLPVCEN',2020,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'ESOLSTCEN',2020,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ESOLSTCEN',2020,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ESOLSTCEN',2020,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ESOLSTCEN',2020,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ESOLSTCEN',2020,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ESOLSTCEN',2020,68.2,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'ESOLSTCEN',2020,68.2,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2025,'ESOLPVCEN',2025,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ESOLPVCEN',2025,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ESOLPVCEN',2025,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ESOLPVCEN',2025,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ESOLPVCEN',2025,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ESOLPVCEN',2025,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'ESOLSTCEN',2025,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ESOLSTCEN',2025,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ESOLSTCEN',2025,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ESOLSTCEN',2025,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ESOLSTCEN',2025,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ESOLSTCEN',2025,68.2,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2030,'ESOLPVCEN',2030,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ESOLPVCEN',2030,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ESOLPVCEN',2030,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ESOLPVCEN',2030,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ESOLPVCEN',2030,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'ESOLSTCEN',2030,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ESOLSTCEN',2030,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ESOLSTCEN',2030,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ESOLSTCEN',2030,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ESOLSTCEN',2030,68.2,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2035,'ESOLPVCEN',2035,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ESOLPVCEN',2035,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ESOLPVCEN',2035,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ESOLPVCEN',2035,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'ESOLSTCEN',2035,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ESOLSTCEN',2035,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ESOLSTCEN',2035,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ESOLSTCEN',2035,68.2,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2040,'ESOLPVCEN',2040,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ESOLPVCEN',2040,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ESOLPVCEN',2040,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'ESOLSTCEN',2040,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ESOLSTCEN',2040,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ESOLSTCEN',2040,68.2,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2045,'ESOLPVCEN',2045,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ESOLPVCEN',2045,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'ESOLSTCEN',2045,68.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ESOLSTCEN',2045,68.2,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2050,'ESOLPVCEN',2050,25.0,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'ESOLSTCEN',2050,68.2,'M$/GW','# MARKAL 2014 v1.1');

-- Future wind
INSERT INTO "CostFixed" VALUES(2015,'EWNDON', 2015,28.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'EWNDON', 2015,28.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EWNDON', 2015,28.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EWNDON', 2015,28.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EWNDON', 2015,28.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EWNDON', 2015,28.4,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'EWNDON', 2015,28.4,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'EWNDON', 2015,28.4,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2020,'EWNDON', 2020,28.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EWNDON', 2020,28.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EWNDON', 2020,28.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EWNDON', 2020,28.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EWNDON', 2020,28.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EWNDON', 2020,28.4,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'EWNDON', 2020,28.4,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2025,'EWNDON', 2025,27.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EWNDON', 2025,27.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EWNDON', 2025,27.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EWNDON', 2025,27.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EWNDON', 2025,27.2,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EWNDON', 2025,27.2,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2030,'EWNDON', 2030,25.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EWNDON', 2030,25.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EWNDON', 2030,25.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EWNDON', 2030,25.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EWNDON', 2030,25.9,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2035,'EWNDON', 2035,25.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EWNDON', 2035,25.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EWNDON', 2035,25.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EWNDON', 2035,25.9,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2040,'EWNDON', 2040,25.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EWNDON', 2040,25.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EWNDON', 2040,25.9,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2045,'EWNDON', 2045,25.9,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EWNDON', 2045,25.9,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2050,'EWNDON', 2050,25.9,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2015,'EWNDOFS',2015,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2020,'EWNDOFS',2015,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EWNDOFS',2015,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EWNDOFS',2015,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EWNDOFS',2015,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EWNDOFS',2015,78.4,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2045,'EWNDOFS',2015,78.4,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'EWNDOFS',2015,78.4,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2020,'EWNDOFS',2020,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2025,'EWNDOFS',2020,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EWNDOFS',2020,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EWNDOFS',2020,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EWNDOFS',2020,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EWNDOFS',2020,78.4,'M$/GW','# MARKAL 2014 v1.1');
-- INSERT INTO "CostFixed" VALUES(2050,'EWNDOFS',2020,78.4,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2025,'EWNDOFS',2025,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2030,'EWNDOFS',2025,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EWNDOFS',2025,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EWNDOFS',2025,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EWNDOFS',2025,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EWNDOFS',2025,78.4,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2030,'EWNDOFS',2030,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2035,'EWNDOFS',2030,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EWNDOFS',2030,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EWNDOFS',2030,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EWNDOFS',2030,78.4,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2035,'EWNDOFS',2035,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2040,'EWNDOFS',2035,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EWNDOFS',2035,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EWNDOFS',2035,78.4,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2040,'EWNDOFS',2040,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2045,'EWNDOFS',2040,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EWNDOFS',2040,78.4,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2045,'EWNDOFS',2045,78.4,'M$/GW','# MARKAL 2014 v1.1');
INSERT INTO "CostFixed" VALUES(2050,'EWNDOFS',2045,78.4,'M$/GW','# MARKAL 2014 v1.1');

INSERT INTO "CostFixed" VALUES(2050,'EWNDOFS',2050,78.4,'M$/GW','# MARKAL 2014 v1.1');

-- Gulf Stream Energy
   INSERT INTO "CostFixed" VALUES(2015,'EHYDGS',2015,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2020,'EHYDGS',2015,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2025,'EHYDGS',2015,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2030,'EHYDGS',2015,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2035,'EHYDGS',2015,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2040,'EHYDGS',2015,573,'M$/GW','# ');
-- INSERT INTO "CostFixed" VALUES(2045,'EHYDGS',2015,573,'M$/GW','# ');
-- INSERT INTO "CostFixed" VALUES(2050,'EHYDGS',2015,573,'M$/GW','# ');

   INSERT INTO "CostFixed" VALUES(2020,'EHYDGS',2020,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2025,'EHYDGS',2020,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2030,'EHYDGS',2020,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2035,'EHYDGS',2020,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2040,'EHYDGS',2020,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2045,'EHYDGS',2020,573,'M$/GW','# ');
-- INSERT INTO "CostFixed" VALUES(2050,'EHYDGS',2020,573,'M$/GW','# ');

   INSERT INTO "CostFixed" VALUES(2025,'EHYDGS',2025,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2030,'EHYDGS',2025,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2035,'EHYDGS',2025,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2040,'EHYDGS',2025,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2045,'EHYDGS',2025,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2050,'EHYDGS',2025,573,'M$/GW','# ');
   
   INSERT INTO "CostFixed" VALUES(2030,'EHYDGS',2030,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2035,'EHYDGS',2030,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2040,'EHYDGS',2030,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2045,'EHYDGS',2030,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2050,'EHYDGS',2030,573,'M$/GW','# ');
   
   INSERT INTO "CostFixed" VALUES(2035,'EHYDGS',2035,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2040,'EHYDGS',2035,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2045,'EHYDGS',2035,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2050,'EHYDGS',2035,573,'M$/GW','# ');
   
   INSERT INTO "CostFixed" VALUES(2040,'EHYDGS',2040,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2045,'EHYDGS',2040,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2050,'EHYDGS',2040,573,'M$/GW','# ');
   
   INSERT INTO "CostFixed" VALUES(2045,'EHYDGS',2045,573,'M$/GW','# ');
   INSERT INTO "CostFixed" VALUES(2050,'EHYDGS',2045,573,'M$/GW','# ');
   
   INSERT INTO "CostFixed" VALUES(2050,'EHYDGS',2050,573,'M$/GW','# ');

-- CO2 emission control for existing coal
INSERT INTO "CostFixed" VALUES(2015,'E_CCR_COAB',        2015,0.264,'#M$/PJout',''); 
INSERT INTO "CostFixed" VALUES(2020,'E_CCR_COAB',        2015,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2025,'E_CCR_COAB',        2015,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2030,'E_CCR_COAB',        2015,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2035,'E_CCR_COAB',        2015,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2040,'E_CCR_COAB',        2015,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COAB',        2015,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COAB',        2015,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2020,'E_CCR_COAB',        2020,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2025,'E_CCR_COAB',        2020,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2030,'E_CCR_COAB',        2020,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2035,'E_CCR_COAB',        2020,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2040,'E_CCR_COAB',        2020,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COAB',        2020,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COAB',        2020,0.264,'#M$/PJ','');
INSERT INTO "CostFixed" VALUES(2025,'E_CCR_COAB',        2025,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2030,'E_CCR_COAB',        2025,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2035,'E_CCR_COAB',        2025,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2040,'E_CCR_COAB',        2025,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COAB',        2025,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COAB',        2025,0.264,'#M$/PJ','');
INSERT INTO "CostFixed" VALUES(2030,'E_CCR_COAB',        2030,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2035,'E_CCR_COAB',        2030,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2040,'E_CCR_COAB',        2030,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COAB',        2030,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COAB',        2030,0.264,'#M$/PJ','');
INSERT INTO "CostFixed" VALUES(2035,'E_CCR_COAB',        2035,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2040,'E_CCR_COAB',        2035,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COAB',        2035,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COAB',        2035,0.264,'#M$/PJ','');
INSERT INTO "CostFixed" VALUES(2040,'E_CCR_COAB',        2040,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COAB',        2040,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COAB',        2040,0.264,'#M$/PJ','');
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COAB',        2045,0.264,'#M$/PJ',''); 
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COAB',        2045,0.264,'#M$/PJ','');
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COAB',        2050,0.264,'#M$/PJ','');

-- IGCC CC
INSERT INTO "CostFixed" VALUES(2015,'E_CCR_COALIGCC_N',    2015,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2020,'E_CCR_COALIGCC_N',    2015,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2025,'E_CCR_COALIGCC_N',    2015,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2030,'E_CCR_COALIGCC_N',    2015,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2035,'E_CCR_COALIGCC_N',    2015,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2040,'E_CCR_COALIGCC_N',    2015,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COALIGCC_N',    2015,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COALIGCC_N',    2015,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2020,'E_CCR_COALIGCC_N',    2020,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2025,'E_CCR_COALIGCC_N',    2020,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2030,'E_CCR_COALIGCC_N',    2020,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2035,'E_CCR_COALIGCC_N',    2020,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2040,'E_CCR_COALIGCC_N',    2020,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COALIGCC_N',    2020,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COALIGCC_N',    2020,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2025,'E_CCR_COALIGCC_N',    2025,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2030,'E_CCR_COALIGCC_N',    2025,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2035,'E_CCR_COALIGCC_N',    2025,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2040,'E_CCR_COALIGCC_N',    2025,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COALIGCC_N',    2025,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COALIGCC_N',    2025,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2030,'E_CCR_COALIGCC_N',    2030,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2035,'E_CCR_COALIGCC_N',    2030,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2040,'E_CCR_COALIGCC_N',    2030,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COALIGCC_N',    2030,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COALIGCC_N',    2030,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2035,'E_CCR_COALIGCC_N',    2035,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2040,'E_CCR_COALIGCC_N',    2035,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COALIGCC_N',    2035,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COALIGCC_N',    2035,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2040,'E_CCR_COALIGCC_N',    2040,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COALIGCC_N',    2040,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COALIGCC_N',    2040,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COALIGCC_N',    2045,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COALIGCC_N',    2045,0.435,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COALIGCC_N',    2050,0.435,'#M$/PJout','');

-- co2 capture retrofit tech before new coal steam plant
INSERT INTO "CostFixed" VALUES(2015,'E_CCR_COALSTM_N',     2015,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2020,'E_CCR_COALSTM_N',     2015,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2025,'E_CCR_COALSTM_N',     2015,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2030,'E_CCR_COALSTM_N',     2015,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2035,'E_CCR_COALSTM_N',     2015,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2040,'E_CCR_COALSTM_N',     2015,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COALSTM_N',     2015,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COALSTM_N',     2015,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2020,'E_CCR_COALSTM_N',     2020,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2025,'E_CCR_COALSTM_N',     2020,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2030,'E_CCR_COALSTM_N',     2020,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2035,'E_CCR_COALSTM_N',     2020,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2040,'E_CCR_COALSTM_N',     2020,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COALSTM_N',     2020,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COALSTM_N',     2020,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2025,'E_CCR_COALSTM_N',     2025,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2030,'E_CCR_COALSTM_N',     2025,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2035,'E_CCR_COALSTM_N',     2025,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2040,'E_CCR_COALSTM_N',     2025,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COALSTM_N',     2025,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COALSTM_N',     2025,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2030,'E_CCR_COALSTM_N',     2030,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2035,'E_CCR_COALSTM_N',     2030,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2040,'E_CCR_COALSTM_N',     2030,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COALSTM_N',     2030,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COALSTM_N',     2030,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2035,'E_CCR_COALSTM_N',     2035,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2040,'E_CCR_COALSTM_N',     2035,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COALSTM_N',     2035,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COALSTM_N',     2035,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2040,'E_CCR_COALSTM_N',     2040,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COALSTM_N',     2040,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COALSTM_N',     2040,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2045,'E_CCR_COALSTM_N',     2045,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COALSTM_N',     2045,0.346,'#M$/PJout','');
INSERT INTO "CostFixed" VALUES(2050,'E_CCR_COALSTM_N',     2050,0.346,'#M$/PJout','');

-------------------------------------------------
-- Note: Transmission & Distribution cost is included
CREATE TABLE CostVariable (
   periods integer NOT NULL,
   tech text NOT NULL,
   vintage integer NOT NULL,
   cost_variable real,
   cost_variable_units text,
   cost_variable_notes text,
   PRIMARY KEY(periods, tech, vintage),
   FOREIGN KEY(periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(tech) REFERENCES technologies(tech),
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods) );
   
-- Existing natural gas
   INSERT INTO "CostVariable" VALUES(2015,'ENGACCR', 1970,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2020,'ENGACCR', 1970,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2025,'ENGACCR', 1970,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2030,'ENGACCR', 1970,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2035,'ENGACCR', 1970,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'ENGACCR', 1970,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ENGACCR', 1970,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACCR', 1970,12.550,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGACCR', 1975,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGACCR', 1975,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2025,'ENGACCR', 1975,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2030,'ENGACCR', 1975,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2035,'ENGACCR', 1975,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'ENGACCR', 1975,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ENGACCR', 1975,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACCR', 1975,12.550,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGACCR', 1980,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGACCR', 1980,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ENGACCR', 1980,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2030,'ENGACCR', 1980,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2035,'ENGACCR', 1980,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'ENGACCR', 1980,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ENGACCR', 1980,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACCR', 1980,12.550,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGACCR', 1985,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGACCR', 1985,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ENGACCR', 1985,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ENGACCR', 1985,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2035,'ENGACCR', 1985,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'ENGACCR', 1985,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ENGACCR', 1985,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACCR', 1985,12.550,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGACCR', 1990,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGACCR', 1990,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ENGACCR', 1990,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ENGACCR', 1990,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ENGACCR', 1990,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'ENGACCR', 1990,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ENGACCR', 1990,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACCR', 1990,12.550,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGACCR', 1995,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGACCR', 1995,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ENGACCR', 1995,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ENGACCR', 1995,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ENGACCR', 1995,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'ENGACCR', 1995,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ENGACCR', 1995,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACCR', 1995,12.550,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGACCR', 2000,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGACCR', 2000,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ENGACCR', 2000,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ENGACCR', 2000,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ENGACCR', 2000,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'ENGACCR', 2000,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2045,'ENGACCR', 2000,12.550,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACCR', 2000,12.550,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGACCR', 2005,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGACCR', 2005,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ENGACCR', 2005,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ENGACCR', 2005,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ENGACCR', 2005,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'ENGACCR', 2005,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2045,'ENGACCR', 2005,12.550,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2050,'ENGACCR', 2005,12.550,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGACTR', 1970,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2020,'ENGACTR', 1970,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2025,'ENGACTR', 1970,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2030,'ENGACTR', 1970,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2035,'ENGACTR', 1970,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'ENGACTR', 1970,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ENGACTR', 1970,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACTR', 1970,20.438,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGACTR', 1975,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGACTR', 1975,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2025,'ENGACTR', 1975,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2030,'ENGACTR', 1975,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2035,'ENGACTR', 1975,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'ENGACTR', 1975,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ENGACTR', 1975,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACTR', 1975,20.438,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGACTR', 1980,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGACTR', 1980,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ENGACTR', 1980,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2030,'ENGACTR', 1980,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2035,'ENGACTR', 1980,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'ENGACTR', 1980,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ENGACTR', 1980,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACTR', 1980,20.438,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGACTR', 1985,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGACTR', 1985,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ENGACTR', 1985,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ENGACTR', 1985,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2035,'ENGACTR', 1985,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'ENGACTR', 1985,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ENGACTR', 1985,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACTR', 1985,20.438,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGACTR', 1990,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGACTR', 1990,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ENGACTR', 1990,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ENGACTR', 1990,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ENGACTR', 1990,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'ENGACTR', 1990,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ENGACTR', 1990,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACTR', 1990,20.438,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGACTR', 1995,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGACTR', 1995,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ENGACTR', 1995,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ENGACTR', 1995,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ENGACTR', 1995,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'ENGACTR', 1995,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ENGACTR', 1995,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACTR', 1995,20.438,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGACTR', 2000,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGACTR', 2000,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ENGACTR', 2000,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ENGACTR', 2000,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ENGACTR', 2000,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'ENGACTR', 2000,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2045,'ENGACTR', 2000,20.438,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACTR', 2000,20.438,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGACTR', 2005,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGACTR', 2005,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ENGACTR', 2005,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ENGACTR', 2005,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ENGACTR', 2005,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'ENGACTR', 2005,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2045,'ENGACTR', 2005,20.438,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2050,'ENGACTR', 2005,20.438,'M$/PJ','# MARKAL 2014 v1.1');

-- INSERT INTO "CostVariable" VALUES(2020,'ENGASTMR',2015,12.988,'M$/PJ','# From Samaneh NUSTD');
-- INSERT INTO "CostVariable" VALUES(2025,'ENGASTMR',2015,12.988,'M$/PJ','# From Samaneh NUSTD');
-- INSERT INTO "CostVariable" VALUES(2030,'ENGASTMR',2015,12.988,'M$/PJ','# From Samaneh NUSTD');
-- INSERT INTO "CostVariable" VALUES(2035,'ENGASTMR',2015,12.988,'M$/PJ','# From Samaneh NUSTD');
-- INSERT INTO "CostVariable" VALUES(2040,'ENGASTMR',2015,12.988,'M$/PJ','# From Samaneh NUSTD');
-- INSERT INTO "CostVariable" VALUES(2045,'ENGASTMR',2015,12.988,'M$/PJ','# From Samaneh NUSTD');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGASTMR',2015,12.988,'M$/PJ','# From Samaneh NUSTD');

-- Existing coal
   INSERT INTO "CostVariable" VALUES(2015,'ECOASTMR',1970,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2020,'ECOASTMR',1970,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2025,'ECOASTMR',1970,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2030,'ECOASTMR',1970,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2035,'ECOASTMR',1970,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'ECOASTMR',1970,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ECOASTMR',1970,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ECOASTMR',1970,12.440,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ECOASTMR',1975,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ECOASTMR',1975,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2025,'ECOASTMR',1975,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2030,'ECOASTMR',1975,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2035,'ECOASTMR',1975,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'ECOASTMR',1975,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ECOASTMR',1975,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ECOASTMR',1975,12.440,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ECOASTMR',1980,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ECOASTMR',1980,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ECOASTMR',1980,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2030,'ECOASTMR',1980,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2035,'ECOASTMR',1980,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'ECOASTMR',1980,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ECOASTMR',1980,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ECOASTMR',1980,12.440,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ECOASTMR',1985,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ECOASTMR',1985,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ECOASTMR',1985,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ECOASTMR',1985,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2035,'ECOASTMR',1985,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'ECOASTMR',1985,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ECOASTMR',1985,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ECOASTMR',1985,12.440,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ECOASTMR',1990,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ECOASTMR',1990,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ECOASTMR',1990,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ECOASTMR',1990,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ECOASTMR',1990,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'ECOASTMR',1990,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ECOASTMR',1990,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ECOASTMR',1990,12.440,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ECOASTMR',1995,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ECOASTMR',1995,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ECOASTMR',1995,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ECOASTMR',1995,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ECOASTMR',1995,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'ECOASTMR',1995,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ECOASTMR',1995,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ECOASTMR',1995,12.440,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ECOASTMR',2000,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ECOASTMR',2000,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ECOASTMR',2000,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ECOASTMR',2000,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ECOASTMR',2000,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'ECOASTMR',2000,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2045,'ECOASTMR',2000,12.440,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ECOASTMR',2000,12.440,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ECOASTMR',2005,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ECOASTMR',2005,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ECOASTMR',2005,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ECOASTMR',2005,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ECOASTMR',2005,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'ECOASTMR',2005,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2045,'ECOASTMR',2005,12.440,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2050,'ECOASTMR',2005,12.440,'M$/PJ','# MARKAL 2014 v1.1');

-- Existing oil
   INSERT INTO "CostVariable" VALUES(2015,'EDSLCTR', 1970,8.459,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2020,'EDSLCTR', 1970,8.459,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2025,'EDSLCTR', 1970,8.459,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2030,'EDSLCTR', 1970,8.459,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2035,'EDSLCTR', 1970,8.459,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'EDSLCTR', 1970,8.459,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'EDSLCTR', 1970,8.459,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'EDSLCTR', 1970,8.459,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'EDSLCTR', 1975,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'EDSLCTR', 1975,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2025,'EDSLCTR', 1975,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2030,'EDSLCTR', 1975,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2035,'EDSLCTR', 1975,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'EDSLCTR', 1975,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'EDSLCTR', 1975,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'EDSLCTR', 1975,21.357,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'EDSLCTR', 1980,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'EDSLCTR', 1980,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'EDSLCTR', 1980,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2030,'EDSLCTR', 1980,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2035,'EDSLCTR', 1980,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'EDSLCTR', 1980,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'EDSLCTR', 1980,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'EDSLCTR', 1980,21.357,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'EDSLCTR', 1985,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'EDSLCTR', 1985,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'EDSLCTR', 1985,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'EDSLCTR', 1985,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2035,'EDSLCTR', 1985,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'EDSLCTR', 1985,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'EDSLCTR', 1985,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'EDSLCTR', 1985,21.357,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'EDSLCTR', 1990,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'EDSLCTR', 1990,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'EDSLCTR', 1990,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'EDSLCTR', 1990,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'EDSLCTR', 1990,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2040,'EDSLCTR', 1990,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'EDSLCTR', 1990,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'EDSLCTR', 1990,21.357,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'EDSLCTR', 1995,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'EDSLCTR', 1995,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'EDSLCTR', 1995,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'EDSLCTR', 1995,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'EDSLCTR', 1995,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'EDSLCTR', 1995,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'EDSLCTR', 1995,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'EDSLCTR', 1995,21.357,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'EDSLCTR', 2000,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'EDSLCTR', 2000,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'EDSLCTR', 2000,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'EDSLCTR', 2000,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'EDSLCTR', 2000,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'EDSLCTR', 2000,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2045,'EDSLCTR', 2000,21.357,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'EDSLCTR', 2000,21.357,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'EDSLCTR', 2005,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'EDSLCTR', 2005,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'EDSLCTR', 2005,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'EDSLCTR', 2005,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'EDSLCTR', 2005,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'EDSLCTR', 2005,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2045,'EDSLCTR', 2005,21.357,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2050,'EDSLCTR', 2005,21.357,'M$/PJ','# MARKAL 2014 v1.1');

-- Existing nuclear
INSERT INTO "CostVariable" VALUES(2015,'EURNALWR',2005,11.583,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2020,'EURNALWR',2005,11.583,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'EURNALWR',2005,11.583,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'EURNALWR',2005,11.583,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EURNALWR',2005,11.583,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EURNALWR',2005,11.583,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EURNALWR',2005,11.583,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EURNALWR',2005,11.583,'M$/PJ','# MARKAL 2014 v1.1');

-- Existing biomass
INSERT INTO "CostVariable" VALUES(2015,'EBIOSTMR',2005,17.033,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2020,'EBIOSTMR',2005,17.033,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'EBIOSTMR',2005,17.033,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'EBIOSTMR',2005,17.033,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EBIOSTMR',2005,17.033,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EBIOSTMR',2005,17.033,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EBIOSTMR',2005,17.033,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EBIOSTMR',2005,17.033,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2015,'ESOLPVR',2005,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2020,'ESOLPVR',2005,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'ESOLPVR',2005,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ESOLPVR',2005,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ESOLPVR',2005,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ESOLPVR',2005,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ESOLPVR',2005,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ESOLPVR',2005,11.124,'M$/PJ','# MARKAL 2014 v1.1');

-- Existing hydro
INSERT INTO "CostVariable" VALUES(2015,'EHYDCONR',2005,16.368,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2020,'EHYDCONR',2005,16.368,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'EHYDCONR',2005,16.368,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'EHYDCONR',2005,16.368,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EHYDCONR',2005,16.368,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EHYDCONR',2005,16.368,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EHYDCONR',2005,16.368,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EHYDCONR',2005,16.368,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2015,'EHYDREVR',2005,17.248,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2020,'EHYDREVR',2005,17.248,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'EHYDREVR',2005,17.248,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'EHYDREVR',2005,17.248,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EHYDREVR',2005,17.248,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EHYDREVR',2005,17.248,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EHYDREVR',2005,17.248,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EHYDREVR',2005,17.248,'M$/PJ','# MARKAL 2014 v1.1');

-- Existing LFG
INSERT INTO "CostVariable" VALUES(2015,'ELFGICER',2005,11.124,'M$/PJ','#');
INSERT INTO "CostVariable" VALUES(2020,'ELFGICER',2005,11.124,'M$/PJ','#');
INSERT INTO "CostVariable" VALUES(2025,'ELFGICER',2005,11.124,'M$/PJ','#');
INSERT INTO "CostVariable" VALUES(2030,'ELFGICER',2005,11.124,'M$/PJ','#');
INSERT INTO "CostVariable" VALUES(2035,'ELFGICER',2005,11.124,'M$/PJ','#');
INSERT INTO "CostVariable" VALUES(2040,'ELFGICER',2005,11.124,'M$/PJ','#');
INSERT INTO "CostVariable" VALUES(2045,'ELFGICER',2005,11.124,'M$/PJ','#');
INSERT INTO "CostVariable" VALUES(2050,'ELFGICER',2005,11.124,'M$/PJ','#');

INSERT INTO "CostVariable" VALUES(2015,'ELFGGTR',2005,11.124,'M$/PJ','#');
INSERT INTO "CostVariable" VALUES(2020,'ELFGGTR',2005,11.124,'M$/PJ','#');
INSERT INTO "CostVariable" VALUES(2025,'ELFGGTR',2005,11.124,'M$/PJ','#');
INSERT INTO "CostVariable" VALUES(2030,'ELFGGTR',2005,11.124,'M$/PJ','#');
INSERT INTO "CostVariable" VALUES(2035,'ELFGGTR',2005,11.124,'M$/PJ','#');
INSERT INTO "CostVariable" VALUES(2040,'ELFGGTR',2005,11.124,'M$/PJ','#');
INSERT INTO "CostVariable" VALUES(2045,'ELFGGTR',2005,11.124,'M$/PJ','#');
INSERT INTO "CostVariable" VALUES(2050,'ELFGGTR',2005,11.124,'M$/PJ','#');


-- I stand in between the present and the future
-- Future natural gas
   INSERT INTO "CostVariable" VALUES(2015,'ENGACC05', 2015,11.388, 'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGACC05', 2015,11.388, 'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ENGACC05', 2015,11.388, 'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ENGACC05', 2015,11.388, 'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ENGACC05', 2015,11.388, 'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'ENGACC05', 2015,11.388, 'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ENGACC05', 2015,11.388, 'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACC05', 2015,11.388, 'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2020,'ENGACC05', 2020,12.184, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'ENGACC05', 2020,12.184, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ENGACC05', 2020,12.184, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ENGACC05', 2020,12.184, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGACC05', 2020,12.184, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGACC05', 2020,12.184, 'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACC05', 2020,12.184, 'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2025,'ENGACC05', 2025,12.460, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ENGACC05', 2025,12.460, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ENGACC05', 2025,12.460, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGACC05', 2025,12.460, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGACC05', 2025,12.460, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGACC05', 2025,12.460, 'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2030,'ENGACC05', 2030,12.725, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ENGACC05', 2030,12.725, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGACC05', 2030,12.725, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGACC05', 2030,12.725, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGACC05', 2030,12.725, 'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2035,'ENGACC05', 2035,12.990, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGACC05', 2035,12.990, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGACC05', 2035,12.990, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGACC05', 2035,12.990, 'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2040,'ENGACC05', 2040,13.177, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGACC05', 2040,13.177, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGACC05', 2040,13.177, 'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2045,'ENGACC05', 2045,13.462, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGACC05', 2045,13.462, 'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2050,'ENGACC05', 2050,13.714, 'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGACT05', 2015,14.877,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGACT05', 2015,14.877,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ENGACT05', 2015,14.877,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ENGACT05', 2015,14.877,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ENGACT05', 2015,14.877,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'ENGACT05', 2015,14.877,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ENGACT05', 2015,14.877,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACT05', 2015,14.877,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2020,'ENGACT05', 2020,15.673,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'ENGACT05', 2020,15.673,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ENGACT05', 2020,15.673,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ENGACT05', 2020,15.673,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGACT05', 2020,15.673,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGACT05', 2020,15.673,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACT05', 2020,15.673,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2025,'ENGACT05', 2025,15.949,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ENGACT05', 2025,15.949,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ENGACT05', 2025,15.949,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGACT05', 2025,15.949,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGACT05', 2025,15.949,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGACT05', 2025,15.949,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2030,'ENGACT05', 2030,16.214,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ENGACT05', 2030,16.214,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGACT05', 2030,16.214,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGACT05', 2030,16.214,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGACT05', 2030,16.214,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2035,'ENGACT05', 2035,16.479,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGACT05', 2035,16.479,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGACT05', 2035,16.479,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGACT05', 2035,16.479,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2040,'ENGACT05', 2040,16.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGACT05', 2040,16.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGACT05', 2040,16.666,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2045,'ENGACT05', 2045,16.951,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGACT05', 2045,16.951,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2050,'ENGACT05', 2050,17.202,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGAACC',  2015,11.291,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGAACC',  2015,11.291,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ENGAACC',  2015,11.291,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ENGAACC',  2015,11.291,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ENGAACC',  2015,11.291,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'ENGAACC',  2015,11.291,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ENGAACC',  2015,11.291,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGAACC',  2015,11.291,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2020,'ENGAACC',  2020,12.087,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'ENGAACC',  2020,12.087,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ENGAACC',  2020,12.087,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ENGAACC',  2020,12.087,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGAACC',  2020,12.087,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGAACC',  2020,12.087,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGAACC',  2020,12.087,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2025,'ENGAACC',  2025,12.363,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ENGAACC',  2025,12.363,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ENGAACC',  2025,12.363,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGAACC',  2025,12.363,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGAACC',  2025,12.363,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGAACC',  2025,12.363,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2030,'ENGAACC',  2030,12.628,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ENGAACC',  2030,12.628,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGAACC',  2030,12.628,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGAACC',  2030,12.628,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGAACC',  2030,12.628,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2035,'ENGAACC',  2035,12.893,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGAACC',  2035,12.893,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGAACC',  2035,12.893,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGAACC',  2035,12.893,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2040,'ENGAACC',  2040,13.080,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGAACC',  2040,13.080,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGAACC',  2040,13.080,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2045,'ENGAACC',  2045,13.365,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGAACC',  2045,13.365,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2050,'ENGAACC',  2050,13.616,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGAACT',  2015,13.382, 'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGAACT',  2015,13.382, 'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ENGAACT',  2015,13.382, 'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ENGAACT',  2015,13.382, 'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ENGAACT',  2015,13.382, 'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'ENGAACT',  2015,13.382, 'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ENGAACT',  2015,13.382, 'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGAACT',  2015,13.382, 'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2020,'ENGAACT',  2020,14.177, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'ENGAACT',  2020,14.177, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ENGAACT',  2020,14.177, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ENGAACT',  2020,14.177, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGAACT',  2020,14.177, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGAACT',  2020,14.177, 'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGAACT',  2020,14.177, 'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2025,'ENGAACT',  2025,14.453, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ENGAACT',  2025,14.453, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ENGAACT',  2025,14.453, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGAACT',  2025,14.453, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGAACT',  2025,14.453, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGAACT',  2025,14.453, 'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2030,'ENGAACT',  2030,14.719, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ENGAACT',  2030,14.719, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGAACT',  2030,14.719, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGAACT',  2030,14.719, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGAACT',  2030,14.719, 'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2035,'ENGAACT',  2035,14.983, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGAACT',  2035,14.983, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGAACT',  2035,14.983, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGAACT',  2035,14.983, 'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2040,'ENGAACT',  2040,15.170, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGAACT',  2040,15.170, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGAACT',  2040,15.170, 'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2045,'ENGAACT',  2045,15.455, 'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGAACT',  2045,15.455, 'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2050,'ENGAACT',  2050,15.707, 'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ENGACCCCS',2015,12.381,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ENGACCCCS',2015,12.381,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ENGACCCCS',2015,12.381,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ENGACCCCS',2015,12.381,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ENGACCCCS',2015,12.381,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'ENGACCCCS',2015,12.381,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ENGACCCCS',2015,12.381,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACCCCS',2015,12.381,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2020,'ENGACCCCS',2020,13.177,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'ENGACCCCS',2020,13.177,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ENGACCCCS',2020,13.177,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ENGACCCCS',2020,13.177,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGACCCCS',2020,13.177,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGACCCCS',2020,13.177,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ENGACCCCS',2020,13.177,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2025,'ENGACCCCS',2025,13.453,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ENGACCCCS',2025,13.453,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ENGACCCCS',2025,13.453,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGACCCCS',2025,13.453,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGACCCCS',2025,13.453,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGACCCCS',2025,13.453,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2030,'ENGACCCCS',2030,13.718,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ENGACCCCS',2030,13.718,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGACCCCS',2030,13.718,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGACCCCS',2030,13.718,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGACCCCS',2030,13.718,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2035,'ENGACCCCS',2035,13.983,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ENGACCCCS',2035,13.983,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGACCCCS',2035,13.983,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGACCCCS',2035,13.983,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2040,'ENGACCCCS',2040,14.170,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ENGACCCCS',2040,14.170,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGACCCCS',2040,14.170,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2045,'ENGACCCCS',2045,14.455,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ENGACCCCS',2045,14.455,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2050,'ENGACCCCS',2050,14.707,'M$/PJ','# MARKAL 2014 v1.1');

-- Future coal
INSERT INTO "CostVariable" VALUES(2015,'ECOALSTM',  2015,11.645,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2020,'ECOALSTM',  2015,11.645,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'ECOALSTM',  2015,11.645,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ECOALSTM',  2015,11.645,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ECOALSTM',  2015,11.645,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ECOALSTM',  2015,11.645,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ECOALSTM',  2015,11.645,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ECOALSTM',  2015,11.645,  'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2020,'ECOALSTM',  2020,12.440,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'ECOALSTM',  2020,12.440,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ECOALSTM',  2020,12.440,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ECOALSTM',  2020,12.440,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ECOALSTM',  2020,12.440,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ECOALSTM',  2020,12.440,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ECOALSTM',  2020,12.440,  'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2025,'ECOALSTM',  2025,12.716,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ECOALSTM',  2025,12.716,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ECOALSTM',  2025,12.716,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ECOALSTM',  2025,12.716,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ECOALSTM',  2025,12.716,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ECOALSTM',  2025,12.716,  'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2030,'ECOALSTM',  2030,12.982,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ECOALSTM',  2030,12.982,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ECOALSTM',  2030,12.982,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ECOALSTM',  2030,12.982,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ECOALSTM',  2030,12.982,  'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2035,'ECOALSTM',  2035,13.246,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ECOALSTM',  2035,13.246,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ECOALSTM',  2035,13.246,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ECOALSTM',  2035,13.246,  'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2040,'ECOALSTM',  2040,13.433,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ECOALSTM',  2040,13.433,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ECOALSTM',  2040,13.433,  'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2045,'ECOALSTM',  2045,13.718,  'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ECOALSTM',  2045,13.718,  'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2050,'ECOALSTM',  2050,13.970,  'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ECOALIGCC', 2015,12.454,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ECOALIGCC', 2015,12.454,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ECOALIGCC', 2015,12.454,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ECOALIGCC', 2015,12.454,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ECOALIGCC', 2015,12.454,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'ECOALIGCC', 2015,12.454,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ECOALIGCC', 2015,12.454,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ECOALIGCC', 2015,12.454,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2020,'ECOALIGCC', 2020,13.250,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'ECOALIGCC', 2020,13.250,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ECOALIGCC', 2020,13.250,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ECOALIGCC', 2020,13.250,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ECOALIGCC', 2020,13.250,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ECOALIGCC', 2020,13.250,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ECOALIGCC', 2020,13.250,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2025,'ECOALIGCC', 2025,13.526,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ECOALIGCC', 2025,13.526,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ECOALIGCC', 2025,13.526,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ECOALIGCC', 2025,13.526,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ECOALIGCC', 2025,13.526,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ECOALIGCC', 2025,13.526,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2030,'ECOALIGCC', 2030,13.791,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ECOALIGCC', 2030,13.791,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ECOALIGCC', 2030,13.791,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ECOALIGCC', 2030,13.791,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ECOALIGCC', 2030,13.791,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2035,'ECOALIGCC', 2035,14.056,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ECOALIGCC', 2035,14.056,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ECOALIGCC', 2035,14.056,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ECOALIGCC', 2035,14.056,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2040,'ECOALIGCC', 2040,14.243,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ECOALIGCC', 2040,14.243,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ECOALIGCC', 2040,14.243,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2045,'ECOALIGCC', 2045,14.528,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ECOALIGCC', 2045,14.528,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2050,'ECOALIGCC', 2050,14.779,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2015,'ECOALIGCCS',2015,12.887,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ECOALIGCCS',2015,12.887,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ECOALIGCCS',2015,12.887,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ECOALIGCCS',2015,12.887,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ECOALIGCCS',2015,12.887,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'ECOALIGCCS',2015,12.887,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ECOALIGCCS',2015,12.887,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ECOALIGCCS',2015,12.887,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2020,'ECOALIGCCS',2020,13.683,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'ECOALIGCCS',2020,13.683,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ECOALIGCCS',2020,13.683,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ECOALIGCCS',2020,13.683,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ECOALIGCCS',2020,13.683,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ECOALIGCCS',2020,13.683,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ECOALIGCCS',2020,13.683,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2025,'ECOALIGCCS',2025,13.959,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ECOALIGCCS',2025,13.959,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ECOALIGCCS',2025,13.959,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ECOALIGCCS',2025,13.959,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ECOALIGCCS',2025,13.959,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ECOALIGCCS',2025,13.959,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2030,'ECOALIGCCS',2030,14.224,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ECOALIGCCS',2030,14.224,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ECOALIGCCS',2030,14.224,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ECOALIGCCS',2030,14.224,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ECOALIGCCS',2030,14.224,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2035,'ECOALIGCCS',2035,14.489,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ECOALIGCCS',2035,14.489,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ECOALIGCCS',2035,14.489,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ECOALIGCCS',2035,14.489,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2040,'ECOALIGCCS',2040,14.675,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ECOALIGCCS',2040,14.675,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ECOALIGCCS',2040,14.675,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2045,'ECOALIGCCS',2045,14.961,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ECOALIGCCS',2045,14.961,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2050,'ECOALIGCCS',2050,15.212,'M$/PJ','# MARKAL 2014 v1.1');

-- Future nuclear
INSERT INTO "CostVariable" VALUES(2015,'EURNALWR15',2015,10.959,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2020,'EURNALWR15',2015,10.959,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'EURNALWR15',2015,10.959,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'EURNALWR15',2015,10.959,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EURNALWR15',2015,10.959,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EURNALWR15',2015,10.959,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EURNALWR15',2015,10.959,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EURNALWR15',2015,10.959,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2020,'EURNALWR15',2020,11.754,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'EURNALWR15',2020,11.754,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'EURNALWR15',2020,11.754,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EURNALWR15',2020,11.754,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EURNALWR15',2020,11.754,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EURNALWR15',2020,11.754,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EURNALWR15',2020,11.754,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2025,'EURNALWR15',2025,12.030,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'EURNALWR15',2025,12.030,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EURNALWR15',2025,12.030,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EURNALWR15',2025,12.030,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EURNALWR15',2025,12.030,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EURNALWR15',2025,12.030,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2030,'EURNALWR15',2030,12.296,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EURNALWR15',2030,12.296,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EURNALWR15',2030,12.296,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EURNALWR15',2030,12.296,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EURNALWR15',2030,12.296,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2035,'EURNALWR15',2035,12.560,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EURNALWR15',2035,12.560,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EURNALWR15',2035,12.560,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EURNALWR15',2035,12.560,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2040,'EURNALWR15',2040,12.747,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EURNALWR15',2040,12.747,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EURNALWR15',2040,12.747,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2045,'EURNALWR15',2045,13.032,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EURNALWR15',2045,13.032,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2050,'EURNALWR15',2050,13.284,'M$/PJ','# MARKAL 2014 v1.1');

-- Future biomass
   INSERT INTO "CostVariable" VALUES(2015,'EBIOIGCC',2015,11.877,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'EBIOIGCC',2015,11.877,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'EBIOIGCC',2015,11.877,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'EBIOIGCC',2015,11.877,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'EBIOIGCC',2015,11.877,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'EBIOIGCC',2015,11.877,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'EBIOIGCC',2015,11.877,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'EBIOIGCC',2015,11.877,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2020,'EBIOIGCC',2020,12.673,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'EBIOIGCC',2020,12.673,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'EBIOIGCC',2020,12.673,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EBIOIGCC',2020,12.673,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EBIOIGCC',2020,12.673,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EBIOIGCC',2020,12.673,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'EBIOIGCC',2020,12.673,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2025,'EBIOIGCC',2025,12.949,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'EBIOIGCC',2025,12.949,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EBIOIGCC',2025,12.949,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EBIOIGCC',2025,12.949,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EBIOIGCC',2025,12.949,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EBIOIGCC',2025,12.949,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2030,'EBIOIGCC',2030,13.214,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EBIOIGCC',2030,13.214,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EBIOIGCC',2030,13.214,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EBIOIGCC',2030,13.214,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EBIOIGCC',2030,13.214,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2035,'EBIOIGCC',2035,13.479,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EBIOIGCC',2035,13.479,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EBIOIGCC',2035,13.479,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EBIOIGCC',2035,13.479,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2040,'EBIOIGCC',2040,13.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EBIOIGCC',2040,13.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EBIOIGCC',2040,13.666,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2045,'EBIOIGCC',2045,13.951,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EBIOIGCC',2045,13.951,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2050,'EBIOIGCC',2050,14.202,'M$/PJ','# MARKAL 2014 v1.1');

-- Future geothermal
   INSERT INTO "CostVariable" VALUES(2015,'EGEOBCFS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'EGEOBCFS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'EGEOBCFS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'EGEOBCFS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'EGEOBCFS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'EGEOBCFS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'EGEOBCFS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'EGEOBCFS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2020,'EGEOBCFS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'EGEOBCFS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'EGEOBCFS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EGEOBCFS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EGEOBCFS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EGEOBCFS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'EGEOBCFS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2025,'EGEOBCFS',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'EGEOBCFS',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EGEOBCFS',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EGEOBCFS',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EGEOBCFS',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EGEOBCFS',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2030,'EGEOBCFS',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EGEOBCFS',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EGEOBCFS',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EGEOBCFS',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EGEOBCFS',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2035,'EGEOBCFS',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EGEOBCFS',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EGEOBCFS',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EGEOBCFS',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2040,'EGEOBCFS',2040,12.117,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EGEOBCFS',2040,12.117,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EGEOBCFS',2040,12.117,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2045,'EGEOBCFS',2045,12.402,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EGEOBCFS',2045,12.402,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2050,'EGEOBCFS',2050,12.654,'M$/PJ','# MARKAL 2014 v1.1');

-- Future solar
   INSERT INTO "CostVariable" VALUES(2015,'ESOLPVCEN',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ESOLPVCEN',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ESOLPVCEN',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ESOLPVCEN',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ESOLPVCEN',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'ESOLPVCEN',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ESOLPVCEN',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ESOLPVCEN',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2015,'ESOLSTCEN',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'ESOLSTCEN',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'ESOLSTCEN',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'ESOLSTCEN',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'ESOLSTCEN',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'ESOLSTCEN',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'ESOLSTCEN',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ESOLSTCEN',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2020,'ESOLPVCEN',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'ESOLPVCEN',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ESOLPVCEN',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ESOLPVCEN',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ESOLPVCEN',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ESOLPVCEN',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ESOLPVCEN',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2020,'ESOLSTCEN',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'ESOLSTCEN',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ESOLSTCEN',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ESOLSTCEN',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ESOLSTCEN',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ESOLSTCEN',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'ESOLSTCEN',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2025,'ESOLPVCEN',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ESOLPVCEN',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ESOLPVCEN',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ESOLPVCEN',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ESOLPVCEN',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ESOLPVCEN',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'ESOLSTCEN',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ESOLSTCEN',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ESOLSTCEN',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ESOLSTCEN',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ESOLSTCEN',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ESOLSTCEN',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2030,'ESOLPVCEN',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ESOLPVCEN',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ESOLPVCEN',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ESOLPVCEN',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ESOLPVCEN',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'ESOLSTCEN',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ESOLSTCEN',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ESOLSTCEN',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ESOLSTCEN',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ESOLSTCEN',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2035,'ESOLPVCEN',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ESOLPVCEN',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ESOLPVCEN',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ESOLPVCEN',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'ESOLSTCEN',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ESOLSTCEN',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ESOLSTCEN',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ESOLSTCEN',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2040,'ESOLPVCEN',2040,12.117,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ESOLPVCEN',2040,12.117,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ESOLPVCEN',2040,12.117,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'ESOLSTCEN',2040,12.117,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ESOLSTCEN',2040,12.117,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ESOLSTCEN',2040,12.117,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2045,'ESOLPVCEN',2045,12.402,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ESOLPVCEN',2045,12.402,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'ESOLSTCEN',2045,12.402,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ESOLSTCEN',2045,12.402,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2050,'ESOLPVCEN',2050,12.654,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'ESOLSTCEN',2050,12.654,'M$/PJ','# MARKAL 2014 v1.1');

-- Future wind
   INSERT INTO "CostVariable" VALUES(2015,'EWNDON', 2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'EWNDON', 2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'EWNDON', 2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'EWNDON', 2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'EWNDON', 2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'EWNDON', 2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'EWNDON', 2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'EWNDON', 2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2015,'EWNDOFS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'EWNDOFS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'EWNDOFS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'EWNDOFS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'EWNDOFS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'EWNDOFS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'EWNDOFS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'EWNDOFS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2020,'EWNDON', 2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'EWNDON', 2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'EWNDON', 2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EWNDON', 2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EWNDON', 2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EWNDON', 2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'EWNDON', 2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2020,'EWNDOFS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'EWNDOFS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'EWNDOFS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EWNDOFS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EWNDOFS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EWNDOFS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'EWNDOFS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2025,'EWNDON', 2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'EWNDON', 2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EWNDON', 2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EWNDON', 2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EWNDON', 2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EWNDON', 2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2025,'EWNDOFS',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'EWNDOFS',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EWNDOFS',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EWNDOFS',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EWNDOFS',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EWNDOFS',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2030,'EWNDON', 2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EWNDON', 2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EWNDON', 2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EWNDON', 2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EWNDON', 2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2030,'EWNDOFS',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EWNDOFS',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EWNDOFS',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EWNDOFS',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EWNDOFS',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2035,'EWNDON', 2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EWNDON', 2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EWNDON', 2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EWNDON', 2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2035,'EWNDOFS',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EWNDOFS',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EWNDOFS',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EWNDOFS',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2040,'EWNDON', 2040,12.117,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EWNDON', 2040,12.117,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EWNDON', 2040,12.117,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2040,'EWNDOFS',2040,12.117,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EWNDOFS',2040,12.117,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EWNDOFS',2040,12.117,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2045,'EWNDON', 2045,12.402,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EWNDON', 2045,12.402,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2045,'EWNDOFS',2045,12.402,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EWNDOFS',2045,12.402,'M$/PJ','# MARKAL 2014 v1.1');

INSERT INTO "CostVariable" VALUES(2050,'EWNDON', 2050,12.654,'M$/PJ','# MARKAL 2014 v1.1');
INSERT INTO "CostVariable" VALUES(2050,'EWNDOFS',2050,12.654,'M$/PJ','# MARKAL 2014 v1.1');

-- Gulf Stream Energy
   INSERT INTO "CostVariable" VALUES(2015,'EHYDGS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2020,'EHYDGS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'EHYDGS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'EHYDGS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'EHYDGS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'EHYDGS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2045,'EHYDGS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'EHYDGS',2015,10.328,'M$/PJ','# MARKAL 2014 v1.1');

   INSERT INTO "CostVariable" VALUES(2020,'EHYDGS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2025,'EHYDGS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'EHYDGS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'EHYDGS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'EHYDGS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2045,'EHYDGS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
-- INSERT INTO "CostVariable" VALUES(2050,'EHYDGS',2020,11.124,'M$/PJ','# MARKAL 2014 v1.1');
   
   INSERT INTO "CostVariable" VALUES(2025,'EHYDGS',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2030,'EHYDGS',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'EHYDGS',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'EHYDGS',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2045,'EHYDGS',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2050,'EHYDGS',2025,11.400,'M$/PJ','# MARKAL 2014 v1.1');
   
   INSERT INTO "CostVariable" VALUES(2030,'EHYDGS',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2035,'EHYDGS',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'EHYDGS',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2045,'EHYDGS',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2050,'EHYDGS',2030,11.666,'M$/PJ','# MARKAL 2014 v1.1');
   
   INSERT INTO "CostVariable" VALUES(2035,'EHYDGS',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2040,'EHYDGS',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2045,'EHYDGS',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2050,'EHYDGS',2035,11.930,'M$/PJ','# MARKAL 2014 v1.1');
   
   INSERT INTO "CostVariable" VALUES(2040,'EHYDGS',2040,12.117,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2045,'EHYDGS',2040,12.117,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2050,'EHYDGS',2040,12.117,'M$/PJ','# MARKAL 2014 v1.1');
   
   INSERT INTO "CostVariable" VALUES(2045,'EHYDGS',2045,12.402,'M$/PJ','# MARKAL 2014 v1.1');
   INSERT INTO "CostVariable" VALUES(2050,'EHYDGS',2045,12.402,'M$/PJ','# MARKAL 2014 v1.1');
   
   INSERT INTO "CostVariable" VALUES(2050,'EHYDGS',2050,12.654,'M$/PJ','# MARKAL 2014 v1.1');

-- Importing coal-----------------
-- Coal importing tech after using Samaneh's naming convention
-- High Oil scenario in AEO2015
-- INSERT INTO "CostVariable" VALUES(2015,'IMPELCCOAB',    2015,2.32,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices');   
-- INSERT INTO "CostVariable" VALUES(2020,'IMPELCCOAB',    2015,2.45,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices');   
-- INSERT INTO "CostVariable" VALUES(2025,'IMPELCCOAB',    2015,2.65,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices');   
-- INSERT INTO "CostVariable" VALUES(2030,'IMPELCCOAB',    2015,2.85,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices');   
-- INSERT INTO "CostVariable" VALUES(2035,'IMPELCCOAB',    2015,3.00,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices');   
-- INSERT INTO "CostVariable" VALUES(2040,'IMPELCCOAB',    2015,3.17,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices');   
-- INSERT INTO "CostVariable" VALUES(2045,'IMPELCCOAB',    2015,3.35,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');   
-- INSERT INTO "CostVariable" VALUES(2050,'IMPELCCOAB',    2015,3.53,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');   

-- High resource scenario in AEO2015
-- INSERT INTO "CostVariable" VALUES(2015,'IMPELCCOAB',    2015,2.14,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices');   
-- INSERT INTO "CostVariable" VALUES(2020,'IMPELCCOAB',    2015,2.15,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices');   
-- INSERT INTO "CostVariable" VALUES(2025,'IMPELCCOAB',    2015,2.27,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices');   
-- INSERT INTO "CostVariable" VALUES(2030,'IMPELCCOAB',    2015,2.35,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices');   
-- INSERT INTO "CostVariable" VALUES(2035,'IMPELCCOAB',    2015,2.44,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices');   
-- INSERT INTO "CostVariable" VALUES(2040,'IMPELCCOAB',    2015,2.57,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices');   
-- INSERT INTO "CostVariable" VALUES(2045,'IMPELCCOAB',    2015,2.63,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');   
-- INSERT INTO "CostVariable" VALUES(2050,'IMPELCCOAB',    2015,2.71,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');   

-- Reference scenario in AEO2015
   INSERT INTO "CostVariable" VALUES(2015,'IMPELCCOAB',    2015,2.17,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices');   
   INSERT INTO "CostVariable" VALUES(2020,'IMPELCCOAB',    2015,2.29,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices');   
   INSERT INTO "CostVariable" VALUES(2025,'IMPELCCOAB',    2015,2.44,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices');   
   INSERT INTO "CostVariable" VALUES(2030,'IMPELCCOAB',    2015,2.57,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices');   
   INSERT INTO "CostVariable" VALUES(2035,'IMPELCCOAB',    2015,2.68,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices');   
   INSERT INTO "CostVariable" VALUES(2040,'IMPELCCOAB',    2015,2.81,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices');   
   INSERT INTO "CostVariable" VALUES(2045,'IMPELCCOAB',    2015,2.94,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');   
   INSERT INTO "CostVariable" VALUES(2050,'IMPELCCOAB',    2015,3.07,'#M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');   

-- Importing natural gas-----------------
-- High Oil scenario in AEO2015
-- INSERT INTO "CostVariable" VALUES(2015,'IMPELCNGCEA',2015, 4.11, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2020,'IMPELCNGCEA',2015, 4.92, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2025,'IMPELCNGCEA',2015, 7.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2030,'IMPELCNGCEA',2015, 7.59, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2035,'IMPELCNGCEA',2015, 8.16, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2040,'IMPELCNGCEA',2015, 9.69, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2045,'IMPELCNGCEA',2015,10.75, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');
-- INSERT INTO "CostVariable" VALUES(2050,'IMPELCNGCEA',2015,11.83, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');
-- 
-- INSERT INTO "CostVariable" VALUES(2015,'IMPELCNGAEA',2015, 4.11,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2020,'IMPELCNGAEA',2015, 4.92,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2025,'IMPELCNGAEA',2015, 7.21,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2030,'IMPELCNGAEA',2015, 7.59,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2035,'IMPELCNGAEA',2015, 8.16,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2040,'IMPELCNGAEA',2015, 9.69,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2045,'IMPELCNGAEA',2015,10.75,'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');
-- INSERT INTO "CostVariable" VALUES(2050,'IMPELCNGAEA',2015,11.83,'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');

-- High resource scenario in AEO2015
-- INSERT INTO "CostVariable" VALUES(2015,'IMPELCNGCEA',2015,3.97, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2020,'IMPELCNGCEA',2015,3.54, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2025,'IMPELCNGCEA',2015,3.85, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2030,'IMPELCNGCEA',2015,3.99, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2035,'IMPELCNGCEA',2015,4.27, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2040,'IMPELCNGCEA',2015,4.49, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2045,'IMPELCNGCEA',2015,4.51, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');
-- INSERT INTO "CostVariable" VALUES(2050,'IMPELCNGCEA',2015,4.65, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');
-- 
-- INSERT INTO "CostVariable" VALUES(2015,'IMPELCNGAEA',2015,3.97, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2020,'IMPELCNGAEA',2015,3.54, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2025,'IMPELCNGAEA',2015,3.85, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2030,'IMPELCNGAEA',2015,3.99, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2035,'IMPELCNGAEA',2015,4.27, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2040,'IMPELCNGAEA',2015,4.49, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2045,'IMPELCNGAEA',2015,4.51, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');
-- INSERT INTO "CostVariable" VALUES(2050,'IMPELCNGAEA',2015,4.65, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');

-- Reference scenario in AEO2015
   INSERT INTO "CostVariable" VALUES(2015,'IMPELCNGCEA',2015,4.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
   INSERT INTO "CostVariable" VALUES(2020,'IMPELCNGCEA',2015,5.18, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
   INSERT INTO "CostVariable" VALUES(2025,'IMPELCNGCEA',2015,6.03, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
   INSERT INTO "CostVariable" VALUES(2030,'IMPELCNGCEA',2015,5.98, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
   INSERT INTO "CostVariable" VALUES(2035,'IMPELCNGCEA',2015,6.71, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
   INSERT INTO "CostVariable" VALUES(2040,'IMPELCNGCEA',2015,7.96, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
   INSERT INTO "CostVariable" VALUES(2045,'IMPELCNGCEA',2015,8.34, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');
   INSERT INTO "CostVariable" VALUES(2050,'IMPELCNGCEA',2015,9.01, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');

   INSERT INTO "CostVariable" VALUES(2015,'IMPELCNGAEA',2015,4.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
   INSERT INTO "CostVariable" VALUES(2020,'IMPELCNGAEA',2015,5.18, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
   INSERT INTO "CostVariable" VALUES(2025,'IMPELCNGAEA',2015,6.03, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
   INSERT INTO "CostVariable" VALUES(2030,'IMPELCNGAEA',2015,5.98, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
   INSERT INTO "CostVariable" VALUES(2035,'IMPELCNGAEA',2015,6.71, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
   INSERT INTO "CostVariable" VALUES(2040,'IMPELCNGAEA',2015,7.96, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
   INSERT INTO "CostVariable" VALUES(2045,'IMPELCNGAEA',2015,8.34, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');
   INSERT INTO "CostVariable" VALUES(2050,'IMPELCNGAEA',2015,9.01, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');

-- Test for low NG prices
-- INSERT INTO "CostVariable" VALUES(2015,'IMPELCNGCEA',2015,3.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2020,'IMPELCNGCEA',2015,2.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2025,'IMPELCNGCEA',2015,2.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2030,'IMPELCNGCEA',2015,2.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2035,'IMPELCNGCEA',2015,2.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2040,'IMPELCNGCEA',2015,2.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2045,'IMPELCNGCEA',2015,2.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');
-- INSERT INTO "CostVariable" VALUES(2050,'IMPELCNGCEA',2015,2.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');

-- INSERT INTO "CostVariable" VALUES(2015,'IMPELCNGAEA',2015,3.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2020,'IMPELCNGAEA',2015,2.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2025,'IMPELCNGAEA',2015,2.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2030,'IMPELCNGAEA',2015,2.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2035,'IMPELCNGAEA',2015,2.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2040,'IMPELCNGAEA',2015,2.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2045,'IMPELCNGAEA',2015,2.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');
-- INSERT INTO "CostVariable" VALUES(2050,'IMPELCNGAEA',2015,2.21, 'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');

-- Importing oils-----------------
-- High oil scenario in AEO2015
-- INSERT INTO "CostVariable" VALUES(2015,'IMPELCDSLEA',2015,25.44,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2020,'IMPELCDSLEA',2015,30.61,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2025,'IMPELCDSLEA',2015,34.58,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2030,'IMPELCDSLEA',2015,39.03,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2035,'IMPELCDSLEA',2015,43.69,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2040,'IMPELCDSLEA',2015,49.04,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2045,'IMPELCDSLEA',2015,53.23,'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');
-- INSERT INTO "CostVariable" VALUES(2050,'IMPELCDSLEA',2015,57.85,'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');

-- High resource scenario in AEO2015
-- INSERT INTO "CostVariable" VALUES(2015,'IMPELCDSLEA',2015,14.07,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2020,'IMPELCDSLEA',2015,17.39,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2025,'IMPELCDSLEA',2015,19.12,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2030,'IMPELCDSLEA',2015,21.26,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2035,'IMPELCDSLEA',2015,24.22,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2040,'IMPELCDSLEA',2015,27.60,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
-- INSERT INTO "CostVariable" VALUES(2045,'IMPELCDSLEA',2015,29.64,'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');
-- INSERT INTO "CostVariable" VALUES(2050,'IMPELCDSLEA',2015,32.21,'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');

-- Reference scenario in AEO2015
   INSERT INTO "CostVariable" VALUES(2015,'IMPELCDSLEA',2015,15.96,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
   INSERT INTO "CostVariable" VALUES(2020,'IMPELCDSLEA',2015,18.05,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
   INSERT INTO "CostVariable" VALUES(2025,'IMPELCDSLEA',2015,20.12,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
   INSERT INTO "CostVariable" VALUES(2030,'IMPELCDSLEA',2015,22.72,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
   INSERT INTO "CostVariable" VALUES(2035,'IMPELCDSLEA',2015,25.68,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
   INSERT INTO "CostVariable" VALUES(2040,'IMPELCDSLEA',2015,29.05,'M$/PJ','AEO2015 Tab 3, national electric fuel prices');
   INSERT INTO "CostVariable" VALUES(2045,'IMPELCDSLEA',2015,31.02,'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');
   INSERT INTO "CostVariable" VALUES(2050,'IMPELCDSLEA',2015,33.62,'M$/PJ','AEO2015 Tab 3, national electric fuel prices, fitted');

-- Importing uranium
INSERT INTO "CostVariable" VALUES(2015,'IMPURNA',2015,0.13,'M$/ton','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2020,'IMPURNA',2015,0.13,'M$/ton','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2025,'IMPURNA',2015,0.13,'M$/ton','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2030,'IMPURNA',2015,0.13,'M$/ton','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2035,'IMPURNA',2015,0.13,'M$/ton','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2040,'IMPURNA',2015,0.13,'M$/ton','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2045,'IMPURNA',2015,0.13,'M$/ton','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2050,'IMPURNA',2015,0.13,'M$/ton','# From Samaneh NUSTD');

-- Importing biogass
INSERT INTO "CostVariable" VALUES(2015,'IMPELCBIGCCEA',2015,3.39,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2020,'IMPELCBIGCCEA',2015,3.39,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2025,'IMPELCBIGCCEA',2015,3.39,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2030,'IMPELCBIGCCEA',2015,3.39,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2035,'IMPELCBIGCCEA',2015,3.39,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2040,'IMPELCBIGCCEA',2015,3.39,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2045,'IMPELCBIGCCEA',2015,3.39,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2050,'IMPELCBIGCCEA',2015,3.39,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2015,'IMPELCBIOSTM', 2015,3.39,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2020,'IMPELCBIOSTM', 2015,3.39,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2025,'IMPELCBIOSTM', 2015,3.39,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2030,'IMPELCBIOSTM', 2015,3.39,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2035,'IMPELCBIOSTM', 2015,3.39,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2040,'IMPELCBIOSTM', 2015,3.39,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2045,'IMPELCBIOSTM', 2015,3.39,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2050,'IMPELCBIOSTM', 2015,3.39,'M$/PJ','# From Samaneh NUSTD');

-- Importing geo
INSERT INTO "CostVariable" VALUES(2015,'IMPELCGEO',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2020,'IMPELCGEO',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2025,'IMPELCGEO',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2030,'IMPELCGEO',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2035,'IMPELCGEO',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2040,'IMPELCGEO',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2045,'IMPELCGEO',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2050,'IMPELCGEO',2015,0,'M$/PJ','# From Samaneh NUSTD');

-- Importing solar
INSERT INTO "CostVariable" VALUES(2015,'IMPSOL',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2020,'IMPSOL',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2025,'IMPSOL',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2030,'IMPSOL',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2035,'IMPSOL',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2040,'IMPSOL',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2045,'IMPSOL',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2050,'IMPSOL',2015,0,'M$/PJ','# From Samaneh NUSTD');

-- Importing wind
INSERT INTO "CostVariable" VALUES(2015,'IMPWND',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2020,'IMPWND',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2025,'IMPWND',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2030,'IMPWND',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2035,'IMPWND',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2040,'IMPWND',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2045,'IMPWND',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2050,'IMPWND',2015,0,'M$/PJ','# From Samaneh NUSTD');

-- Importing hydro
INSERT INTO "CostVariable" VALUES(2015,'IMPELCHYD',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2020,'IMPELCHYD',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2025,'IMPELCHYD',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2030,'IMPELCHYD',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2035,'IMPELCHYD',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2040,'IMPELCHYD',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2045,'IMPELCHYD',2015,0,'M$/PJ','# From Samaneh NUSTD');
INSERT INTO "CostVariable" VALUES(2050,'IMPELCHYD',2015,0,'M$/PJ','# From Samaneh NUSTD');

--Importing landfill gas
-- Note that only direct-use of LFG requires payment for "importing" LFG,
-- therefore importing LFG is supposed to be 0.
-- See LFG Energy Project Development Handbook
-- http://www.epa.gov/lmop/documents/pdfs/pdf_full.pdf

INSERT INTO "CostVariable" VALUES(2015,'IMPLFGICEEA',2015,0,'M$/PJ','# ');
INSERT INTO "CostVariable" VALUES(2020,'IMPLFGICEEA',2015,0,'M$/PJ','# ');
INSERT INTO "CostVariable" VALUES(2025,'IMPLFGICEEA',2015,0,'M$/PJ','# ');
INSERT INTO "CostVariable" VALUES(2030,'IMPLFGICEEA',2015,0,'M$/PJ','# ');
INSERT INTO "CostVariable" VALUES(2035,'IMPLFGICEEA',2015,0,'M$/PJ','# ');
INSERT INTO "CostVariable" VALUES(2040,'IMPLFGICEEA',2015,0,'M$/PJ','# ');
INSERT INTO "CostVariable" VALUES(2045,'IMPLFGICEEA',2015,0,'M$/PJ','# ');
INSERT INTO "CostVariable" VALUES(2050,'IMPLFGICEEA',2015,0,'M$/PJ','# ');

INSERT INTO "CostVariable" VALUES(2015,'IMPLFGGTREA',2015,0,'M$/PJ','# ');
INSERT INTO "CostVariable" VALUES(2020,'IMPLFGGTREA',2015,0,'M$/PJ','# ');
INSERT INTO "CostVariable" VALUES(2025,'IMPLFGGTREA',2015,0,'M$/PJ','# ');
INSERT INTO "CostVariable" VALUES(2030,'IMPLFGGTREA',2015,0,'M$/PJ','# ');
INSERT INTO "CostVariable" VALUES(2035,'IMPLFGGTREA',2015,0,'M$/PJ','# ');
INSERT INTO "CostVariable" VALUES(2040,'IMPLFGGTREA',2015,0,'M$/PJ','# ');
INSERT INTO "CostVariable" VALUES(2045,'IMPLFGGTREA',2015,0,'M$/PJ','# ');
INSERT INTO "CostVariable" VALUES(2050,'IMPLFGGTREA',2015,0,'M$/PJ','# ');

-- Dummy electricity to electricity demand
-- Note that if all cost variable that is not inputted are 0.
INSERT INTO "CostVariable" VALUES(2015,'ELC2DMD',2015,0,'M$/PJ','');

-- Emission Control technologies
-- Existing Low NOx Burner + SNCR
INSERT INTO "CostVariable" VALUES(2015,'E_LNBSNCR_COAB_R',        2010,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_LNBSNCR_COAB_R',        2010,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_LNBSNCR_COAB_R',        2010,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_LNBSNCR_COAB_R',        2010,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_LNBSNCR_COAB_R',        2010,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_LNBSNCR_COAB_R',        2010,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNBSNCR_COAB_R',        2010,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNBSNCR_COAB_R',        2010,0.049,'#M$/PJ','');

-- New Low NOx burner + SNCR
INSERT INTO "CostVariable" VALUES(2015,'E_LNBSNCR_COAB_N',        2015,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_LNBSNCR_COAB_N',        2015,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_LNBSNCR_COAB_N',        2015,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_LNBSNCR_COAB_N',        2015,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_LNBSNCR_COAB_N',        2015,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_LNBSNCR_COAB_N',        2015,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNBSNCR_COAB_N',        2015,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNBSNCR_COAB_N',        2015,0.049,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2020,'E_LNBSNCR_COAB_N',        2020,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_LNBSNCR_COAB_N',        2020,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_LNBSNCR_COAB_N',        2020,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_LNBSNCR_COAB_N',        2020,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_LNBSNCR_COAB_N',        2020,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNBSNCR_COAB_N',        2020,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNBSNCR_COAB_N',        2020,0.049,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2025,'E_LNBSNCR_COAB_N',        2025,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_LNBSNCR_COAB_N',        2025,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_LNBSNCR_COAB_N',        2025,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_LNBSNCR_COAB_N',        2025,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNBSNCR_COAB_N',        2025,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNBSNCR_COAB_N',        2025,0.049,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2030,'E_LNBSNCR_COAB_N',        2030,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_LNBSNCR_COAB_N',        2030,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_LNBSNCR_COAB_N',        2030,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNBSNCR_COAB_N',        2030,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNBSNCR_COAB_N',        2030,0.049,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2035,'E_LNBSNCR_COAB_N',        2035,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_LNBSNCR_COAB_N',        2035,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNBSNCR_COAB_N',        2035,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNBSNCR_COAB_N',        2035,0.049,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2040,'E_LNBSNCR_COAB_N',        2040,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNBSNCR_COAB_N',        2040,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNBSNCR_COAB_N',        2040,0.049,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2045,'E_LNBSNCR_COAB_N',        2045,0.049,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNBSNCR_COAB_N',        2045,0.049,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2050,'E_LNBSNCR_COAB_N',        2050,0.049,'#M$/PJ','');

-- Existing Low NOx burner + SCR
INSERT INTO "CostVariable" VALUES(2015,'E_LNBSCR_COAB_R',        2010,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_LNBSCR_COAB_R',        2010,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_LNBSCR_COAB_R',        2010,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_LNBSCR_COAB_R',        2010,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_LNBSCR_COAB_R',        2010,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_LNBSCR_COAB_R',        2010,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNBSCR_COAB_R',        2010,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNBSCR_COAB_R',        2010,0.11,'#M$/PJ','');

-- Future LNB + SCR
INSERT INTO "CostVariable" VALUES(2015,'E_LNBSCR_COAB_N',        2015,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_LNBSCR_COAB_N',        2015,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_LNBSCR_COAB_N',        2015,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_LNBSCR_COAB_N',        2015,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_LNBSCR_COAB_N',        2015,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_LNBSCR_COAB_N',        2015,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNBSCR_COAB_N',        2015,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNBSCR_COAB_N',        2015,0.11,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2020,'E_LNBSCR_COAB_N',        2020,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_LNBSCR_COAB_N',        2020,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_LNBSCR_COAB_N',        2020,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_LNBSCR_COAB_N',        2020,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_LNBSCR_COAB_N',        2020,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNBSCR_COAB_N',        2020,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNBSCR_COAB_N',        2020,0.11,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2025,'E_LNBSCR_COAB_N',        2025,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_LNBSCR_COAB_N',        2025,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_LNBSCR_COAB_N',        2025,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_LNBSCR_COAB_N',        2025,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNBSCR_COAB_N',        2025,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNBSCR_COAB_N',        2025,0.11,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2030,'E_LNBSCR_COAB_N',        2030,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_LNBSCR_COAB_N',        2030,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_LNBSCR_COAB_N',        2030,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNBSCR_COAB_N',        2030,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNBSCR_COAB_N',        2030,0.11,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2035,'E_LNBSCR_COAB_N',        2035,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_LNBSCR_COAB_N',        2035,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNBSCR_COAB_N',        2035,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNBSCR_COAB_N',        2035,0.11,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2040,'E_LNBSCR_COAB_N',        2040,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNBSCR_COAB_N',        2040,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNBSCR_COAB_N',        2040,0.11,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2045,'E_LNBSCR_COAB_N',        2045,0.11,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNBSCR_COAB_N',        2045,0.11,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2050,'E_LNBSCR_COAB_N',        2050,0.11,'#M$/PJ','');

-- Existing SNCR
INSERT INTO "CostVariable" VALUES(2015,'E_SNCR_COAB_R',        2010,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_SNCR_COAB_R',        2010,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_SNCR_COAB_R',        2010,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_SNCR_COAB_R',        2010,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_SNCR_COAB_R',        2010,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_SNCR_COAB_R',        2010,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_SNCR_COAB_R',        2010,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_SNCR_COAB_R',        2010,0.045,'#M$/PJ','');

-- Future SNCR
INSERT INTO "CostVariable" VALUES(2015,'E_SNCR_COAB_N',        2015,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_SNCR_COAB_N',        2015,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_SNCR_COAB_N',        2015,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_SNCR_COAB_N',        2015,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_SNCR_COAB_N',        2015,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_SNCR_COAB_N',        2015,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_SNCR_COAB_N',        2015,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_SNCR_COAB_N',        2015,0.045,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2020,'E_SNCR_COAB_N',        2020,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_SNCR_COAB_N',        2020,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_SNCR_COAB_N',        2020,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_SNCR_COAB_N',        2020,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_SNCR_COAB_N',        2020,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_SNCR_COAB_N',        2020,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_SNCR_COAB_N',        2020,0.045,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2025,'E_SNCR_COAB_N',        2025,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_SNCR_COAB_N',        2025,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_SNCR_COAB_N',        2025,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_SNCR_COAB_N',        2025,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_SNCR_COAB_N',        2025,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_SNCR_COAB_N',        2025,0.045,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2030,'E_SNCR_COAB_N',        2030,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_SNCR_COAB_N',        2030,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_SNCR_COAB_N',        2030,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_SNCR_COAB_N',        2030,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_SNCR_COAB_N',        2030,0.045,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2035,'E_SNCR_COAB_N',        2035,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_SNCR_COAB_N',        2035,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_SNCR_COAB_N',        2035,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_SNCR_COAB_N',        2035,0.045,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2040,'E_SNCR_COAB_N',        2040,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_SNCR_COAB_N',        2040,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_SNCR_COAB_N',        2040,0.045,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2045,'E_SNCR_COAB_N',        2045,0.045,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_SNCR_COAB_N',        2045,0.045,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2050,'E_SNCR_COAB_N',        2050,0.045,'#M$/PJ','');

-- Existing SCR
-- INSERT INTO "CostVariable" VALUES(2015,'E_SCR_COAB_R',        2010,0.15,'#M$/PJ',''); 
-- INSERT INTO "CostVariable" VALUES(2020,'E_SCR_COAB_R',        2010,0.15,'#M$/PJ',''); 
-- INSERT INTO "CostVariable" VALUES(2025,'E_SCR_COAB_R',        2010,0.15,'#M$/PJ',''); 
-- INSERT INTO "CostVariable" VALUES(2030,'E_SCR_COAB_R',        2010,0.15,'#M$/PJ',''); 
-- INSERT INTO "CostVariable" VALUES(2035,'E_SCR_COAB_R',        2010,0.15,'#M$/PJ',''); 
-- INSERT INTO "CostVariable" VALUES(2040,'E_SCR_COAB_R',        2010,0.15,'#M$/PJ',''); 
-- INSERT INTO "CostVariable" VALUES(2045,'E_SCR_COAB_R',        2010,0.15,'#M$/PJ',''); 
-- INSERT INTO "CostVariable" VALUES(2050,'E_SCR_COAB_R',        2010,0.15,'#M$/PJ','');

-- Future SCR
INSERT INTO "CostVariable" VALUES(2015,'E_SCR_COAB_N',        2015,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_SCR_COAB_N',        2015,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_SCR_COAB_N',        2015,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_SCR_COAB_N',        2015,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_SCR_COAB_N',        2015,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_SCR_COAB_N',        2015,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_SCR_COAB_N',        2015,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_SCR_COAB_N',        2015,0.15,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2020,'E_SCR_COAB_N',        2020,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_SCR_COAB_N',        2020,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_SCR_COAB_N',        2020,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_SCR_COAB_N',        2020,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_SCR_COAB_N',        2020,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_SCR_COAB_N',        2020,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_SCR_COAB_N',        2020,0.15,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2025,'E_SCR_COAB_N',        2025,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_SCR_COAB_N',        2025,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_SCR_COAB_N',        2025,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_SCR_COAB_N',        2025,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_SCR_COAB_N',        2025,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_SCR_COAB_N',        2025,0.15,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2030,'E_SCR_COAB_N',        2030,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_SCR_COAB_N',        2030,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_SCR_COAB_N',        2030,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_SCR_COAB_N',        2030,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_SCR_COAB_N',        2030,0.15,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2035,'E_SCR_COAB_N',        2035,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_SCR_COAB_N',        2035,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_SCR_COAB_N',        2035,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_SCR_COAB_N',        2035,0.15,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2040,'E_SCR_COAB_N',        2040,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_SCR_COAB_N',        2040,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_SCR_COAB_N',        2040,0.15,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2045,'E_SCR_COAB_N',        2045,0.15,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_SCR_COAB_N',        2045,0.15,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2050,'E_SCR_COAB_N',        2050,0.15,'#M$/PJ','');

-- Existing LNB 
INSERT INTO "CostVariable" VALUES(2015,'E_LNB_COAB_R',        2010,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_LNB_COAB_R',        2010,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_LNB_COAB_R',        2010,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_LNB_COAB_R',        2010,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_LNB_COAB_R',        2010,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_LNB_COAB_R',        2010,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNB_COAB_R',        2010,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNB_COAB_R',        2010,0.006,'#M$/PJ','');

-- Future LNB
INSERT INTO "CostVariable" VALUES(2015,'E_LNB_COAB_N',        2015,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_LNB_COAB_N',        2015,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_LNB_COAB_N',        2015,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_LNB_COAB_N',        2015,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_LNB_COAB_N',        2015,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_LNB_COAB_N',        2015,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNB_COAB_N',        2015,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNB_COAB_N',        2015,0.006,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2020,'E_LNB_COAB_N',        2020,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_LNB_COAB_N',        2020,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_LNB_COAB_N',        2020,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_LNB_COAB_N',        2020,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_LNB_COAB_N',        2020,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNB_COAB_N',        2020,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNB_COAB_N',        2020,0.006,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2025,'E_LNB_COAB_N',        2025,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_LNB_COAB_N',        2025,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_LNB_COAB_N',        2025,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_LNB_COAB_N',        2025,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNB_COAB_N',        2025,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNB_COAB_N',        2025,0.006,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2030,'E_LNB_COAB_N',        2030,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_LNB_COAB_N',        2030,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_LNB_COAB_N',        2030,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNB_COAB_N',        2030,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNB_COAB_N',        2030,0.006,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2035,'E_LNB_COAB_N',        2035,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_LNB_COAB_N',        2035,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNB_COAB_N',        2035,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNB_COAB_N',        2035,0.006,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2040,'E_LNB_COAB_N',        2040,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_LNB_COAB_N',        2040,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNB_COAB_N',        2040,0.006,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2045,'E_LNB_COAB_N',        2045,0.006,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_LNB_COAB_N',        2045,0.006,'#M$/PJ','');

INSERT INTO "CostVariable" VALUES(2050,'E_LNB_COAB_N',        2050,0.006,'#M$/PJ','');

-- CO2 emission control for existing coal
INSERT INTO "CostVariable" VALUES(2015,'E_CCR_COAB',        2015,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_CCR_COAB',        2015,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_CCR_COAB',        2015,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_CCR_COAB',        2015,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_CCR_COAB',        2015,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_CCR_COAB',        2015,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COAB',        2015,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COAB',        2015,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_CCR_COAB',        2020,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_CCR_COAB',        2020,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_CCR_COAB',        2020,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_CCR_COAB',        2020,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_CCR_COAB',        2020,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COAB',        2020,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COAB',        2020,0.894,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2025,'E_CCR_COAB',        2025,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_CCR_COAB',        2025,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_CCR_COAB',        2025,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_CCR_COAB',        2025,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COAB',        2025,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COAB',        2025,0.894,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2030,'E_CCR_COAB',        2030,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_CCR_COAB',        2030,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_CCR_COAB',        2030,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COAB',        2030,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COAB',        2030,0.894,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2035,'E_CCR_COAB',        2035,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_CCR_COAB',        2035,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COAB',        2035,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COAB',        2035,0.894,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2040,'E_CCR_COAB',        2040,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COAB',        2040,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COAB',        2040,0.894,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COAB',        2045,0.894,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COAB',        2045,0.894,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COAB',        2050,0.894,'#M$/PJ','');

-- Existing SO2 control for existing high sulfur coal
-- INSERT INTO "CostVariable" VALUES(2015,'E_FGD_COABH_R',        2010,0.301,'#M$/PJ',''); 
-- INSERT INTO "CostVariable" VALUES(2020,'E_FGD_COABH_R',        2010,0.301,'#M$/PJ',''); 
-- INSERT INTO "CostVariable" VALUES(2025,'E_FGD_COABH_R',        2010,0.301,'#M$/PJ',''); 
-- INSERT INTO "CostVariable" VALUES(2030,'E_FGD_COABH_R',        2010,0.301,'#M$/PJ',''); 
-- INSERT INTO "CostVariable" VALUES(2035,'E_FGD_COABH_R',        2010,0.301,'#M$/PJ',''); 
-- INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABH_R',        2010,0.301,'#M$/PJ',''); 
-- INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABH_R',        2010,0.301,'#M$/PJ',''); 
-- INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABH_R',        2010,0.301,'#M$/PJ',''); 

-- Future SO emission control for high sulfur bituminous coal
INSERT INTO "CostVariable" VALUES(2015,'E_FGD_COABH_N',        2015,0.301,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2020,'E_FGD_COABH_N',        2015,0.301,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2025,'E_FGD_COABH_N',        2015,0.301,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2030,'E_FGD_COABH_N',        2015,0.301,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2035,'E_FGD_COABH_N',        2015,0.301,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABH_N',        2015,0.301,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABH_N',        2015,0.301,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABH_N',        2015,0.301,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2020,'E_FGD_COABH_N',        2020,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_FGD_COABH_N',        2020,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_FGD_COABH_N',        2020,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_FGD_COABH_N',        2020,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABH_N',        2020,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABH_N',        2020,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABH_N',        2020,0.301,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2025,'E_FGD_COABH_N',        2025,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_FGD_COABH_N',        2025,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_FGD_COABH_N',        2025,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABH_N',        2025,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABH_N',        2025,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABH_N',        2025,0.301,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2030,'E_FGD_COABH_N',        2030,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_FGD_COABH_N',        2030,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABH_N',        2030,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABH_N',        2030,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABH_N',        2030,0.301,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2035,'E_FGD_COABH_N',        2035,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABH_N',        2035,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABH_N',        2035,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABH_N',        2035,0.301,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABH_N',        2040,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABH_N',        2040,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABH_N',        2040,0.301,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABH_N',        2045,0.301,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABH_N',        2045,0.301,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABH_N',        2050,0.301,'#M$/PJ','');

-- Existing SO2 control for median bit coal
INSERT INTO "CostVariable" VALUES(2015,'E_FGD_COABM_R',        2010,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_FGD_COABM_R',        2010,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_FGD_COABM_R',        2010,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_FGD_COABM_R',        2010,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_FGD_COABM_R',        2010,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABM_R',        2010,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABM_R',        2010,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABM_R',        2010,0.218,'#M$/PJ',''); 

-- Future SO2 control for median sulfur bituminous coal
INSERT INTO "CostVariable" VALUES(2015,'E_FGD_COABM_N',        2015,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_FGD_COABM_N',        2015,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_FGD_COABM_N',        2015,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_FGD_COABM_N',        2015,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_FGD_COABM_N',        2015,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABM_N',        2015,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABM_N',        2015,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABM_N',        2015,0.218,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2020,'E_FGD_COABM_N',        2020,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_FGD_COABM_N',        2020,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_FGD_COABM_N',        2020,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_FGD_COABM_N',        2020,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABM_N',        2020,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABM_N',        2020,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABM_N',        2020,0.218,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2025,'E_FGD_COABM_N',        2025,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_FGD_COABM_N',        2025,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_FGD_COABM_N',        2025,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABM_N',        2025,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABM_N',        2025,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABM_N',        2025,0.218,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2030,'E_FGD_COABM_N',        2030,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_FGD_COABM_N',        2030,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABM_N',        2030,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABM_N',        2030,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABM_N',        2030,0.218,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2035,'E_FGD_COABM_N',        2035,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABM_N',        2035,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABM_N',        2035,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABM_N',        2035,0.218,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABM_N',        2040,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABM_N',        2040,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABM_N',        2040,0.218,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABM_N',        2045,0.218,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABM_N',        2045,0.218,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABM_N',        2050,0.218,'#M$/PJ','');

-- Existing SO2 control for low sulfur bit coal
INSERT INTO "CostVariable" VALUES(2015,'E_FGD_COABL_R',        2010,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_FGD_COABL_R',        2010,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_FGD_COABL_R',        2010,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_FGD_COABL_R',        2010,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_FGD_COABL_R',        2010,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABL_R',        2010,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABL_R',        2010,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABL_R',        2010,0.35,'#M$/PJ',''); 

-- Future SO2 control for low sulfur bit coal
INSERT INTO "CostVariable" VALUES(2015,'E_FGD_COABL_N',        2015,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_FGD_COABL_N',        2015,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_FGD_COABL_N',        2015,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_FGD_COABL_N',        2015,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_FGD_COABL_N',        2015,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABL_N',        2015,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABL_N',        2015,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABL_N',        2015,0.35,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2020,'E_FGD_COABL_N',        2020,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_FGD_COABL_N',        2020,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_FGD_COABL_N',        2020,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_FGD_COABL_N',        2020,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABL_N',        2020,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABL_N',        2020,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABL_N',        2020,0.35,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2025,'E_FGD_COABL_N',        2025,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_FGD_COABL_N',        2025,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_FGD_COABL_N',        2025,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABL_N',        2025,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABL_N',        2025,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABL_N',        2025,0.35,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2030,'E_FGD_COABL_N',        2030,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_FGD_COABL_N',        2030,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABL_N',        2030,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABL_N',        2030,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABL_N',        2030,0.35,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2035,'E_FGD_COABL_N',        2035,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABL_N',        2035,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABL_N',        2035,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABL_N',        2035,0.35,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2040,'E_FGD_COABL_N',        2040,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABL_N',        2040,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABL_N',        2040,0.35,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2045,'E_FGD_COABL_N',        2045,0.35,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABL_N',        2045,0.35,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2050,'E_FGD_COABL_N',        2050,0.35,'#M$/PJ','');

-- IGCC CC
INSERT INTO "CostVariable" VALUES(2015,'E_CCR_COALIGCC_N ',      2015,0.618,'#M$/PJout',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_CCR_COALIGCC_N ',      2015,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_CCR_COALIGCC_N ',      2015,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_CCR_COALIGCC_N ',      2015,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_CCR_COALIGCC_N ',      2015,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_CCR_COALIGCC_N ',      2015,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COALIGCC_N ',      2015,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COALIGCC_N ',      2015,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_CCR_COALIGCC_N ',      2020,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_CCR_COALIGCC_N ',      2020,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_CCR_COALIGCC_N ',      2020,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_CCR_COALIGCC_N ',      2020,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_CCR_COALIGCC_N ',      2020,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COALIGCC_N ',      2020,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COALIGCC_N ',      2020,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_CCR_COALIGCC_N ',      2025,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_CCR_COALIGCC_N ',      2025,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_CCR_COALIGCC_N ',      2025,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_CCR_COALIGCC_N ',      2025,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COALIGCC_N ',      2025,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COALIGCC_N ',      2025,0.618,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2030,'E_CCR_COALIGCC_N ',      2030,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_CCR_COALIGCC_N ',      2030,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_CCR_COALIGCC_N ',      2030,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COALIGCC_N ',      2030,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COALIGCC_N ',      2030,0.618,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2035,'E_CCR_COALIGCC_N ',      2035,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_CCR_COALIGCC_N ',      2035,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COALIGCC_N ',      2035,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COALIGCC_N ',      2035,0.618,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2040,'E_CCR_COALIGCC_N ',      2040,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COALIGCC_N ',      2040,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COALIGCC_N ',      2040,0.618,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COALIGCC_N ',      2045,0.618,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COALIGCC_N ',      2045,0.618,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COALIGCC_N ',      2050,0.618,'#M$/PJ',''); 

-- co2 capture retrofit tech before new coal steam plant
INSERT INTO "CostVariable" VALUES(2015,'E_CCR_COALSTM_N ',      2015,1.171,'#M$/PJout',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_CCR_COALSTM_N ',      2015,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_CCR_COALSTM_N ',      2015,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_CCR_COALSTM_N ',      2015,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_CCR_COALSTM_N ',      2015,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_CCR_COALSTM_N ',      2015,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COALSTM_N ',      2015,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COALSTM_N ',      2015,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2020,'E_CCR_COALSTM_N ',      2020,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_CCR_COALSTM_N ',      2020,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_CCR_COALSTM_N ',      2020,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_CCR_COALSTM_N ',      2020,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_CCR_COALSTM_N ',      2020,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COALSTM_N ',      2020,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COALSTM_N ',      2020,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2025,'E_CCR_COALSTM_N ',      2025,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2030,'E_CCR_COALSTM_N ',      2025,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_CCR_COALSTM_N ',      2025,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_CCR_COALSTM_N ',      2025,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COALSTM_N ',      2025,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COALSTM_N ',      2025,1.171,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2030,'E_CCR_COALSTM_N ',      2030,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2035,'E_CCR_COALSTM_N ',      2030,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_CCR_COALSTM_N ',      2030,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COALSTM_N ',      2030,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COALSTM_N ',      2030,1.171,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2035,'E_CCR_COALSTM_N ',      2035,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2040,'E_CCR_COALSTM_N ',      2035,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COALSTM_N ',      2035,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COALSTM_N ',      2035,1.171,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2040,'E_CCR_COALSTM_N ',      2040,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COALSTM_N ',      2040,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COALSTM_N ',      2040,1.171,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2045,'E_CCR_COALSTM_N ',      2045,1.171,'#M$/PJ',''); 
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COALSTM_N ',      2045,1.171,'#M$/PJ','');
INSERT INTO "CostVariable" VALUES(2050,'E_CCR_COALSTM_N ',      2050,1.171,'#M$/PJ','');

-------------------------------------------------
CREATE TABLE  LifetimeTech (
   tech text,
   life real,
   life_notes text,
   PRIMARY KEY(tech),
   FOREIGN KEY(tech) REFERENCES technologies(tech) );

-- INSERT INTO "LifetimeTech" VALUES('IMPCOALSTMCC', 1000,'');
-- INSERT INTO "LifetimeTech" VALUES('IMPCOALIGCCCC',1000,'');
-- INSERT INTO "LifetimeTech" VALUES('IMPCOALIGCC',  1000,'');
-- INSERT INTO "LifetimeTech" VALUES('IMPCOALSTMN',  1000,'');
-- INSERT INTO "LifetimeTech" VALUES('IMPCOALSTM',   1000,'');
   INSERT INTO "LifetimeTech" VALUES('IMPELCNGCEA',  1000,'');
   INSERT INTO "LifetimeTech" VALUES('IMPELCNGAEA',  1000,'');
-- INSERT INTO "LifetimeTech" VALUES('IMPELCNGSEA',  1000,'');
  INSERT INTO "LifetimeTech" VALUES('IMPELCDSLEA',  1000,'');
-- INSERT INTO "LifetimeTech" VALUES('IMPELCRFLEA',  1000,'');
   INSERT INTO "LifetimeTech" VALUES('IMPURNA',      1000,'');
   INSERT INTO "LifetimeTech" VALUES('IMPELCBIGCCEA',1000,'');
   INSERT INTO "LifetimeTech" VALUES('IMPELCBIOSTM', 1000,'');
   INSERT INTO "LifetimeTech" VALUES('IMPELCGEO',    1000,'');
   INSERT INTO "LifetimeTech" VALUES('IMPSOL',       1000,'');
   INSERT INTO "LifetimeTech" VALUES('IMPWND',       1000,'');
   INSERT INTO "LifetimeTech" VALUES('IMPELCHYD',    1000,'');
-- INSERT INTO "LifetimeTech" VALUES('IMPELCMSWEA',  1000,'');
   INSERT INTO "LifetimeTech" VALUES('IMPLFGICEEA',  1000,'');
   INSERT INTO "LifetimeTech" VALUES('IMPLFGGTREA',  1000,'');
   INSERT INTO "LifetimeTech" VALUES('IMPELCCOAB',   1000,'');	

-- INSERT INTO "LifetimeTech" VALUES('ENGACC05',     25,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('ENGACT05',     25,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('ENGAACC',      30,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('ENGAACT',      30,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('ENGACCCCS',    50,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('ENGACCR',      25,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('ENGACTR',      29,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('ENGASTMR',     10,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('ECOALSTM',     45,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('ECOALIGCC',    40,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('ECOALIGCCS',   50,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('ECOALOXYCS',   50,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('ECOASTMR',     17,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('EDSLCCR',      23,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('EDSLCTR',      16,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('ERFLSTMR',     10,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('EURNALWR',     50,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('EURNALWR15',   45,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('EBIOIGCC',     35,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('EBIOSTMR',     27,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('EGEOBCFS',     25,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('EGEOR',        26,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('ESOLPVCEN',    30,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('ESOLSTCEN',    30,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('ESOLTHR',      27,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('ESOLPVR',      31,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('EWNDR',        35,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('EWNDON',      30,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('EWNDOFS',      30,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('EWNDOFD',      30,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('EHYDCONR',     10,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('EHYDREVR',     18,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('EMSWSTMR',     29,  '# From Samaneh NUSTD');
-- INSERT INTO "LifetimeTech" VALUES('ELFGICER',     40,  '# From EPA MARKAL 2015 R5');
-- INSERT INTO "LifetimeTech" VALUES('ELFGGTR',      40,  '# From EPA MARKAL 2015 R5');

INSERT INTO "LifetimeTech" VALUES('ENGACC05',     30,  '');
INSERT INTO "LifetimeTech" VALUES('ENGACT05',     30,  '');
INSERT INTO "LifetimeTech" VALUES('ENGAACC',      30,  '');
INSERT INTO "LifetimeTech" VALUES('ENGAACT',      30,  '');
INSERT INTO "LifetimeTech" VALUES('ENGACCCCS',    30,  '');
INSERT INTO "LifetimeTech" VALUES('ENGACCR',      50,  '');
INSERT INTO "LifetimeTech" VALUES('ENGACTR',      50,  '');
-- INSERT INTO "LifetimeTech" VALUES('ENGASTMR',     50,  '');
INSERT INTO "LifetimeTech" VALUES('ECOALSTM',     50,  '');
INSERT INTO "LifetimeTech" VALUES('ECOALIGCC',    30,  '');
INSERT INTO "LifetimeTech" VALUES('ECOALIGCCS',   30,  '');
-- INSERT INTO "LifetimeTech" VALUES('ECOALOXYCS',   50,  '');
INSERT INTO "LifetimeTech" VALUES('ECOASTMR',     50,  '');
-- INSERT INTO "LifetimeTech" VALUES('EDSLCCR',      50,  '');
INSERT INTO "LifetimeTech" VALUES('EDSLCTR',      50,  '');
-- INSERT INTO "LifetimeTech" VALUES('ERFLSTMR',     50,  '');
INSERT INTO "LifetimeTech" VALUES('EURNALWR',     50,  '');
INSERT INTO "LifetimeTech" VALUES('EURNALWR15',   45,  '');
INSERT INTO "LifetimeTech" VALUES('EBIOIGCC',     30,  '');
INSERT INTO "LifetimeTech" VALUES('EBIOSTMR',     50,  '');
INSERT INTO "LifetimeTech" VALUES('EGEOBCFS',     30,  '');
-- INSERT INTO "LifetimeTech" VALUES('EGEOR',        50,  '');
INSERT INTO "LifetimeTech" VALUES('ESOLPVCEN',    30,  '');
INSERT INTO "LifetimeTech" VALUES('ESOLSTCEN',    30,  '');
-- INSERT INTO "LifetimeTech" VALUES('ESOLTHR',      50,  '');
INSERT INTO "LifetimeTech" VALUES('ESOLPVR',      50,  '');
-- INSERT INTO "LifetimeTech" VALUES('EWNDR',        50,  '');
INSERT INTO "LifetimeTech" VALUES('EWNDON',       30,  '');
INSERT INTO "LifetimeTech" VALUES('EWNDOFS',      30,  '');
-- INSERT INTO "LifetimeTech" VALUES('EWNDOFD',      30,  '');
INSERT INTO "LifetimeTech" VALUES('EHYDCONR',     50,  '');
INSERT INTO "LifetimeTech" VALUES('EHYDREVR',     50,  '');
-- INSERT INTO "LifetimeTech" VALUES('EMSWSTMR',     50,  '');
INSERT INTO "LifetimeTech" VALUES('ELFGICER',     50,  '');
INSERT INTO "LifetimeTech" VALUES('ELFGGTR',      50,  '');
INSERT INTO "LifetimeTech" VALUES('EHYDGS',       30,  '');

INSERT INTO "LifetimeTech" VALUES('ELC2DMD',      1000,'');

-- Emission control technologies
-- Group existing coal-fired steam turbine
   INSERT INTO "LifetimeTech" VALUES('E_BLND_BITSUBLIG_COALSTM_R',50,'');
   INSERT INTO "LifetimeTech" VALUES('E_BLND_BIT_COALSTM_R',      50,'');

   INSERT INTO "LifetimeTech" VALUES('E_LNBSNCR_COAB_R',           50,'');
   INSERT INTO "LifetimeTech" VALUES('E_LNBSNCR_COAB_N',           50,'');
   INSERT INTO "LifetimeTech" VALUES('E_LNBSCR_COAB_R',            50,'');
   INSERT INTO "LifetimeTech" VALUES('E_LNBSCR_COAB_N',            50,'');
   INSERT INTO "LifetimeTech" VALUES('E_PTNOXSCR_COAB',            50,'');
   INSERT INTO "LifetimeTech" VALUES('E_SNCR_COAB_R',              50,'');
   INSERT INTO "LifetimeTech" VALUES('E_SNCR_COAB_N',              50,'');
-- INSERT INTO "LifetimeTech" VALUES('E_SCR_COAB_R',               50,'');
   INSERT INTO "LifetimeTech" VALUES('E_SCR_COAB_N',               50,'');
   INSERT INTO "LifetimeTech" VALUES('E_PTNOXLNB_COAB',            50,'');
   INSERT INTO "LifetimeTech" VALUES('E_LNB_COAB_R',               50,'');
   INSERT INTO "LifetimeTech" VALUES('E_LNB_COAB_N',               50,'');
   INSERT INTO "LifetimeTech" VALUES('E_CCR_COAB',                 50,'');
   INSERT INTO "LifetimeTech" VALUES('E_PTCO2_COAB',               50,'');
-- INSERT INTO "LifetimeTech" VALUES('E_FGD_COABH_R',              50,'');
   INSERT INTO "LifetimeTech" VALUES('E_FGD_COABH_N',              50,'');
   INSERT INTO "LifetimeTech" VALUES('E_FGD_COABM_R',              50,'');
   INSERT INTO "LifetimeTech" VALUES('E_FGD_COABM_N',              50,'');
   INSERT INTO "LifetimeTech" VALUES('E_FGD_COABL_R',              50,'');
   INSERT INTO "LifetimeTech" VALUES('E_FGD_COABL_N',              50,'');
   INSERT INTO "LifetimeTech" VALUES('E_PTSO2_COABH',              50,'');
   INSERT INTO "LifetimeTech" VALUES('E_PTSO2_COABM',              50,'');
   INSERT INTO "LifetimeTech" VALUES('E_PTSO2_COABL',              50,'');
   INSERT INTO "LifetimeTech" VALUES('E_EA_COAB',                  50,'');
   INSERT INTO "LifetimeTech" VALUES('E_CCR_COALIGCC_N',           50,'');
   INSERT INTO "LifetimeTech" VALUES('E_BLND_BITSUBLIG_COALIGCC_N',50,'');
   INSERT INTO "LifetimeTech" VALUES('E_BLND_BITHML_COALIGCC_N',   50,'');
   INSERT INTO "LifetimeTech" VALUES('E_CCR_COALSTM_N',            50,'');
   INSERT INTO "LifetimeTech" VALUES('E_BLND_BITSUBLIG_COALSTM_N', 50,'');
   INSERT INTO "LifetimeTech" VALUES('E_BLND_BITHML_COALSTM_N',    50,'');


-------------------------------------------------
CREATE TABLE GlobalDiscountRate (
   rate real );
INSERT INTO "GlobalDiscountRate" VALUES(0.05);

-------------------------------------------------
CREATE TABLE Demand (
   periods integer,
   demand_comm text,
   demand real,
   demand_units text,
   demand_notes text,
   PRIMARY KEY(periods, demand_comm),
   FOREIGN KEY(periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(demand_comm) REFERENCES commodities(comm_name) );
-- AEO'15, reference scenario
INSERT INTO "Demand" VALUES(2015,'ELCDMD',453,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
INSERT INTO "Demand" VALUES(2020,'ELCDMD',474,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
INSERT INTO "Demand" VALUES(2025,'ELCDMD',495,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
INSERT INTO "Demand" VALUES(2030,'ELCDMD',517,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
INSERT INTO "Demand" VALUES(2035,'ELCDMD',540,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
INSERT INTO "Demand" VALUES(2040,'ELCDMD',564,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
INSERT INTO "Demand" VALUES(2045,'ELCDMD',590,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
INSERT INTO "Demand" VALUES(2050,'ELCDMD',616,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');

-- AEO'15, high oil scenario
-- INSERT INTO "Demand" VALUES(2015,'ELCDMD',453,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
-- INSERT INTO "Demand" VALUES(2020,'ELCDMD',475,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
-- INSERT INTO "Demand" VALUES(2025,'ELCDMD',497,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
-- INSERT INTO "Demand" VALUES(2030,'ELCDMD',521,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
-- INSERT INTO "Demand" VALUES(2035,'ELCDMD',546,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
-- INSERT INTO "Demand" VALUES(2040,'ELCDMD',572,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
-- INSERT INTO "Demand" VALUES(2045,'ELCDMD',599,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
-- INSERT INTO "Demand" VALUES(2050,'ELCDMD',627,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');

-- AEO'15, high resource scenario
-- INSERT INTO "Demand" VALUES(2015,'ELCDMD',453,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
-- INSERT INTO "Demand" VALUES(2020,'ELCDMD',480,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
-- INSERT INTO "Demand" VALUES(2025,'ELCDMD',508,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
-- INSERT INTO "Demand" VALUES(2030,'ELCDMD',539,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
-- INSERT INTO "Demand" VALUES(2035,'ELCDMD',570,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
-- INSERT INTO "Demand" VALUES(2040,'ELCDMD',604,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
-- INSERT INTO "Demand" VALUES(2045,'ELCDMD',640,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');
-- INSERT INTO "Demand" VALUES(2050,'ELCDMD',677,'PJ','# Based on EIA 2013 electricity and AEO2015 growth rate for VACAR');

-------------------------------------------------
CREATE TABLE DemandSpecificDistribution (
   season_name text,
   time_of_day_name text,
   demand_name text,
   dds real check (dds>=0 AND dds<=1),
   dds_notes text,
   PRIMARY KEY(season_name, time_of_day_name, demand_name),
   FOREIGN KEY(season_name) REFERENCES time_season(t_season),
   FOREIGN KEY(time_of_day_name) REFERENCES time_of_day(t_day), 
   FOREIGN KEY(demand_name) REFERENCES commodities(comm_name) );

-- Below is based on 4 seasons and 24 tods, but with synthetic data.
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod01', 'ELCDMD', 0.00752173,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod02', 'ELCDMD', 0.00701759,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod03', 'ELCDMD', 0.00655773,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod04', 'ELCDMD', 0.00684074,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod05', 'ELCDMD', 0.00774481,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod06', 'ELCDMD', 0.00857682,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod07', 'ELCDMD', 0.00895182,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod08', 'ELCDMD', 0.00916204,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod09', 'ELCDMD', 0.0093357,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod10', 'ELCDMD', 0.00949828,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod11', 'ELCDMD', 0.00953559,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod12', 'ELCDMD', 0.00957833,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod13', 'ELCDMD', 0.00971702,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod14', 'ELCDMD', 0.00981686,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod15', 'ELCDMD', 0.00987046,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod16', 'ELCDMD', 0.00997499,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod17', 'ELCDMD', 0.01012927,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod18', 'ELCDMD', 0.01019235,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod19', 'ELCDMD', 0.01024059,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod20', 'ELCDMD', 0.01100325,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod21', 'ELCDMD', 0.010692,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod22', 'ELCDMD', 0.00924139,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod23', 'ELCDMD', 0.00872765,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod24', 'ELCDMD', 0.0082089,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod01', 'ELCDMD', 0.00864662,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod02', 'ELCDMD', 0.00828622,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod03', 'ELCDMD', 0.00804124,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod04', 'ELCDMD', 0.00763399,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod05', 'ELCDMD', 0.00813066,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod06', 'ELCDMD', 0.00842701,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod07', 'ELCDMD', 0.00880223,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod08', 'ELCDMD', 0.00905361,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod09', 'ELCDMD', 0.01055558,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod10', 'ELCDMD', 0.01197565,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod11', 'ELCDMD', 0.01294646,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod12', 'ELCDMD', 0.01396852,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod13', 'ELCDMD', 0.01438852,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod14', 'ELCDMD', 0.01486952,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod15', 'ELCDMD', 0.0155039,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod16', 'ELCDMD', 0.01693936,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod17', 'ELCDMD', 0.01599425,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod18', 'ELCDMD', 0.01518219,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod19', 'ELCDMD', 0.0146092,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod20', 'ELCDMD', 0.01419004,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod21', 'ELCDMD', 0.01359768,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod22', 'ELCDMD', 0.01241704,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod23', 'ELCDMD', 0.01129375,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod24', 'ELCDMD', 0.00910797,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod01', 'ELCDMD', 0.00786719,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod02', 'ELCDMD', 0.00732055,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod03', 'ELCDMD', 0.0070822,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod04', 'ELCDMD', 0.00718928,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod05', 'ELCDMD', 0.00776712,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod06', 'ELCDMD', 0.00840392,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod07', 'ELCDMD', 0.00890765,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod08', 'ELCDMD', 0.0091024,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod09', 'ELCDMD', 0.0093531,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod10', 'ELCDMD', 0.0095655,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod11', 'ELCDMD', 0.00981445,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod12', 'ELCDMD', 0.00996287,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod13', 'ELCDMD', 0.01024951,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod14', 'ELCDMD', 0.01031077,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod15', 'ELCDMD', 0.01051012,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod16', 'ELCDMD', 0.01072217,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod17', 'ELCDMD', 0.01095954,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod18', 'ELCDMD', 0.01125274,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod19', 'ELCDMD', 0.01150125,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod20', 'ELCDMD', 0.01141735,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod21', 'ELCDMD', 0.01102813,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod22', 'ELCDMD', 0.00918871,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod23', 'ELCDMD', 0.00878554,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod24', 'ELCDMD', 0.00826442,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod01', 'ELCDMD', 0.00941691,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod02', 'ELCDMD', 0.00917022,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod03', 'ELCDMD', 0.00920886,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod04', 'ELCDMD', 0.00955544,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod05', 'ELCDMD', 0.0105295,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod06', 'ELCDMD', 0.01153752,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod07', 'ELCDMD', 0.01280141,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod08', 'ELCDMD', 0.01348205,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod09', 'ELCDMD', 0.01312552,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod10', 'ELCDMD', 0.01295182,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod11', 'ELCDMD', 0.01203469,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod12', 'ELCDMD', 0.01181004,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod13', 'ELCDMD', 0.01120987,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod14', 'ELCDMD', 0.0109696,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod15', 'ELCDMD', 0.01006468,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod16', 'ELCDMD', 0.00980491,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod17', 'ELCDMD', 0.01026236,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod18', 'ELCDMD', 0.01162699,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod19', 'ELCDMD', 0.01225808,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod20', 'ELCDMD', 0.01251883,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod21', 'ELCDMD', 0.01238171,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod22', 'ELCDMD', 0.01191132,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod23', 'ELCDMD', 0.01145802,'Synthetic');
-- INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod24', 'ELCDMD', 0.01068603,'Synthetic');

-- Below is based on 4 seasons and 24 tods, data from FERC-714 form 2014 Progress Energy Carolina and Duke Energy Carolina
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod01', 'ELCDMD', 0.008140453,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod02', 'ELCDMD', 0.007917775,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod03', 'ELCDMD', 0.007799703,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod04', 'ELCDMD', 0.007908279,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod05', 'ELCDMD', 0.008258673,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod06', 'ELCDMD', 0.00898754, 'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod07', 'ELCDMD', 0.009681353,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod08', 'ELCDMD', 0.009990321,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod09', 'ELCDMD', 0.010105967,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod10', 'ELCDMD', 0.01016994, 'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod11', 'ELCDMD', 0.010196859,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod12', 'ELCDMD', 0.010214277,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod13', 'ELCDMD', 0.010267287,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod14', 'ELCDMD', 0.010300377,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod15', 'ELCDMD', 0.010320859,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod16', 'ELCDMD', 0.010365628,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod17', 'ELCDMD', 0.010407013,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod18', 'ELCDMD', 0.010410876,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod19', 'ELCDMD', 0.010457521,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod20', 'ELCDMD', 0.010641003,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod21', 'ELCDMD', 0.010571599,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod22', 'ELCDMD', 0.010011619,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod23', 'ELCDMD', 0.009231357,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s001', 'tod24', 'ELCDMD', 0.00854846, 'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod01', 'ELCDMD', 0.009132218,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod02', 'ELCDMD', 0.008644488,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod03', 'ELCDMD', 0.008337325,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod04', 'ELCDMD', 0.008214549,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod05', 'ELCDMD', 0.008364664,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod06', 'ELCDMD', 0.008768997,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod07', 'ELCDMD', 0.009254017,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod08', 'ELCDMD', 0.009853086,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod09', 'ELCDMD', 0.010563281,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod10', 'ELCDMD', 0.011348708,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod11', 'ELCDMD', 0.012106452,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod12', 'ELCDMD', 0.012767678,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod13', 'ELCDMD', 0.013345217,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod14', 'ELCDMD', 0.013795212,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod15', 'ELCDMD', 0.014091862,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod16', 'ELCDMD', 0.014237208,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod17', 'ELCDMD', 0.014217454,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod18', 'ELCDMD', 0.013978819,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod19', 'ELCDMD', 0.013519447,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod20', 'ELCDMD', 0.013063369,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod21', 'ELCDMD', 0.012695895,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod22', 'ELCDMD', 0.01192614, 'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod23', 'ELCDMD', 0.010858588,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s002', 'tod24', 'ELCDMD', 0.009884448,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod01', 'ELCDMD', 0.008223495,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod02', 'ELCDMD', 0.008011903,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod03', 'ELCDMD', 0.007871959,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod04', 'ELCDMD', 0.007904132,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod05', 'ELCDMD', 0.008182299,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod06', 'ELCDMD', 0.008865078,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod07', 'ELCDMD', 0.00958991, 'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod08', 'ELCDMD', 0.009885489,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod09', 'ELCDMD', 0.010041828,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod10', 'ELCDMD', 0.010151037,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod11', 'ELCDMD', 0.010225252,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod12', 'ELCDMD', 0.010275233,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod13', 'ELCDMD', 0.01034992, 'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod14', 'ELCDMD', 0.010418804,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod15', 'ELCDMD', 0.01045216, 'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod16', 'ELCDMD', 0.010491326,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod17', 'ELCDMD', 0.010558323,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod18', 'ELCDMD', 0.010749396,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod19', 'ELCDMD', 0.010920112,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod20', 'ELCDMD', 0.010902031,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod21', 'ELCDMD', 0.010579284,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod22', 'ELCDMD', 0.00998115, 'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod23', 'ELCDMD', 0.00927657, 'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s003', 'tod24', 'ELCDMD', 0.008639808,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod01', 'ELCDMD', 0.010025008,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod02', 'ELCDMD', 0.009912994,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod03', 'ELCDMD', 0.009927608,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod04', 'ELCDMD', 0.010049123,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod05', 'ELCDMD', 0.010343093,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod06', 'ELCDMD', 0.010976074,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod07', 'ELCDMD', 0.011950521,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod08', 'ELCDMD', 0.012427454,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod09', 'ELCDMD', 0.012366374,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod10', 'ELCDMD', 0.012018808,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod11', 'ELCDMD', 0.01158736, 'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod12', 'ELCDMD', 0.011143879,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod13', 'ELCDMD', 0.010758596,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod14', 'ELCDMD', 0.010467815,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod15', 'ELCDMD', 0.010232339,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod16', 'ELCDMD', 0.010141098,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod17', 'ELCDMD', 0.010331645,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod18', 'ELCDMD', 0.01102441, 'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod19', 'ELCDMD', 0.011674998,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod20', 'ELCDMD', 0.011771322,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod21', 'ELCDMD', 0.011705184,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod22', 'ELCDMD', 0.011415911,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod23', 'ELCDMD', 0.010924691,'Slice average');
INSERT INTO "DemandSpecificDistribution" VALUES('s004', 'tod24', 'ELCDMD', 0.010403333,'Slice average');

-------------------------------------------------
CREATE TABLE ExistingCapacity (
   tech text,
   vintage integer,
   exist_cap real,
   exist_cap_units text,
   exist_cap_notes text,
   PRIMARY KEY(tech, vintage),
   FOREIGN KEY(tech) REFERENCES technologies(tech),
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods) );
   INSERT INTO "ExistingCapacity" VALUES('ENGACCR' ,1970,  0.096 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ENGACCR' ,1975,  0.096 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ENGACCR' ,1980,  0.096 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ENGACCR' ,1985,  0.096 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ENGACCR' ,1990,  0.096 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ENGACCR' ,1995,  0.096 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ENGACCR' ,2000,  0.096 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ENGACCR' ,2005,  4.031 ,'GW','# EIA860 2013');

   INSERT INTO "ExistingCapacity" VALUES('ENGACTR' ,1970,  0.014 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ENGACTR' ,1975,  0.014 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ENGACTR' ,1980,  0.014 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ENGACTR' ,1985,  0.014 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ENGACTR' ,1990,  0.014 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ENGACTR' ,1995,  0.014 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ENGACTR' ,2000,  0.014 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ENGACTR' ,2005,  5.940 ,'GW','# EIA860 2013');

-- no ENGASTMR 

-- Coal from EIA860 by using retirement pattern reported on news and Duke energy website
   INSERT INTO "ExistingCapacity" VALUES('ECOASTMR',1970,  0.376 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ECOASTMR',1975,  0.676 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ECOASTMR',1980,  0.001 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ECOASTMR',1985,  0.001 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ECOASTMR',1990,  0.001 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ECOASTMR',1995,  0.001 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ECOASTMR',2000,  0.001 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('ECOASTMR',2005,  9.743 ,'GW','# EIA860 2013');

-- no EDSLCCR

   INSERT INTO "ExistingCapacity" VALUES('EDSLCTR' ,1970,  0.014 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('EDSLCTR' ,1975,  0.014 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('EDSLCTR' ,1980,  0.014 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('EDSLCTR' ,1985,  0.014 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('EDSLCTR' ,1990,  0.014 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('EDSLCTR' ,1995,  0.014 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('EDSLCTR' ,2000,  0.014 ,'GW','# EIA860 2013');
   INSERT INTO "ExistingCapacity" VALUES('EDSLCTR' ,2005,  0.142 ,'GW','# EIA860 2013');
-- no ERFLSTMR
INSERT INTO "ExistingCapacity" VALUES('EURNALWR',2005,  5.0761,'GW','# EIA860 2013');
INSERT INTO "ExistingCapacity" VALUES('EBIOSTMR',2005,  0.5024,'GW','# EIA860 2013');
-- no EGEOR
-- no ESOLTHR
INSERT INTO "ExistingCapacity" VALUES('ESOLPVR' ,2005,  0.676, 'GW','# EIA860 2014');
-- no EWNDR
INSERT INTO "ExistingCapacity" VALUES('EHYDCONR',2005,  1.997 ,'GW','# EIA860 2013');
INSERT INTO "ExistingCapacity" VALUES('EHYDREVR',2005,  0.086 ,'GW','# EIA860 2013');
-- no EMSWSTMR
INSERT INTO "ExistingCapacity" VALUES('ELFGICER',2005,  0.0331,'GW','# EIA860 2013');
INSERT INTO "ExistingCapacity" VALUES('ELFGGTR' ,2005,  0.0154,'GW','# EIA860 2013');

-- Emission control technologies
   INSERT INTO "ExistingCapacity" VALUES('E_LNBSNCR_COAB_R',2010, 143,'#PJ','# eGrid 2010');
   INSERT INTO "ExistingCapacity" VALUES('E_LNBSCR_COAB_R', 2010, 386,'#PJ','# eGrid 2010');
   INSERT INTO "ExistingCapacity" VALUES('E_SNCR_COAB_R',   2010,   3,'#PJ','# eGrid 2010');
-- INSERT INTO "ExistingCapacity" VALUES('E_SCR_COAB_R',    2010,   0,'#PJ','# eGrid 2010');
   INSERT INTO "ExistingCapacity" VALUES('E_LNB_COAB_R',    2010,  67,'#PJ','# eGrid 2010');
-- INSERT INTO "ExistingCapacity" VALUES('E_FGD_COABH_R',   2010,   0,'#PJ','# eGrid 2010');
   INSERT INTO "ExistingCapacity" VALUES('E_FGD_COABM_R',   2010,30.5,'#PJ','# eGrid 2010');
   INSERT INTO "ExistingCapacity" VALUES('E_FGD_COABL_R',   2010, 596,'#PJ','# eGrid 2010');

-------------------------------------------------
-- Below is added due to the new database schema
CREATE TABLE DiscountRate (
   tech text,
   vintage integer,
   tech_rate real,
   tech_rate_notes text,
   PRIMARY KEY(tech, vintage),
   FOREIGN KEY(tech) REFERENCES technologies(tech),
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods));

-------------------------------------------------
CREATE TABLE EmissionActivity  (
   emis_comm text,
   input_comm text,
   tech text,
   vintage integer,
   output_comm text,
   emis_act real,
   emis_act_units text,
   emis_act_notes text,
   PRIMARY KEY(emis_comm, input_comm, tech, vintage, output_comm),
   FOREIGN KEY(emis_comm) REFERENCES commodities(comm_name), 
   FOREIGN KEY(input_comm) REFERENCES commodities(comm_name), 
   FOREIGN KEY(tech) REFERENCES technologies(tech),
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods), 
   FOREIGN KEY(output_comm) REFERENCES commodities(comm_name) );
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNBSNCR_COAB_R',2010,'COAB_R',        -0.2314,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNBSNCR_COAB_R',2010,'COAB_R',        -0.2314,'#kt/PJout','');

INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNBSNCR_COAB_N',2015,'COAB_R',        -0.2314,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNBSNCR_COAB_N',2020,'COAB_R',        -0.2314,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNBSNCR_COAB_N',2025,'COAB_R',        -0.2314,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNBSNCR_COAB_N',2030,'COAB_R',        -0.2314,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNBSNCR_COAB_N',2035,'COAB_R',        -0.2314,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNBSNCR_COAB_N',2040,'COAB_R',        -0.2314,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNBSNCR_COAB_N',2045,'COAB_R',        -0.2314,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNBSNCR_COAB_N',2050,'COAB_R',        -0.2314,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNBSNCR_COAB_N',2015,'COAB_R',        -0.2314,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNBSNCR_COAB_N',2020,'COAB_R',        -0.2314,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNBSNCR_COAB_N',2025,'COAB_R',        -0.2314,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNBSNCR_COAB_N',2030,'COAB_R',        -0.2314,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNBSNCR_COAB_N',2035,'COAB_R',        -0.2314,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNBSNCR_COAB_N',2040,'COAB_R',        -0.2314,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNBSNCR_COAB_N',2045,'COAB_R',        -0.2314,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNBSNCR_COAB_N',2050,'COAB_R',        -0.2314,'#kt/PJout','');

-- Existing LNB + SCR
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNBSCR_COAB_R',2010,'COAB_R',        -0.3004,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNBSCR_COAB_R',2010,'COAB_R',        -0.3004,'#kt/PJout','');

-- Future LNB + SCR
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNBSCR_COAB_N',2015,'COAB_R',        -0.3004,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNBSCR_COAB_N',2020,'COAB_R',        -0.3004,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNBSCR_COAB_N',2025,'COAB_R',        -0.3004,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNBSCR_COAB_N',2030,'COAB_R',        -0.3004,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNBSCR_COAB_N',2035,'COAB_R',        -0.3004,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNBSCR_COAB_N',2040,'COAB_R',        -0.3004,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNBSCR_COAB_N',2045,'COAB_R',        -0.3004,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNBSCR_COAB_N',2050,'COAB_R',        -0.3004,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNBSCR_COAB_N',2015,'COAB_R',        -0.3004,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNBSCR_COAB_N',2020,'COAB_R',        -0.3004,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNBSCR_COAB_N',2025,'COAB_R',        -0.3004,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNBSCR_COAB_N',2030,'COAB_R',        -0.3004,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNBSCR_COAB_N',2035,'COAB_R',        -0.3004,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNBSCR_COAB_N',2040,'COAB_R',        -0.3004,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNBSCR_COAB_N',2045,'COAB_R',        -0.3004,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNBSCR_COAB_N',2050,'COAB_R',        -0.3004,'#kt/PJout','');

-- Existing SNCR
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_SCR_PT','E_SNCR_COAB_R',2010,'COAB_R',        -0.1106,'#kt/PJout','');

-- Future SNCR
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_SCR_PT','E_SNCR_COAB_N',2015,'COAB_R',        -0.1106,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_SCR_PT','E_SNCR_COAB_N',2020,'COAB_R',        -0.1106,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_SCR_PT','E_SNCR_COAB_N',2025,'COAB_R',        -0.1106,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_SCR_PT','E_SNCR_COAB_N',2030,'COAB_R',        -0.1106,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_SCR_PT','E_SNCR_COAB_N',2035,'COAB_R',        -0.1106,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_SCR_PT','E_SNCR_COAB_N',2040,'COAB_R',        -0.1106,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_SCR_PT','E_SNCR_COAB_N',2045,'COAB_R',        -0.1106,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_SCR_PT','E_SNCR_COAB_N',2050,'COAB_R',        -0.1106,'#kt/PJout','');

-- Existing SCR
-- INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_SCR_PT','E_SCR_COAB_R',2010,'COAB_R',        -0.1822,'#kt/PJout','');

-- Future SCR
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_SCR_PT','E_SCR_COAB_N',2015,'COAB_R',        -0.1822,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_SCR_PT','E_SCR_COAB_N',2020,'COAB_R',        -0.1822,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_SCR_PT','E_SCR_COAB_N',2025,'COAB_R',        -0.1822,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_SCR_PT','E_SCR_COAB_N',2030,'COAB_R',        -0.1822,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_SCR_PT','E_SCR_COAB_N',2035,'COAB_R',        -0.1822,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_SCR_PT','E_SCR_COAB_N',2040,'COAB_R',        -0.1822,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_SCR_PT','E_SCR_COAB_N',2045,'COAB_R',        -0.1822,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_SCR_PT','E_SCR_COAB_N',2050,'COAB_R',        -0.1822,'#kt/PJout','');

-- Existing LNB
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNB_COAB_R',2010,'COAB_R_SCR_PT',        -0.1164,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNB_COAB_R',2010,'COAB_R_SCR_PT',        -0.1164,'#kt/PJout','');

-- Future LNB
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNB_COAB_N',2015,'COAB_R_SCR_PT',        -0.1164,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNB_COAB_N',2020,'COAB_R_SCR_PT',        -0.1164,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNB_COAB_N',2025,'COAB_R_SCR_PT',        -0.1164,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNB_COAB_N',2030,'COAB_R_SCR_PT',        -0.1164,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNB_COAB_N',2035,'COAB_R_SCR_PT',        -0.1164,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNB_COAB_N',2040,'COAB_R_SCR_PT',        -0.1164,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNB_COAB_N',2045,'COAB_R_SCR_PT',        -0.1164,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB',   'E_LNB_COAB_N',2050,'COAB_R_SCR_PT',        -0.1164,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNB_COAB_N',2015,'COAB_R_SCR_PT',        -0.1164,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNB_COAB_N',2020,'COAB_R_SCR_PT',        -0.1164,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNB_COAB_N',2025,'COAB_R_SCR_PT',        -0.1164,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNB_COAB_N',2030,'COAB_R_SCR_PT',        -0.1164,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNB_COAB_N',2035,'COAB_R_SCR_PT',        -0.1164,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNB_COAB_N',2040,'COAB_R_SCR_PT',        -0.1164,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNB_COAB_N',2045,'COAB_R_SCR_PT',        -0.1164,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_R_LNB_PT','E_LNB_COAB_N',2050,'COAB_R_SCR_PT',        -0.1164,'#kt/PJout','');

-- CO2 control for existing coal
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_R_CC','E_CCR_COAB',2015,'COAB_R_LNB',        -115.56,'#kt/PJout','#converted from PJin to PJout');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_R_CC','E_CCR_COAB',2020,'COAB_R_LNB',        -115.56,'#kt/PJout','#converted from PJin to PJout');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_R_CC','E_CCR_COAB',2025,'COAB_R_LNB',        -115.56,'#kt/PJout','#converted from PJin to PJout');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_R_CC','E_CCR_COAB',2030,'COAB_R_LNB',        -115.56,'#kt/PJout','#converted from PJin to PJout');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_R_CC','E_CCR_COAB',2035,'COAB_R_LNB',        -115.56,'#kt/PJout','#converted from PJin to PJout');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_R_CC','E_CCR_COAB',2040,'COAB_R_LNB',        -115.56,'#kt/PJout','#converted from PJin to PJout');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_R_CC','E_CCR_COAB',2045,'COAB_R_LNB',        -115.56,'#kt/PJout','#converted from PJin to PJout');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_R_CC','E_CCR_COAB',2050,'COAB_R_LNB',        -115.56,'#kt/PJout','#converted from PJin to PJout');

-- Existing SO2 control for existing high sulfur coal
-- INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABH_R','E_FGD_COABH_R',2010,'COAB_R_CC',        -1.127,'#kt/PJout','');

-- New SO2 control for high sulfur coal
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABH_R','E_FGD_COABH_N',2015,'COAB_R_CC',        -1.127,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABH_R','E_FGD_COABH_N',2020,'COAB_R_CC',        -1.127,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABH_R','E_FGD_COABH_N',2025,'COAB_R_CC',        -1.127,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABH_R','E_FGD_COABH_N',2030,'COAB_R_CC',        -1.127,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABH_R','E_FGD_COABH_N',2035,'COAB_R_CC',        -1.127,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABH_R','E_FGD_COABH_N',2040,'COAB_R_CC',        -1.127,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABH_R','E_FGD_COABH_N',2045,'COAB_R_CC',        -1.127,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABH_R','E_FGD_COABH_N',2050,'COAB_R_CC',        -1.127,'#kt/PJout','');

-- Existing SO2 control for existing median sulfur coal
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABM_R','E_FGD_COABM_R',2010,'COAB_R_CC',        -0.505,'#kt/PJout','');

-- Future SO2 control for existing median sulfur coal
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABM_R','E_FGD_COABM_N',2015,'COAB_R_CC',        -0.505,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABM_R','E_FGD_COABM_N',2020,'COAB_R_CC',        -0.505,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABM_R','E_FGD_COABM_N',2025,'COAB_R_CC',        -0.505,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABM_R','E_FGD_COABM_N',2030,'COAB_R_CC',        -0.505,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABM_R','E_FGD_COABM_N',2035,'COAB_R_CC',        -0.505,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABM_R','E_FGD_COABM_N',2040,'COAB_R_CC',        -0.505,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABM_R','E_FGD_COABM_N',2045,'COAB_R_CC',        -0.505,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABM_R','E_FGD_COABM_N',2050,'COAB_R_CC',        -0.505,'#kt/PJout','');

--Existing SO2 control for existing low sulfur coal
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABL_R','E_FGD_COABL_R',2010,'COAB_R_CC',        -0.14,'#kt/PJout','');

-- Futue SO2 control for low sulfur bit coal
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABL_R','E_FGD_COABL_N',2015,'COAB_R_CC',        -0.14,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABL_R','E_FGD_COABL_N',2020,'COAB_R_CC',        -0.14,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABL_R','E_FGD_COABL_N',2025,'COAB_R_CC',        -0.14,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABL_R','E_FGD_COABL_N',2030,'COAB_R_CC',        -0.14,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABL_R','E_FGD_COABL_N',2035,'COAB_R_CC',        -0.14,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABL_R','E_FGD_COABL_N',2040,'COAB_R_CC',        -0.14,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABL_R','E_FGD_COABL_N',2045,'COAB_R_CC',        -0.14,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COABL_R','E_FGD_COABL_N',2050,'COAB_R_CC',        -0.14,'#kt/PJout','');

-- Emission accounting for bituminous coal
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2015,'COABH_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2020,'COABH_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2025,'COABH_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2030,'COABH_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2035,'COABH_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2040,'COABH_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2045,'COABH_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2050,'COABH_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2015,'COABL_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2020,'COABL_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2025,'COABL_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2030,'COABL_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2035,'COABL_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2040,'COABL_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2045,'COABL_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2050,'COABL_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2015,'COABM_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2020,'COABM_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2025,'COABM_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2030,'COABM_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2035,'COABM_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2040,'COABM_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2045,'COABM_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2050,'COABM_R',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2015,'COABH_R',         1.186,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2020,'COABH_R',         1.186,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2025,'COABH_R',         1.186,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2030,'COABH_R',         1.186,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2035,'COABH_R',         1.186,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2040,'COABH_R',         1.186,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2045,'COABH_R',         1.186,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2050,'COABH_R',         1.186,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2015,'COABL_R',        0.1474,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2020,'COABL_R',        0.1474,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2025,'COABL_R',        0.1474,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2030,'COABL_R',        0.1474,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2035,'COABL_R',        0.1474,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2040,'COABL_R',        0.1474,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2045,'COABL_R',        0.1474,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2050,'COABL_R',        0.1474,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2015,'COABM_R',         0.526,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2020,'COABM_R',         0.526,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2025,'COABM_R',         0.526,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2030,'COABM_R',         0.526,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2035,'COABM_R',         0.526,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2040,'COABM_R',         0.526,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2045,'COABM_R',         0.526,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2050,'COABM_R',         0.526,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2015,'COABH_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2020,'COABH_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2025,'COABH_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2030,'COABH_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2035,'COABH_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2040,'COABH_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2045,'COABH_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2050,'COABH_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2015,'COABL_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2020,'COABL_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2025,'COABL_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2030,'COABL_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2035,'COABL_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2040,'COABL_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2045,'COABL_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2050,'COABL_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2015,'COABM_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2020,'COABM_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2025,'COABM_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2030,'COABM_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2035,'COABM_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2040,'COABM_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2045,'COABM_R',         0.346,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2050,'COABM_R',         0.346,'#kt/PJout','');

INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2015,'COABH_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2020,'COABH_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2025,'COABH_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2030,'COABH_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2035,'COABH_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2040,'COABH_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2045,'COABH_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2050,'COABH_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2015,'COABL_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2020,'COABL_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2025,'COABL_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2030,'COABL_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2035,'COABL_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2040,'COABL_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2045,'COABL_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2050,'COABL_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2015,'COABM_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2020,'COABM_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2025,'COABM_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2030,'COABM_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2035,'COABM_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2040,'COABM_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2045,'COABM_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2050,'COABM_N',        88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2015,'COABH_N',        0.0518,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2020,'COABH_N',        0.0518,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2025,'COABH_N',        0.0518,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2030,'COABH_N',        0.0518,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2035,'COABH_N',        0.0518,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2040,'COABH_N',        0.0518,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2045,'COABH_N',        0.0518,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2050,'COABH_N',        0.0518,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2015,'COABL_N',        0.0064,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2020,'COABL_N',        0.0064,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2025,'COABL_N',        0.0064,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2030,'COABL_N',        0.0064,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2035,'COABL_N',        0.0064,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2040,'COABL_N',        0.0064,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2045,'COABL_N',        0.0064,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2050,'COABL_N',        0.0064,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2015,'COABM_N',        0.023,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2020,'COABM_N',        0.023,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2025,'COABM_N',        0.023,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2030,'COABM_N',        0.023,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2035,'COABM_N',        0.023,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2040,'COABM_N',        0.023,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2045,'COABM_N',        0.023,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2050,'COABM_N',        0.023,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2015,'COABH_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2020,'COABH_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2025,'COABH_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2030,'COABH_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2035,'COABH_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2040,'COABH_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2045,'COABH_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2050,'COABH_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2015,'COABL_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2020,'COABL_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2025,'COABL_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2030,'COABL_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2035,'COABL_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2040,'COABL_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2045,'COABL_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2050,'COABL_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2015,'COABM_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2020,'COABM_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2025,'COABM_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2030,'COABM_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2035,'COABM_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2040,'COABM_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2045,'COABM_N',        0.0604,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2050,'COABM_N',        0.0604,'#kt/PJout','');

INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2015,'COABH_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2020,'COABH_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2025,'COABH_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2030,'COABH_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2035,'COABH_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2040,'COABH_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2045,'COABH_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2050,'COABH_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2015,'COABL_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2020,'COABL_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2025,'COABL_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2030,'COABL_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2035,'COABL_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2040,'COABL_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2045,'COABL_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2050,'COABL_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2015,'COABM_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2020,'COABM_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2025,'COABM_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2030,'COABM_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2035,'COABM_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2040,'COABM_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2045,'COABM_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COAB_EA','E_EA_COAB',2050,'COABM_IGCC_N',         88.42,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2015,'COABH_IGCC_N',        0.0096,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2020,'COABH_IGCC_N',        0.0096,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2025,'COABH_IGCC_N',        0.0096,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2030,'COABH_IGCC_N',        0.0096,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2035,'COABH_IGCC_N',        0.0096,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2040,'COABH_IGCC_N',        0.0096,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2045,'COABH_IGCC_N',        0.0096,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2050,'COABH_IGCC_N',        0.0096,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2015,'COABL_IGCC_N',        0.0012,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2020,'COABL_IGCC_N',        0.0012,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2025,'COABL_IGCC_N',        0.0012,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2030,'COABL_IGCC_N',        0.0012,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2035,'COABL_IGCC_N',        0.0012,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2040,'COABL_IGCC_N',        0.0012,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2045,'COABL_IGCC_N',        0.0012,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2050,'COABL_IGCC_N',        0.0012,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2015,'COABM_IGCC_N',        0.0043,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2020,'COABM_IGCC_N',        0.0043,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2025,'COABM_IGCC_N',        0.0043,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2030,'COABM_IGCC_N',        0.0043,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2035,'COABM_IGCC_N',        0.0043,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2040,'COABM_IGCC_N',        0.0043,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2045,'COABM_IGCC_N',        0.0043,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','COAB_EA','E_EA_COAB',2050,'COABM_IGCC_N',        0.0043,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2015,'COABH_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2020,'COABH_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2025,'COABH_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2030,'COABH_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2035,'COABH_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2040,'COABH_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2045,'COABH_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2050,'COABH_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2015,'COABL_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2020,'COABL_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2025,'COABL_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2030,'COABL_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2035,'COABL_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2040,'COABL_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2045,'COABL_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2050,'COABL_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2015,'COABM_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2020,'COABM_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2025,'COABM_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2030,'COABM_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2035,'COABM_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2040,'COABM_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2045,'COABM_IGCC_N',        0.0345,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','COAB_EA','E_EA_COAB',2050,'COABM_IGCC_N',        0.0345,'#kt/PJout','');

-- IGCC CC
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COALIGCC_N_CC','E_CCR_COALIGCC_N',2015,'COALIGCC',        -93.94,'#kt/PJout','#converted from PJin to PJout');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COALIGCC_N_CC','E_CCR_COALIGCC_N',2020,'COALIGCC',        -93.94,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COALIGCC_N_CC','E_CCR_COALIGCC_N',2025,'COALIGCC',        -93.94,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COALIGCC_N_CC','E_CCR_COALIGCC_N',2030,'COALIGCC',        -93.94,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COALIGCC_N_CC','E_CCR_COALIGCC_N',2035,'COALIGCC',        -93.94,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COALIGCC_N_CC','E_CCR_COALIGCC_N',2040,'COALIGCC',        -93.94,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COALIGCC_N_CC','E_CCR_COALIGCC_N',2045,'COALIGCC',        -93.94,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC','COALIGCC_N_CC','E_CCR_COALIGCC_N',2050,'COALIGCC',        -93.94,'#kt/PJout','');

--  Blending tech to collect BIT/SUB/LIG coal for new coal IGCC plant
   INSERT INTO "EmissionActivity" VALUES('co2_ELC','COALIGCC_N_B','E_BLND_BITSUBLIG_COALIGCC_N',2015,'COALIGCCCC', -84,'#kt/PJout',''); -- 'COALIGCCCC' in NUSTD: 'COALIGCC_CCS_N' 
   INSERT INTO "EmissionActivity" VALUES('co2_ELC','COALIGCC_N_B','E_BLND_BITSUBLIG_COALIGCC_N',2020,'COALIGCCCC', -84,'#kt/PJout',''); -- 'COALIGCCCC' in NUSTD: 'COALIGCC_CCS_N'
   INSERT INTO "EmissionActivity" VALUES('co2_ELC','COALIGCC_N_B','E_BLND_BITSUBLIG_COALIGCC_N',2025,'COALIGCCCC', -84,'#kt/PJout',''); -- 'COALIGCCCC' in NUSTD: 'COALIGCC_CCS_N'
   INSERT INTO "EmissionActivity" VALUES('co2_ELC','COALIGCC_N_B','E_BLND_BITSUBLIG_COALIGCC_N',2030,'COALIGCCCC', -84,'#kt/PJout',''); -- 'COALIGCCCC' in NUSTD: 'COALIGCC_CCS_N'
   INSERT INTO "EmissionActivity" VALUES('co2_ELC','COALIGCC_N_B','E_BLND_BITSUBLIG_COALIGCC_N',2035,'COALIGCCCC', -84,'#kt/PJout',''); -- 'COALIGCCCC' in NUSTD: 'COALIGCC_CCS_N'
   INSERT INTO "EmissionActivity" VALUES('co2_ELC','COALIGCC_N_B','E_BLND_BITSUBLIG_COALIGCC_N',2040,'COALIGCCCC', -84,'#kt/PJout',''); -- 'COALIGCCCC' in NUSTD: 'COALIGCC_CCS_N'
   INSERT INTO "EmissionActivity" VALUES('co2_ELC','COALIGCC_N_B','E_BLND_BITSUBLIG_COALIGCC_N',2045,'COALIGCCCC', -84,'#kt/PJout',''); -- 'COALIGCCCC' in NUSTD: 'COALIGCC_CCS_N'
   INSERT INTO "EmissionActivity" VALUES('co2_ELC','COALIGCC_N_B','E_BLND_BITSUBLIG_COALIGCC_N',2050,'COALIGCCCC', -84,'#kt/PJout',''); -- 'COALIGCCCC' in NUSTD: 'COALIGCC_CCS_N'

-- co2 capture retrofit tech before new coal steam plant
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'COALSTM_N_CC', 'E_CCR_COALSTM_N', 2015, 'COALSTMCC', -107.4, '#kt/PJout', '#converted from PJin to PJout');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'COALSTM_N_CC', 'E_CCR_COALSTM_N', 2020, 'COALSTMCC', -107.4, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'COALSTM_N_CC', 'E_CCR_COALSTM_N', 2025, 'COALSTMCC', -107.4, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'COALSTM_N_CC', 'E_CCR_COALSTM_N', 2030, 'COALSTMCC', -107.4, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'COALSTM_N_CC', 'E_CCR_COALSTM_N', 2035, 'COALSTMCC', -107.4, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'COALSTM_N_CC', 'E_CCR_COALSTM_N', 2040, 'COALSTMCC', -107.4, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'COALSTM_N_CC', 'E_CCR_COALSTM_N', 2045, 'COALSTMCC', -107.4, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'COALSTM_N_CC', 'E_CCR_COALSTM_N', 2050, 'COALSTMCC', -107.4, '#kt/PJout', '');

-- Existing Natural gas combustion turbine, new NUSTD code: E_NGACT_R
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA', 'ENGACTR', 1970, 'ELC',   204,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA', 'ENGACTR', 1975, 'ELC',   204,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA', 'ENGACTR', 1980, 'ELC',   204,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA', 'ENGACTR', 1985, 'ELC',   204,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA', 'ENGACTR', 1990, 'ELC',   204,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA', 'ENGACTR', 1995, 'ELC',   204,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA', 'ENGACTR', 2000, 'ELC',   204,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA', 'ENGACTR', 2005, 'ELC',   204,'#kt/PJout', '');

INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGAEA', 'ENGACTR', 1970, 'ELC', 0.019,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGAEA', 'ENGACTR', 1975, 'ELC', 0.019,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGAEA', 'ENGACTR', 1980, 'ELC', 0.019,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGAEA', 'ENGACTR', 1985, 'ELC', 0.019,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGAEA', 'ENGACTR', 1990, 'ELC', 0.019,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGAEA', 'ENGACTR', 1995, 'ELC', 0.019,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGAEA', 'ENGACTR', 2000, 'ELC', 0.019,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGAEA', 'ENGACTR', 2005, 'ELC', 0.019,'#kt/PJout', '');

INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCNGAEA', 'ENGACTR', 1970, 'ELC', 0.001,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCNGAEA', 'ENGACTR', 1975, 'ELC', 0.001,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCNGAEA', 'ENGACTR', 1980, 'ELC', 0.001,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCNGAEA', 'ENGACTR', 1985, 'ELC', 0.001,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCNGAEA', 'ENGACTR', 1990, 'ELC', 0.001,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCNGAEA', 'ENGACTR', 1995, 'ELC', 0.001,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCNGAEA', 'ENGACTR', 2000, 'ELC', 0.001,'#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCNGAEA', 'ENGACTR', 2005, 'ELC', 0.001,'#kt/PJout', '');

-- Future natural gas combustion turbine, new NUSTD code: E_NGACT_N
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA', 'ENGACT05' ,2015, 'ELC', 158, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA', 'ENGACT05' ,2020, 'ELC', 158, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA', 'ENGACT05' ,2025, 'ELC', 158, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA', 'ENGACT05' ,2030, 'ELC', 158, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA', 'ENGACT05' ,2035, 'ELC', 158, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA', 'ENGACT05' ,2040, 'ELC', 158, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA', 'ENGACT05' ,2045, 'ELC', 158, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA', 'ENGACT05' ,2050, 'ELC', 158, '#kt/PJout','');

INSERT INTO "EmissionActivity" VALUES('nox_ELC', 'ELCNGAEA', 'ENGACT05' ,2015, 'ELC',  0.015, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC', 'ELCNGAEA', 'ENGACT05' ,2020, 'ELC',  0.015, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC', 'ELCNGAEA', 'ENGACT05' ,2025, 'ELC',  0.015, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC', 'ELCNGAEA', 'ENGACT05' ,2030, 'ELC',  0.015, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC', 'ELCNGAEA', 'ENGACT05' ,2035, 'ELC',  0.015, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC', 'ELCNGAEA', 'ENGACT05' ,2040, 'ELC',  0.015, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC', 'ELCNGAEA', 'ENGACT05' ,2045, 'ELC',  0.015, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC', 'ELCNGAEA', 'ENGACT05' ,2050, 'ELC',  0.015, '#kt/PJout','');

INSERT INTO "EmissionActivity" VALUES('so2_ELC', 'ELCNGAEA', 'ENGACT05' ,2015, 'ELC', 0.0008, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC', 'ELCNGAEA', 'ENGACT05' ,2020, 'ELC', 0.0008, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC', 'ELCNGAEA', 'ENGACT05' ,2025, 'ELC', 0.0008, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC', 'ELCNGAEA', 'ENGACT05' ,2030, 'ELC', 0.0008, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC', 'ELCNGAEA', 'ENGACT05' ,2035, 'ELC', 0.0008, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC', 'ELCNGAEA', 'ENGACT05' ,2040, 'ELC', 0.0008, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC', 'ELCNGAEA', 'ENGACT05' ,2045, 'ELC', 0.0008, '#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC', 'ELCNGAEA', 'ENGACT05' ,2050, 'ELC', 0.0008, '#kt/PJout','');

-- Natural gas advanced combustion cycle, new NUSTD code: E_NGAACT_N
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA','ENGAACT',2015,'ELC',        126,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA','ENGAACT',2020,'ELC',        126,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA','ENGAACT',2025,'ELC',        126,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA','ENGAACT',2030,'ELC',        126,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA','ENGAACT',2035,'ELC',        126,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA','ENGAACT',2040,'ELC',        126,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA','ENGAACT',2045,'ELC',        126,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGAEA','ENGAACT',2050,'ELC',        126,'#kt/PJout','');

INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGAEA','ENGAACT',2015,'ELC',        0.012,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGAEA','ENGAACT',2020,'ELC',        0.012,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGAEA','ENGAACT',2025,'ELC',        0.012,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGAEA','ENGAACT',2030,'ELC',        0.012,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGAEA','ENGAACT',2035,'ELC',        0.012,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGAEA','ENGAACT',2040,'ELC',        0.012,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGAEA','ENGAACT',2045,'ELC',        0.012,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGAEA','ENGAACT',2050,'ELC',        0.012,'#kt/PJout','');

INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCNGAEA','ENGAACT',2015,'ELC',        0.0006,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCNGAEA','ENGAACT',2020,'ELC',        0.0006,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCNGAEA','ENGAACT',2025,'ELC',        0.0006,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCNGAEA','ENGAACT',2030,'ELC',        0.0006,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCNGAEA','ENGAACT',2035,'ELC',        0.0006,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCNGAEA','ENGAACT',2040,'ELC',        0.0006,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCNGAEA','ENGAACT',2045,'ELC',        0.0006,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCNGAEA','ENGAACT',2050,'ELC',        0.0006,'#kt/PJout','');

-- Existing NG combined cycle, new NUSTD code: E_NGACC_R
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACCR', 1970, 'ELC',    136, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACCR', 1975, 'ELC',    136, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACCR', 1980, 'ELC',    136, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACCR', 1985, 'ELC',    136, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACCR', 1990, 'ELC',    136, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACCR', 1995, 'ELC',    136, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACCR', 2000, 'ELC',    136, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACCR', 2005, 'ELC',    136, '#kt/PJout', '');

INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACCR', 1970, 'ELC', 0.0128, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACCR', 1975, 'ELC', 0.0128, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACCR', 1980, 'ELC', 0.0128, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACCR', 1985, 'ELC', 0.0128, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACCR', 1990, 'ELC', 0.0128, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACCR', 1995, 'ELC', 0.0128, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACCR', 2000, 'ELC', 0.0128, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACCR', 2005, 'ELC', 0.0128, '#kt/PJout', '');

-- Future NG combined cycle, new NUSTD code: E_NGACC_N
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACC05', 2015, 'ELC', 100.25, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACC05', 2020, 'ELC', 100.25, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACC05', 2025, 'ELC', 100.25, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACC05', 2030, 'ELC', 100.25, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACC05', 2035, 'ELC', 100.25, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACC05', 2040, 'ELC', 100.25, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACC05', 2045, 'ELC', 100.25, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACC05', 2050, 'ELC', 100.25, '#kt/PJout', '');

INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACC05', 2015, 'ELC', 0.0094, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACC05', 2020, 'ELC', 0.0094, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACC05', 2025, 'ELC', 0.0094, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACC05', 2030, 'ELC', 0.0094, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACC05', 2035, 'ELC', 0.0094, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACC05', 2040, 'ELC', 0.0094, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACC05', 2045, 'ELC', 0.0094, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACC05', 2050, 'ELC', 0.0094, '#kt/PJout', '');

-- FUture NG advanced combined cycle, new NUSTD code: E_NGAACC_N
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGAACC', 2015, 'ELC',   93.4, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGAACC', 2020, 'ELC',   93.4, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGAACC', 2025, 'ELC',   93.4, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGAACC', 2030, 'ELC',   93.4, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGAACC', 2035, 'ELC',   93.4, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGAACC', 2040, 'ELC',   93.4, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGAACC', 2045, 'ELC',   93.4, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGAACC', 2050, 'ELC',   93.4, '#kt/PJout', '');

INSERT INTO "EmissionActivity" VALUES('nox_ELC', 'ELCNGCEA', 'ENGAACC', 2015, 'ELC', 0.0088, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC', 'ELCNGCEA', 'ENGAACC', 2020, 'ELC', 0.0088, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC', 'ELCNGCEA', 'ENGAACC', 2025, 'ELC', 0.0088, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC', 'ELCNGCEA', 'ENGAACC', 2030, 'ELC', 0.0088, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC', 'ELCNGCEA', 'ENGAACC', 2035, 'ELC', 0.0088, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC', 'ELCNGCEA', 'ENGAACC', 2040, 'ELC', 0.0088, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC', 'ELCNGCEA', 'ENGAACC', 2045, 'ELC', 0.0088, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC', 'ELCNGCEA', 'ENGAACC', 2050, 'ELC', 0.0088, '#kt/PJout', '');

-- Future NG combined cycle w/CCS, new NUSTD code: E_NGACC_CCS_N
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACCCCS',    2015, 'ELC',     11,'#kt/PJout','#accounted for co2 capture');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACCCCS',    2020, 'ELC',     11,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACCCCS',    2025, 'ELC',     11,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACCCCS',    2030, 'ELC',     11,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACCCCS',    2035, 'ELC',     11,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACCCCS',    2040, 'ELC',     11,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACCCCS',    2045, 'ELC',     11,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCNGCEA', 'ENGACCCCS',    2050, 'ELC',     11,'#kt/PJout','');

INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACCCCS',    2015, 'ELC', 0.0104,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACCCCS',    2020, 'ELC', 0.0104,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACCCCS',    2025, 'ELC', 0.0104,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACCCCS',    2030, 'ELC', 0.0104,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACCCCS',    2035, 'ELC', 0.0104,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACCCCS',    2040, 'ELC', 0.0104,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACCCCS',    2045, 'ELC', 0.0104,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCNGCEA', 'ENGACCCCS',    2050, 'ELC', 0.0104,'#kt/PJout','');

-- Existing diesel fired combustion turbine, new NUSTD code: E_DSLCT_R
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCDSLEA', 'EDSLCTR', 1970, 'ELC', 314.3, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCDSLEA', 'EDSLCTR', 1975, 'ELC', 314.3, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCDSLEA', 'EDSLCTR', 1980, 'ELC', 314.3, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCDSLEA', 'EDSLCTR', 1985, 'ELC', 314.3, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCDSLEA', 'EDSLCTR', 1990, 'ELC', 314.3, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCDSLEA', 'EDSLCTR', 1995, 'ELC', 314.3, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCDSLEA', 'EDSLCTR', 2000, 'ELC', 314.3, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('co2_ELC', 'ELCDSLEA', 'EDSLCTR', 2005, 'ELC', 314.3, '#kt/PJout', '');

INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCDSLEA', 'EDSLCTR', 1970, 'ELC', 0.487, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCDSLEA', 'EDSLCTR', 1975, 'ELC', 0.487, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCDSLEA', 'EDSLCTR', 1980, 'ELC', 0.487, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCDSLEA', 'EDSLCTR', 1985, 'ELC', 0.487, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCDSLEA', 'EDSLCTR', 1990, 'ELC', 0.487, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCDSLEA', 'EDSLCTR', 1995, 'ELC', 0.487, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCDSLEA', 'EDSLCTR', 2000, 'ELC', 0.487, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCDSLEA', 'EDSLCTR', 2005, 'ELC', 0.487, '#kt/PJout', '');

INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCDSLEA', 'EDSLCTR', 1970, 'ELC', 1.605, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCDSLEA', 'EDSLCTR', 1975, 'ELC', 1.605, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCDSLEA', 'EDSLCTR', 1980, 'ELC', 1.605, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCDSLEA', 'EDSLCTR', 1985, 'ELC', 1.605, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCDSLEA', 'EDSLCTR', 1990, 'ELC', 1.605, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCDSLEA', 'EDSLCTR', 1995, 'ELC', 1.605, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCDSLEA', 'EDSLCTR', 2000, 'ELC', 1.605, '#kt/PJout', '');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCDSLEA', 'EDSLCTR', 2005, 'ELC', 1.605, '#kt/PJout', '');

-- Existing bio steam
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCBIOSTM','EBIOSTMR',2005,'ELC', 0.273,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCBIOSTM','EBIOSTMR',2005,'ELC',  0.79,'#kt/PJout','');

-- Future bio IGCC
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCBIGCCEA','EBIOIGCC',2015,'ELC', 0.196,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCBIGCCEA','EBIOIGCC',2020,'ELC', 0.196,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCBIGCCEA','EBIOIGCC',2025,'ELC', 0.196,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCBIGCCEA','EBIOIGCC',2030,'ELC', 0.196,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCBIGCCEA','EBIOIGCC',2035,'ELC', 0.196,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCBIGCCEA','EBIOIGCC',2040,'ELC', 0.196,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCBIGCCEA','EBIOIGCC',2045,'ELC', 0.196,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('nox_ELC','ELCBIGCCEA','EBIOIGCC',2050,'ELC', 0.196,'#kt/PJout','');

INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCBIGCCEA','EBIOIGCC',2015,'ELC', 0.104,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCBIGCCEA','EBIOIGCC',2020,'ELC', 0.104,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCBIGCCEA','EBIOIGCC',2025,'ELC', 0.104,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCBIGCCEA','EBIOIGCC',2030,'ELC', 0.104,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCBIGCCEA','EBIOIGCC',2035,'ELC', 0.104,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCBIGCCEA','EBIOIGCC',2040,'ELC', 0.104,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCBIGCCEA','EBIOIGCC',2045,'ELC', 0.104,'#kt/PJout','');
INSERT INTO "EmissionActivity" VALUES('so2_ELC','ELCBIGCCEA','EBIOIGCC',2050,'ELC', 0.104,'#kt/PJout','');

-- Importing bit coal
INSERT INTO "EmissionActivity" VALUES('co2_SUP', 'ethos', 'IMPELCCOAB', 2015, 'COAB_EA',     0.44, '#kt/PJout', '');    
INSERT INTO "EmissionActivity" VALUES('so2_SUP', 'ethos', 'IMPELCCOAB', 2015, 'COAB_EA', 0.006265, '#kt/PJout', '');    
INSERT INTO "EmissionActivity" VALUES('nox_SUP', 'ethos', 'IMPELCCOAB', 2015, 'COAB_EA',  0.00055, '#kt/PJout', '');    

-- Importing Natural gas for combustion turbines
INSERT INTO "EmissionActivity" VALUES('co2_SUP', 'ethos', 'IMPELCNGAEA', 2015, 'ELCNGAEA',      4.33, '#kt/PJout', '');    
INSERT INTO "EmissionActivity" VALUES('so2_SUP', 'ethos', 'IMPELCNGAEA', 2015, 'ELCNGAEA',    0.0107, '#kt/PJout', '');    
INSERT INTO "EmissionActivity" VALUES('nox_SUP', 'ethos', 'IMPELCNGAEA', 2015, 'ELCNGAEA',    0.0176, '#kt/PJout', '');    
-- Importing Natural gas for combined cycles
INSERT INTO "EmissionActivity" VALUES('co2_SUP', 'ethos', 'IMPELCNGCEA', 2015, 'ELCNGCEA',      4.33, '#kt/PJout', '');    
INSERT INTO "EmissionActivity" VALUES('so2_SUP', 'ethos', 'IMPELCNGCEA', 2015, 'ELCNGCEA',    0.0107, '#kt/PJout', '');    
INSERT INTO "EmissionActivity" VALUES('nox_SUP', 'ethos', 'IMPELCNGCEA', 2015, 'ELCNGCEA',    0.0176, '#kt/PJout', '');    

-- Importing diesel, new NUSTD code: IMPELCDSL
INSERT INTO "EmissionActivity" VALUES('co2_SUP', 'ethos', 'IMPELCDSLEA', 2015,'ELCDSLEA',   11.95,'#kt/PJout','');   
INSERT INTO "EmissionActivity" VALUES('so2_SUP', 'ethos', 'IMPELCDSLEA', 2015,'ELCDSLEA',  0.0191,'#kt/PJout','');   
INSERT INTO "EmissionActivity" VALUES('nox_SUP', 'ethos', 'IMPELCDSLEA', 2015,'ELCDSLEA',  0.0196,'#kt/PJout','');   

-- Importing bio steam, new NUSTD code: IMPELCBSTMEA
INSERT INTO "EmissionActivity" VALUES('so2_SUP','ethos', 'IMPELCBIOSTM',2015,'ELCBIOSTM',  0.243,'#kt/PJout',''); 

-------------------------------------------------
CREATE TABLE EmissionLimit  (
   periods integer,
   emis_comm text,
   emis_limit real,
   emis_limit_units text,
   emis_limit_notes text,
   PRIMARY KEY(periods, emis_comm),
   FOREIGN KEY(periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(emis_comm) REFERENCES commodities(comm_name) );
   INSERT INTO "EmissionLimit" VALUES(2015,'nox_ELC',29.9,'#kt','# MARKAL 2014 v1.1 R5, apportioned based on history emission share of NC Electric Power Profile');
   INSERT INTO "EmissionLimit" VALUES(2020,'nox_ELC',33.4,'#kt','# MARKAL 2014 v1.1 R5, apportioned based on history emission share of NC from EIA Power Profile');
   INSERT INTO "EmissionLimit" VALUES(2025,'nox_ELC',34.7,'#kt','# MARKAL 2014 v1.1 R5, apportioned based on history emission share of NC from EIA Power Profile');
   INSERT INTO "EmissionLimit" VALUES(2030,'nox_ELC',34.7,'#kt','# MARKAL 2014 v1.1 R5, apportioned based on history emission share of NC from EIA Power Profile');
   INSERT INTO "EmissionLimit" VALUES(2035,'nox_ELC',34.7,'#kt','# MARKAL 2014 v1.1 R5, apportioned based on history emission share of NC from EIA Power Profile');
   INSERT INTO "EmissionLimit" VALUES(2040,'nox_ELC',34.7,'#kt','# MARKAL 2014 v1.1 R5, apportioned based on history emission share of NC from EIA Power Profile');
   INSERT INTO "EmissionLimit" VALUES(2045,'nox_ELC',34.7,'#kt','# MARKAL 2014 v1.1 R5, apportioned based on history emission share of NC from EIA Power Profile');
   INSERT INTO "EmissionLimit" VALUES(2050,'nox_ELC',34.7,'#kt','# MARKAL 2014 v1.1 R5, apportioned based on history emission share of NC from EIA Power Profile');
   
   INSERT INTO "EmissionLimit" VALUES(2015,'so2_ELC',30.1,'#kt','# MARKAL 2014 v1.1 R5, apportioned based on history emission share of NC from EIA Power Profile');
   INSERT INTO "EmissionLimit" VALUES(2020,'so2_ELC',33.5,'#kt','# MARKAL 2014 v1.1 R5, apportioned based on history emission share of NC from EIA Power Profile');
   INSERT INTO "EmissionLimit" VALUES(2025,'so2_ELC',34.9,'#kt','# MARKAL 2014 v1.1 R5, apportioned based on history emission share of NC from EIA Power Profile');
   INSERT INTO "EmissionLimit" VALUES(2030,'so2_ELC',34.9,'#kt','# MARKAL 2014 v1.1 R5, apportioned based on history emission share of NC from EIA Power Profile');
   INSERT INTO "EmissionLimit" VALUES(2035,'so2_ELC',34.9,'#kt','# MARKAL 2014 v1.1 R5, apportioned based on history emission share of NC from EIA Power Profile');
   INSERT INTO "EmissionLimit" VALUES(2040,'so2_ELC',34.9,'#kt','# MARKAL 2014 v1.1 R5, apportioned based on history emission share of NC from EIA Power Profile');
   INSERT INTO "EmissionLimit" VALUES(2045,'so2_ELC',34.9,'#kt','# MARKAL 2014 v1.1 R5, apportioned based on history emission share of NC from EIA Power Profile');
   INSERT INTO "EmissionLimit" VALUES(2050,'so2_ELC',34.9,'#kt','# MARKAL 2014 v1.1 R5, apportioned based on history emission share of NC from EIA Power Profile');

-------------------------------------------------
CREATE TABLE TechInputSplit (
   periods integer,
   input_comm text,
   tech text,
   ti_split real,
   ti_split_notes text,
   PRIMARY KEY(periods, input_comm, tech),
   FOREIGN KEY(periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(input_comm) REFERENCES commodities(comm_name),
   FOREIGN KEY(tech) REFERENCES technologies(tech) );

INSERT INTO "TechInputSplit" VALUES(2015, 'COALSTM_R_B',  'E_BLND_BITSUBLIG_COALSTM_R',  1,'');
INSERT INTO "TechInputSplit" VALUES(2015, 'COALIGCC_N_B', 'E_BLND_BITSUBLIG_COALIGCC_N', 1,'');
INSERT INTO "TechInputSplit" VALUES(2015, 'COALSTM_N_B',  'E_BLND_BITSUBLIG_COALSTM_N',  1,'');

INSERT INTO "TechInputSplit" VALUES(2020, 'COALSTM_R_B',  'E_BLND_BITSUBLIG_COALSTM_R',  1,'');
INSERT INTO "TechInputSplit" VALUES(2020, 'COALIGCC_N_B', 'E_BLND_BITSUBLIG_COALIGCC_N', 1,'');
INSERT INTO "TechInputSplit" VALUES(2020, 'COALSTM_N_B',  'E_BLND_BITSUBLIG_COALSTM_N',  1,'');

INSERT INTO "TechInputSplit" VALUES(2025, 'COALSTM_R_B',  'E_BLND_BITSUBLIG_COALSTM_R',  1,'');
INSERT INTO "TechInputSplit" VALUES(2025, 'COALIGCC_N_B', 'E_BLND_BITSUBLIG_COALIGCC_N', 1,'');
INSERT INTO "TechInputSplit" VALUES(2025, 'COALSTM_N_B',  'E_BLND_BITSUBLIG_COALSTM_N',  1,'');

INSERT INTO "TechInputSplit" VALUES(2030, 'COALSTM_R_B',  'E_BLND_BITSUBLIG_COALSTM_R',  1,'');
INSERT INTO "TechInputSplit" VALUES(2030, 'COALIGCC_N_B', 'E_BLND_BITSUBLIG_COALIGCC_N', 1,'');
INSERT INTO "TechInputSplit" VALUES(2030, 'COALSTM_N_B',  'E_BLND_BITSUBLIG_COALSTM_N',  1,'');

INSERT INTO "TechInputSplit" VALUES(2035, 'COALSTM_R_B',  'E_BLND_BITSUBLIG_COALSTM_R',  1,'');
INSERT INTO "TechInputSplit" VALUES(2035, 'COALIGCC_N_B', 'E_BLND_BITSUBLIG_COALIGCC_N', 1,'');
INSERT INTO "TechInputSplit" VALUES(2035, 'COALSTM_N_B',  'E_BLND_BITSUBLIG_COALSTM_N',  1,'');

INSERT INTO "TechInputSplit" VALUES(2040, 'COALSTM_R_B',  'E_BLND_BITSUBLIG_COALSTM_R',  1,'');
INSERT INTO "TechInputSplit" VALUES(2040, 'COALIGCC_N_B', 'E_BLND_BITSUBLIG_COALIGCC_N', 1,'');
INSERT INTO "TechInputSplit" VALUES(2040, 'COALSTM_N_B',  'E_BLND_BITSUBLIG_COALSTM_N',  1,'');

INSERT INTO "TechInputSplit" VALUES(2045, 'COALSTM_R_B',  'E_BLND_BITSUBLIG_COALSTM_R',  1,'');
INSERT INTO "TechInputSplit" VALUES(2045, 'COALIGCC_N_B', 'E_BLND_BITSUBLIG_COALIGCC_N', 1,'');
INSERT INTO "TechInputSplit" VALUES(2045, 'COALSTM_N_B',  'E_BLND_BITSUBLIG_COALSTM_N',  1,'');

INSERT INTO "TechInputSplit" VALUES(2050, 'COALSTM_R_B',  'E_BLND_BITSUBLIG_COALSTM_R',  1,'');
INSERT INTO "TechInputSplit" VALUES(2050, 'COALIGCC_N_B', 'E_BLND_BITSUBLIG_COALIGCC_N', 1,'');
INSERT INTO "TechInputSplit" VALUES(2050, 'COALSTM_N_B',  'E_BLND_BITSUBLIG_COALSTM_N',  1,'');

-------------------------------------------------
CREATE TABLE TechOutputSplit (
   tech text,
   output_comm text,
   to_split real,
   to_split_notes text,
   PRIMARY KEY(tech, output_comm),
   FOREIGN KEY(tech) REFERENCES technologies(tech),
   FOREIGN KEY(output_comm) REFERENCES commodities(comm_name) );
   
-------------------------------------------------
CREATE TABLE MinCapacity (
   periods integer,
   tech text,
   mincap real,
   mincap_units text,
   mincap_notes text,
   PRIMARY KEY(periods, tech),
   FOREIGN KEY(periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(tech) REFERENCES technologies(tech) );

-------------------------------------------------
CREATE TABLE MaxCapacity (
   periods integer,
   tech text,
   maxcap real,
   maxcap_units text,
   maxcap_notes text,
   PRIMARY KEY(periods, tech),
   FOREIGN KEY(periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(tech) REFERENCES technologies(tech) );

INSERT INTO "MaxCapacity" VALUES(2015, 'EGEOBCFS',       0, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2020, 'EGEOBCFS',       0, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2025, 'EGEOBCFS',       0, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2030, 'EGEOBCFS',       0, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2035, 'EGEOBCFS',       0, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2040, 'EGEOBCFS',       0, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2045, 'EGEOBCFS',       0, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2050, 'EGEOBCFS',       0, 'GW', '');

INSERT INTO "MaxCapacity" VALUES(2015, 'ESOLSTCEN',       0, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2020, 'ESOLSTCEN',       0, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2025, 'ESOLSTCEN',       0, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2030, 'ESOLSTCEN',       0, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2035, 'ESOLSTCEN',       0, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2040, 'ESOLSTCEN',       0, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2045, 'ESOLSTCEN',       0, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2050, 'ESOLSTCEN',       0, 'GW', '');

INSERT INTO "MaxCapacity" VALUES(2015, 'EWNDON',       1, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2020, 'EWNDON',       1, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2025, 'EWNDON',       1, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2030, 'EWNDON',       1, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2035, 'EWNDON',       1, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2040, 'EWNDON',       1, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2045, 'EWNDON',       1, 'GW', '');
INSERT INTO "MaxCapacity" VALUES(2050, 'EWNDON',       1, 'GW', '');
-------------------------------------------------
CREATE TABLE MinActivity (
   periods integer,
   tech text,
   minact real,
   minact_units text,
   minact_notes text,
   PRIMARY KEY(periods, tech),
   FOREIGN KEY(periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(tech) REFERENCES technologies(tech) );  

-------------------------------------------------
CREATE TABLE MaxActivity (
   periods integer,
   tech text,
   maxact real,
   maxact_units text,
   maxact_notes text,
   PRIMARY KEY(periods, tech),
   FOREIGN KEY(periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(tech) REFERENCES technologies(tech) );

INSERT INTO "MaxActivity" VALUES(2015, 'ECOASTMR', 170, 'PJ', '');
INSERT INTO "MaxActivity" VALUES(2020, 'ECOASTMR', 170, 'PJ', '');
INSERT INTO "MaxActivity" VALUES(2025, 'ECOASTMR', 170, 'PJ', '');
INSERT INTO "MaxActivity" VALUES(2030, 'ECOASTMR', 170, 'PJ', '');
INSERT INTO "MaxActivity" VALUES(2035, 'ECOASTMR', 170, 'PJ', '');
INSERT INTO "MaxActivity" VALUES(2040, 'ECOASTMR', 170, 'PJ', '');
INSERT INTO "MaxActivity" VALUES(2045, 'ECOASTMR', 170, 'PJ', '');
INSERT INTO "MaxActivity" VALUES(2050, 'ECOASTMR', 170, 'PJ', '');

-------------------------------------------------
CREATE TABLE GrowthRateMax (
   tech text,
   growthrate_max real,
   growthrate_max_notes text,
   FOREIGN KEY(tech) REFERENCES technologies(tech) );
INSERT INTO "GrowthRateMax" VALUES('ECOALSTM',   1.05, '');
-- INSERT INTO "GrowthRateMax" VALUES('EWNDOFD',    1.05, '');
INSERT INTO "GrowthRateMax" VALUES('EWNDOFS',    1.05, '');
INSERT INTO "GrowthRateMax" VALUES('EWNDON',     1.05, '');
INSERT INTO "GrowthRateMax" VALUES('EURNALWR15', 1.05, '');

-------------------------------------------------
CREATE TABLE GrowthRateSeed (
   tech text,
   growthrate_seed real,
   growthrate_seed_units text,
   growthrate_seed_notes text,
   FOREIGN KEY(tech) REFERENCES technologies(tech) );
------------------------------------------------- 
INSERT INTO "GrowthRateSeed" VALUES('ECOALSTM',   0.1, 'GW', '');
-- INSERT INTO "GrowthRateSeed" VALUES('EWNDOFD',    0.1, 'GW', '');
INSERT INTO "GrowthRateSeed" VALUES('EWNDOFS',    0.1, 'GW', '');
INSERT INTO "GrowthRateSeed" VALUES('EWNDON',     0.1, 'GW', '');
INSERT INTO "GrowthRateSeed" VALUES('EURNALWR15', 0.1, 'GW', '');

CREATE TABLE LifetimeProcess (
   tech text,
   vintage integer,
   life_process real,
   life_process_notes text,
   PRIMARY KEY(tech, vintage),
   FOREIGN KEY(tech) REFERENCES technologies(tech),
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods) );
   
-------------------------------------------------
CREATE TABLE LifetimeLoanTech (
   tech text,
   loan real,
   loan_notes text,
   PRIMARY KEY(tech),
   FOREIGN KEY(tech) REFERENCES technologies(tech) );
   
-------------------------------------------------
CREATE TABLE Output_VFlow_Out (
   scenario text,
   t_periods integer,
   t_season text,
   t_day text,
   input_comm text,
   tech text,
   vintage integer,
   output_comm text,
   vflow_out real,
   PRIMARY KEY(scenario, t_periods, t_season, t_day, input_comm, tech, vintage, output_comm),
   FOREIGN KEY(t_periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(t_season) REFERENCES time_periods(t_periods),   
   FOREIGN KEY(t_day) REFERENCES time_of_day(t_day),
   FOREIGN KEY(input_comm) REFERENCES commodities(comm_name),
   FOREIGN KEY(tech) REFERENCES technologies(tech),
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods), 
   FOREIGN KEY(output_comm) REFERENCES commodities(comm_name));

-------------------------------------------------
CREATE TABLE Output_VFlow_In (
   scenario text,
   t_periods integer,
   t_season text,
   t_day text,
   input_comm text,
   tech text,
   vintage integer,
   output_comm text,
   vflow_in real,
   PRIMARY KEY(scenario, t_periods, t_season, t_day, input_comm, tech, vintage, output_comm),
   FOREIGN KEY(t_periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(t_season) REFERENCES time_periods(t_periods),   
   FOREIGN KEY(t_day) REFERENCES time_of_day(t_day),
   FOREIGN KEY(input_comm) REFERENCES commodities(comm_name),
   FOREIGN KEY(tech) REFERENCES technologies(tech),
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods), 
   FOREIGN KEY(output_comm) REFERENCES commodities(comm_name));
 
-------------------------------------------------
CREATE TABLE Output_Capacity (
   scenario text,
   t_periods integer,
   tech text,
   capacity real,
   PRIMARY KEY(scenario, t_periods, tech),
   FOREIGN KEY(t_periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(tech) REFERENCES technologies(tech)); 

-------------------------------------------------
CREATE TABLE V_Capacity (
   scenario text,
   tech text,
   vintage integer,
   capacity real,
   PRIMARY KEY(scenario, tech, vintage),
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods), 
   FOREIGN KEY(tech) REFERENCES technologies(tech)); 

-------------------------------------------------
CREATE TABLE V_ActivityByPeriodAndProcess (    
   scenario text,
   t_periods integer,
   tech text,
   vintage integer,
   activity real,
   PRIMARY KEY(scenario, t_periods, tech, vintage),
   FOREIGN KEY(t_periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(tech) REFERENCES technologies(tech)
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods));

-------------------------------------------------
CREATE TABLE Output_Emissions (    
   scenario text,
   t_periods integer,
   emissions_comm text,
   tech text,
   vintage integer,
   emissions real,
   PRIMARY KEY(scenario, t_periods, emissions_comm, tech, vintage),
   FOREIGN KEY(emissions_comm) REFERENCES EmissionActivity(emis_comm),
   FOREIGN KEY(t_periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(tech) REFERENCES technologies(tech)
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods));

-------------------------------------------------
CREATE TABLE Output_Costs (
   scenario text,
   output_name text,
   tech text,
   vintage integer,
   output_cost real,
   PRIMARY KEY(scenario, output_name, tech, vintage),
   FOREIGN KEY(tech) REFERENCES technologies(tech),   
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods)); 

-------------------------------------------------
CREATE TABLE Output_TotalCost (
   scenario text,
   total_system_cost real);
   
COMMIT;
