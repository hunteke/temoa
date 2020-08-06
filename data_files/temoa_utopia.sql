BEGIN TRANSACTION;
CREATE TABLE time_season (
  t_season text primary key );
INSERT INTO `time_season` (t_season) VALUES ('inter');
INSERT INTO `time_season` (t_season) VALUES ('summer');
INSERT INTO `time_season` (t_season) VALUES ('winter');
CREATE TABLE time_periods (
  t_periods integer primary key,
  flag text,
  FOREIGN KEY(flag) REFERENCES time_period_labels(t_period_labels));
INSERT INTO `time_periods` (t_periods,flag) VALUES (1960,'e');
INSERT INTO `time_periods` (t_periods,flag) VALUES (1970,'e');
INSERT INTO `time_periods` (t_periods,flag) VALUES (1980,'e');
INSERT INTO `time_periods` (t_periods,flag) VALUES (1990,'f');
INSERT INTO `time_periods` (t_periods,flag) VALUES (2000,'f');
INSERT INTO `time_periods` (t_periods,flag) VALUES (2010,'f');
INSERT INTO `time_periods` (t_periods,flag) VALUES (2020,'f');
CREATE TABLE time_period_labels (
  t_period_labels text primary key,
  t_period_labels_desc text);
INSERT INTO `time_period_labels` (t_period_labels,t_period_labels_desc) VALUES ('e','existing vintages');
INSERT INTO `time_period_labels` (t_period_labels,t_period_labels_desc) VALUES ('f','future');
CREATE TABLE time_of_day (
  t_day text primary key );
INSERT INTO `time_of_day` (t_day) VALUES ('day');
INSERT INTO `time_of_day` (t_day) VALUES ('night');
CREATE TABLE technology_labels (
  tech_labels text primary key,
  tech_labels_desc text);
INSERT INTO `technology_labels` (tech_labels,tech_labels_desc) VALUES ('r','resource technology');
INSERT INTO `technology_labels` (tech_labels,tech_labels_desc) VALUES ('p','production technology');
INSERT INTO `technology_labels` (tech_labels,tech_labels_desc) VALUES ('pb','baseload production technology');
INSERT INTO `technology_labels` (tech_labels,tech_labels_desc) VALUES ('ps','storage production technology');
CREATE TABLE technologies (
  tech text primary key,
  flag text,
  sector text,
  tech_desc text,
  tech_category text,
  FOREIGN KEY(flag) REFERENCES technology_labels(tech_labels),
  FOREIGN KEY(sector) REFERENCES sector_labels(sector));
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('IMPDSL1','r','supply',' imported diesel','petroleum');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('IMPGSL1','r','supply',' imported gasoline','petroleum');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('IMPHCO1','r','supply',' imported coal','coal');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('IMPOIL1','r','supply',' imported crude oil','petroleum');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('IMPURN1','r','supply',' imported uranium','uranium');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('IMPFEQ','r','supply',' imported fossil equivalent','');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('IMPHYD','r','supply',' imported water -- doesnt exist in Utopia','water');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('E01','pb','electric',' coal power plant','coal');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('E21','pb','electric',' nuclear power plant','nuclear');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('E31','pb','electric',' hydro power','hydro');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('E51','ps','electric',' electric storage','storage');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('E70','p','electric',' diesel power plant','diesel');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('RHE','p','residential',' electric residential heating','electric');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('RHO','p','residential',' diesel residential heating','diesel');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('RL1','p','residential',' residential lighting','electric');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('SRE','p','supply',' crude oil processor','petroleum');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('TXD','p','transport',' diesel powered vehicles','diesel');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('TXE','p','transport',' electric powered vehicles','electric');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('TXG','p','transport',' gasoline powered vehicles','gasoline');
CREATE TABLE `tech_reserve` (
	`tech`	text,
	`notes`	text,
	PRIMARY KEY(`tech`)
);
CREATE TABLE `tech_curtailment` (
	`technology`	text,
	PRIMARY KEY(`technology`),
	FOREIGN KEY(`technology`) REFERENCES `technologies`(`tech`)
);
CREATE TABLE "tech_annual" (
	`tech`	text,
	`region`	TEXT,
	PRIMARY KEY(tech),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`)
);
CREATE TABLE sector_labels (
  sector text primary key);
INSERT INTO `sector_labels` (sector) VALUES ('supply');
INSERT INTO `sector_labels` (sector) VALUES ('electric');
INSERT INTO `sector_labels` (sector) VALUES ('transport');
INSERT INTO `sector_labels` (sector) VALUES ('commercial');
INSERT INTO `sector_labels` (sector) VALUES ('residential');
INSERT INTO `sector_labels` (sector) VALUES ('industrial');
CREATE TABLE `regions` (
	`region`	TEXT,
	`region_note`	TEXT,
	PRIMARY KEY(`region`)
);
INSERT INTO `regions` (region,region_note) VALUES ('utopia',NULL);
CREATE TABLE `groups` (
	`group_name`	text,
	`notes`	text,
	PRIMARY KEY(`group_name`)
);
CREATE TABLE commodity_labels (
  comm_labels text primary key,
  comm_labels_desc text);
INSERT INTO `commodity_labels` (comm_labels,comm_labels_desc) VALUES ('p','physical commodity');
INSERT INTO `commodity_labels` (comm_labels,comm_labels_desc) VALUES ('e','emissions commodity');
INSERT INTO `commodity_labels` (comm_labels,comm_labels_desc) VALUES ('d','demand commodity');
CREATE TABLE commodities (
  comm_name text primary key,
  flag text,  
  comm_desc text,
  FOREIGN KEY(flag) REFERENCES commodity_labels(comm_labels));
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('ethos','p','# dummy commodity to supply inputs (makes graph easier to read)');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('DSL','p','# diesel');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('ELC','p','# electricity');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('FEQ','p','# fossil equivalent');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('GSL','p','# gasoline');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('HCO','p','# coal');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('HYD','p','# water');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('OIL','p','# crude oil');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('URN','p','# uranium');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('co2','e','#CO2 emissions');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('nox','e','#NOX emissions');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('RH','d','# residential heating');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('RL','d','# residential lighting');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('TX','d','# transportation');
CREATE TABLE "TechOutputSplit" (
	`region`	TEXT,
	`periods`	integer,
	`tech`	TEXT,
	`output_comm`	text,
	`to_split`	real,
	`to_split_notes`	text,
	PRIMARY KEY(region,periods,tech,output_comm),
	FOREIGN KEY(`periods`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`),
	FOREIGN KEY(`output_comm`) REFERENCES `commodities`(`comm_name`)
);
INSERT INTO `TechOutputSplit` (region,periods,tech,output_comm,to_split,to_split_notes) VALUES ('utopia',1990,'SRE','DSL',0.7,'');
INSERT INTO `TechOutputSplit` (region,periods,tech,output_comm,to_split,to_split_notes) VALUES ('utopia',2000,'SRE','DSL',0.7,'');
INSERT INTO `TechOutputSplit` (region,periods,tech,output_comm,to_split,to_split_notes) VALUES ('utopia',2010,'SRE','DSL',0.7,'');
INSERT INTO `TechOutputSplit` (region,periods,tech,output_comm,to_split,to_split_notes) VALUES ('utopia',1990,'SRE','GSL',0.3,'');
INSERT INTO `TechOutputSplit` (region,periods,tech,output_comm,to_split,to_split_notes) VALUES ('utopia',2000,'SRE','GSL',0.3,'');
INSERT INTO `TechOutputSplit` (region,periods,tech,output_comm,to_split,to_split_notes) VALUES ('utopia',2010,'SRE','GSL',0.3,'');
CREATE TABLE "TechInputSplit" (
	`region`	TEXT,
	`periods`	integer,
	`input_comm`	text,
	`tech`	text,
	`ti_split`	real,
	`ti_split_notes`	text,
	PRIMARY KEY(region,periods,input_comm,tech),
	FOREIGN KEY(`periods`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`input_comm`) REFERENCES `commodities`(`comm_name`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`)
);
CREATE TABLE `StorageDuration` (
	`region`	text,
	`tech`	text,
	`duration`	real,
	`duration_notes`	text,
	PRIMARY KEY(`region`,`tech`)
);
CREATE TABLE SegFrac (
   season_name text,
   time_of_day_name text,
   segfrac real check (segfrac>=0 AND segfrac<=1),
   segfrac_notes text,
   PRIMARY KEY(season_name, time_of_day_name), --here's where I define primary key as a combo of columns
   FOREIGN KEY(season_name) REFERENCES time_season(t_season),
   FOREIGN KEY(time_of_day_name) REFERENCES time_of_day(t_day) );
INSERT INTO `SegFrac` (season_name,time_of_day_name,segfrac,segfrac_notes) VALUES ('inter','day',0.1667,'# I-D');
INSERT INTO `SegFrac` (season_name,time_of_day_name,segfrac,segfrac_notes) VALUES ('inter','night',0.0833,'# I-N');
INSERT INTO `SegFrac` (season_name,time_of_day_name,segfrac,segfrac_notes) VALUES ('summer','day',0.1667,'# S-D');
INSERT INTO `SegFrac` (season_name,time_of_day_name,segfrac,segfrac_notes) VALUES ('summer','night',0.0833,'# S-N');
INSERT INTO `SegFrac` (season_name,time_of_day_name,segfrac,segfrac_notes) VALUES ('winter','day',0.3333,'# W-D');
INSERT INTO `SegFrac` (season_name,time_of_day_name,segfrac,segfrac_notes) VALUES ('winter','night',0.1667,'# W-N');
CREATE TABLE `PlanningReserveMargin` (
	`region`	text,
	`reserve_margin`	REAL
);
CREATE TABLE "Output_V_Capacity" (
	`region`	text,
	`scenario`	text,
	`sector`	text,
	`tech`	text,
	`vintage`	integer,
	`capacity`	real,
	PRIMARY KEY(region,scenario,tech,vintage),
	FOREIGN KEY(`sector`) REFERENCES `sector_labels`(`sector`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`),
	FOREIGN KEY(`vintage`) REFERENCES `time_periods`(`t_periods`)
);
CREATE TABLE "Output_VFlow_Out" (
	`region`	text,
	`scenario`	text,
	`sector`	text,
	`t_periods`	integer,
	`t_season`	text,
	`t_day`	text,
	`input_comm`	text,
	`tech`	text,
	`vintage`	integer,
	`output_comm`	text,
	`vflow_out`	real,
	PRIMARY KEY(region,scenario,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm),
	FOREIGN KEY(`sector`) REFERENCES `sector_labels`(`sector`),
	FOREIGN KEY(`t_periods`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`t_season`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`t_day`) REFERENCES `time_of_day`(`t_day`),
	FOREIGN KEY(`input_comm`) REFERENCES `commodities`(`comm_name`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`),
	FOREIGN KEY(`vintage`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`output_comm`) REFERENCES `commodities`(`comm_name`)
);
CREATE TABLE "Output_VFlow_In" (
	`region`	text,
	`scenario`	text,
	`sector`	text,
	`t_periods`	integer,
	`t_season`	text,
	`t_day`	text,
	`input_comm`	text,
	`tech`	text,
	`vintage`	integer,
	`output_comm`	text,
	`vflow_in`	real,
	PRIMARY KEY(region,scenario,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm),
	FOREIGN KEY(`sector`) REFERENCES `sector_labels`(`sector`),
	FOREIGN KEY(`t_periods`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`t_season`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`t_day`) REFERENCES `time_of_day`(`t_day`),
	FOREIGN KEY(`input_comm`) REFERENCES `commodities`(`comm_name`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`),
	FOREIGN KEY(`vintage`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`output_comm`) REFERENCES `commodities`(`comm_name`)
);
CREATE TABLE Output_Objective (
   scenario text,
   objective_name text,
   total_system_cost real );
CREATE TABLE "Output_Emissions" (
	`region`	text,
	`scenario`	text,
	`sector`	text,
	`t_periods`	integer,
	`emissions_comm`	text,
	`tech`	text,
	`vintage`	integer,
	`emissions`	real,
	PRIMARY KEY(region,scenario,t_periods,emissions_comm,tech,vintage),
	FOREIGN KEY(`sector`) REFERENCES `sector_labels`(`sector`),
	FOREIGN KEY(`t_periods`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`emissions_comm`) REFERENCES `EmissionActivity`(`emis_comm`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`),
	FOREIGN KEY(`vintage`) REFERENCES `time_periods`(`t_periods`)
);
CREATE TABLE `Output_Curtailment` (
	`region`	text,
	`scenario`	text,
	`sector`	text,
	`t_periods`	integer,
	`t_season`	text,
	`t_day`	text,
	`input_comm`	text,
	`tech`	text,
	`vintage`	integer,
	`output_comm`	text,
	`curtailment`	real,
	PRIMARY KEY(`region`,`scenario`,`t_periods`,`t_season`,`t_day`,`input_comm`,`tech`,`vintage`,`output_comm`),
	FOREIGN KEY(`t_periods`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`t_season`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`t_day`) REFERENCES `time_of_day`(`t_day`),
	FOREIGN KEY(`input_comm`) REFERENCES `commodities`(`comm_name`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`),
	FOREIGN KEY(`vintage`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`output_comm`) REFERENCES `commodities`(`comm_name`)
);
CREATE TABLE "Output_Costs" (
	`region`	text,
	`scenario`	text,
	`sector`	text,
	`output_name`	text,
	`tech`	text,
	`vintage`	integer,
	`output_cost`	real,
	PRIMARY KEY(region,scenario,output_name,tech,vintage),
	FOREIGN KEY(`sector`) REFERENCES `sector_labels`(`sector`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`),
	FOREIGN KEY(`vintage`) REFERENCES `time_periods`(`t_periods`)
);
CREATE TABLE "Output_CapacityByPeriodAndTech" (
	`region`	text,
	`scenario`	text,
	`sector`	text,
	`t_periods`	integer,
	`tech`	text,
	`capacity`	real,
	PRIMARY KEY(region,scenario,t_periods,tech),
	FOREIGN KEY(`sector`) REFERENCES `sector_labels`(`sector`),
	FOREIGN KEY(`t_periods`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`)
);
CREATE TABLE `MinGenGroupWeight` (
	`tech`	text,
	`group_name`	text,
	`act_fraction`	REAL,
	`tech_desc`	text,
	`region`	text,
	PRIMARY KEY(`tech`,`group_name`)
);
CREATE TABLE `MinGenGroupTarget` (
	`period`	integer,
	`group_name`	text,
	`min_act_g`	real,
	`notes`	text,
	`region`	text,
	PRIMARY KEY(`period`,`group_name`)
);
CREATE TABLE "MinCapacity" (
	`region`	text,
	`periods`	integer,
	`tech`	text,
	`mincap`	real,
	`mincap_units`	text,
	`mincap_notes`	text,
	PRIMARY KEY(region,periods,tech),
	FOREIGN KEY(`periods`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`)
);
INSERT INTO `MinCapacity` (region,periods,tech,mincap,mincap_units,mincap_notes) VALUES ('utopia',1990,'E31',0.13,'','');
INSERT INTO `MinCapacity` (region,periods,tech,mincap,mincap_units,mincap_notes) VALUES ('utopia',2000,'E31',0.13,'','');
INSERT INTO `MinCapacity` (region,periods,tech,mincap,mincap_units,mincap_notes) VALUES ('utopia',2010,'E31',0.13,'','');
INSERT INTO `MinCapacity` (region,periods,tech,mincap,mincap_units,mincap_notes) VALUES ('utopia',1990,'SRE',0.1,'','');
CREATE TABLE "MinActivity" (
	`region`	text,
	`periods`	integer,
	`tech`	text,
	`minact`	real,
	`minact_units`	text,
	`minact_notes`	text,
	PRIMARY KEY(region,periods,tech),
	FOREIGN KEY(`periods`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`)
);
CREATE TABLE "MaxCapacity" (
	`region`	text,
	`periods`	integer,
	`tech`	text,
	`maxcap`	real,
	`maxcap_units`	text,
	`maxcap_notes`	text,
	PRIMARY KEY(region,periods,tech),
	FOREIGN KEY(`periods`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`)
);
INSERT INTO `MaxCapacity` (region,periods,tech,maxcap,maxcap_units,maxcap_notes) VALUES ('utopia',1990,'E31',0.13,'','');
INSERT INTO `MaxCapacity` (region,periods,tech,maxcap,maxcap_units,maxcap_notes) VALUES ('utopia',2000,'E31',0.17,'','');
INSERT INTO `MaxCapacity` (region,periods,tech,maxcap,maxcap_units,maxcap_notes) VALUES ('utopia',2010,'E31',0.21,'','');
INSERT INTO `MaxCapacity` (region,periods,tech,maxcap,maxcap_units,maxcap_notes) VALUES ('utopia',1990,'RHE',0.0,'','');
INSERT INTO `MaxCapacity` (region,periods,tech,maxcap,maxcap_units,maxcap_notes) VALUES ('utopia',1990,'TXD',0.6,'','');
INSERT INTO `MaxCapacity` (region,periods,tech,maxcap,maxcap_units,maxcap_notes) VALUES ('utopia',2000,'TXD',1.76,'','');
INSERT INTO `MaxCapacity` (region,periods,tech,maxcap,maxcap_units,maxcap_notes) VALUES ('utopia',2010,'TXD',4.76,'','');
CREATE TABLE "MaxActivity" (
	`region`	text,
	`periods`	integer,
	`tech`	text,
	`maxact`	real,
	`maxact_units`	text,
	`maxact_notes`	text,
	PRIMARY KEY(region,periods,tech),
	FOREIGN KEY(`periods`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`)
);
CREATE TABLE "LifetimeTech" (
	`region`	text,
	`tech`	text,
	`life`	real,
	`life_notes`	text,
	PRIMARY KEY(region,tech),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`)
);
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','E01',40.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','E21',40.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','E31',100.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','E51',100.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','E70',40.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','RHE',30.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','RHO',30.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','RL1',10.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','SRE',50.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','TXD',15.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','TXE',15.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','TXG',15.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','IMPDSL1',1000.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','IMPGSL1',1000.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','IMPHCO1',1000.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','IMPOIL1',1000.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','IMPURN1',1000.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','IMPHYD',1000.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('utopia','IMPFEQ',1000.0,'');
CREATE TABLE "LifetimeProcess" (
	`region`	text,
	`tech`	text,
	`vintage`	integer,
	`life_process`	real,
	`life_process_notes`	text,
	PRIMARY KEY(region,tech,vintage),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`),
	FOREIGN KEY(`vintage`) REFERENCES `time_periods`(`t_periods`)
);
INSERT INTO `LifetimeProcess` (region,tech,vintage,life_process,life_process_notes) VALUES ('utopia','RL1',1980,20.0,'#forexistingcap');
INSERT INTO `LifetimeProcess` (region,tech,vintage,life_process,life_process_notes) VALUES ('utopia','TXD',1970,30.0,'#forexistingcap');
INSERT INTO `LifetimeProcess` (region,tech,vintage,life_process,life_process_notes) VALUES ('utopia','TXD',1980,30.0,'#forexistingcap');
INSERT INTO `LifetimeProcess` (region,tech,vintage,life_process,life_process_notes) VALUES ('utopia','TXG',1970,30.0,'#forexistingcap');
INSERT INTO `LifetimeProcess` (region,tech,vintage,life_process,life_process_notes) VALUES ('utopia','TXG',1980,30.0,'#forexistingcap');
CREATE TABLE "LifetimeLoanTech" (
	`region`	text,
	`tech`	text,
	`loan`	real,
	`loan_notes`	text,
	PRIMARY KEY(region,tech),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`)
);
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('utopia','E01',40.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('utopia','E21',40.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('utopia','E31',100.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('utopia','E51',100.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('utopia','E70',40.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('utopia','RHE',30.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('utopia','RHO',30.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('utopia','RL1',10.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('utopia','SRE',50.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('utopia','TXD',15.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('utopia','TXE',15.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('utopia','TXG',15.0,'');
CREATE TABLE "GrowthRateSeed" (
	`region`	text,
	`tech`	text,
	`growthrate_seed`	real,
	`growthrate_seed_units`	text,
	`growthrate_seed_notes`	text,
	PRIMARY KEY(region,tech),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`)
);
CREATE TABLE "GrowthRateMax" (
	`region`	text,
	`tech`	text,
	`growthrate_max`	real,
	`growthrate_max_notes`	text,
	PRIMARY KEY(region,tech),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`)
);
CREATE TABLE GlobalDiscountRate (
   rate real );
INSERT INTO `GlobalDiscountRate` (rate) VALUES (0.05);
CREATE TABLE "ExistingCapacity" (
	`region`	text,
	`tech`	text,
	`vintage`	integer,
	`exist_cap`	real,
	`exist_cap_units`	text,
	`exist_cap_notes`	text,
	PRIMARY KEY(region,tech,vintage),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`),
	FOREIGN KEY(`vintage`) REFERENCES `time_periods`(`t_periods`)
);
INSERT INTO `ExistingCapacity` (region,tech,vintage,exist_cap,exist_cap_units,exist_cap_notes) VALUES ('utopia','E01',1960,0.175,'','');
INSERT INTO `ExistingCapacity` (region,tech,vintage,exist_cap,exist_cap_units,exist_cap_notes) VALUES ('utopia','E01',1970,0.175,'','');
INSERT INTO `ExistingCapacity` (region,tech,vintage,exist_cap,exist_cap_units,exist_cap_notes) VALUES ('utopia','E01',1980,0.15,'','');
INSERT INTO `ExistingCapacity` (region,tech,vintage,exist_cap,exist_cap_units,exist_cap_notes) VALUES ('utopia','E31',1980,0.1,'','');
INSERT INTO `ExistingCapacity` (region,tech,vintage,exist_cap,exist_cap_units,exist_cap_notes) VALUES ('utopia','E51',1980,0.5,'','');
INSERT INTO `ExistingCapacity` (region,tech,vintage,exist_cap,exist_cap_units,exist_cap_notes) VALUES ('utopia','E70',1960,0.05,'','');
INSERT INTO `ExistingCapacity` (region,tech,vintage,exist_cap,exist_cap_units,exist_cap_notes) VALUES ('utopia','E70',1970,0.05,'','');
INSERT INTO `ExistingCapacity` (region,tech,vintage,exist_cap,exist_cap_units,exist_cap_notes) VALUES ('utopia','E70',1980,0.2,'','');
INSERT INTO `ExistingCapacity` (region,tech,vintage,exist_cap,exist_cap_units,exist_cap_notes) VALUES ('utopia','RHO',1970,12.5,'','');
INSERT INTO `ExistingCapacity` (region,tech,vintage,exist_cap,exist_cap_units,exist_cap_notes) VALUES ('utopia','RHO',1980,12.5,'','');
INSERT INTO `ExistingCapacity` (region,tech,vintage,exist_cap,exist_cap_units,exist_cap_notes) VALUES ('utopia','RL1',1980,5.6,'','');
INSERT INTO `ExistingCapacity` (region,tech,vintage,exist_cap,exist_cap_units,exist_cap_notes) VALUES ('utopia','TXD',1970,0.4,'','');
INSERT INTO `ExistingCapacity` (region,tech,vintage,exist_cap,exist_cap_units,exist_cap_notes) VALUES ('utopia','TXD',1980,0.2,'','');
INSERT INTO `ExistingCapacity` (region,tech,vintage,exist_cap,exist_cap_units,exist_cap_notes) VALUES ('utopia','TXG',1970,3.1,'','');
INSERT INTO `ExistingCapacity` (region,tech,vintage,exist_cap,exist_cap_units,exist_cap_notes) VALUES ('utopia','TXG',1980,1.5,'','');
CREATE TABLE "EmissionLimit" (
	`region`	text,
	`periods`	integer,
	`emis_comm`	text,
	`emis_limit`	real,
	`emis_limit_units`	text,
	`emis_limit_notes`	text,
	PRIMARY KEY(region,periods,emis_comm),
	FOREIGN KEY(`periods`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`emis_comm`) REFERENCES `commodities`(`comm_name`)
);
CREATE TABLE "EmissionActivity" (
	`region`	text,
	`emis_comm`	text,
	`input_comm`	text,
	`tech`	text,
	`vintage`	integer,
	`output_comm`	text,
	`emis_act`	real,
	`emis_act_units`	text,
	`emis_act_notes`	text,
	PRIMARY KEY(region,emis_comm,input_comm,tech,vintage,output_comm),
	FOREIGN KEY(`emis_comm`) REFERENCES `commodities`(`comm_name`),
	FOREIGN KEY(`input_comm`) REFERENCES `commodities`(`comm_name`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`),
	FOREIGN KEY(`vintage`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`output_comm`) REFERENCES `commodities`(`comm_name`)
);
INSERT INTO `EmissionActivity` (region,emis_comm,input_comm,tech,vintage,output_comm,emis_act,emis_act_units,emis_act_notes) VALUES ('utopia','co2','ethos','IMPDSL1',1990,'DSL',0.075,'','');
INSERT INTO `EmissionActivity` (region,emis_comm,input_comm,tech,vintage,output_comm,emis_act,emis_act_units,emis_act_notes) VALUES ('utopia','co2','ethos','IMPGSL1',1990,'GSL',0.075,'','');
INSERT INTO `EmissionActivity` (region,emis_comm,input_comm,tech,vintage,output_comm,emis_act,emis_act_units,emis_act_notes) VALUES ('utopia','co2','ethos','IMPHCO1',1990,'HCO',0.089,'','');
INSERT INTO `EmissionActivity` (region,emis_comm,input_comm,tech,vintage,output_comm,emis_act,emis_act_units,emis_act_notes) VALUES ('utopia','co2','ethos','IMPOIL1',1990,'OIL',0.075,'','');
INSERT INTO `EmissionActivity` (region,emis_comm,input_comm,tech,vintage,output_comm,emis_act,emis_act_units,emis_act_notes) VALUES ('utopia','nox','DSL','TXD',1970,'TX',1.0,'','');
INSERT INTO `EmissionActivity` (region,emis_comm,input_comm,tech,vintage,output_comm,emis_act,emis_act_units,emis_act_notes) VALUES ('utopia','nox','DSL','TXD',1980,'TX',1.0,'','');
INSERT INTO `EmissionActivity` (region,emis_comm,input_comm,tech,vintage,output_comm,emis_act,emis_act_units,emis_act_notes) VALUES ('utopia','nox','DSL','TXD',1990,'TX',1.0,'','');
INSERT INTO `EmissionActivity` (region,emis_comm,input_comm,tech,vintage,output_comm,emis_act,emis_act_units,emis_act_notes) VALUES ('utopia','nox','DSL','TXD',2000,'TX',1.0,'','');
INSERT INTO `EmissionActivity` (region,emis_comm,input_comm,tech,vintage,output_comm,emis_act,emis_act_units,emis_act_notes) VALUES ('utopia','nox','DSL','TXD',2010,'TX',1.0,'','');
INSERT INTO `EmissionActivity` (region,emis_comm,input_comm,tech,vintage,output_comm,emis_act,emis_act_units,emis_act_notes) VALUES ('utopia','nox','GSL','TXG',1970,'TX',1.0,'','');
INSERT INTO `EmissionActivity` (region,emis_comm,input_comm,tech,vintage,output_comm,emis_act,emis_act_units,emis_act_notes) VALUES ('utopia','nox','GSL','TXG',1980,'TX',1.0,'','');
INSERT INTO `EmissionActivity` (region,emis_comm,input_comm,tech,vintage,output_comm,emis_act,emis_act_units,emis_act_notes) VALUES ('utopia','nox','GSL','TXG',1990,'TX',1.0,'','');
INSERT INTO `EmissionActivity` (region,emis_comm,input_comm,tech,vintage,output_comm,emis_act,emis_act_units,emis_act_notes) VALUES ('utopia','nox','GSL','TXG',2000,'TX',1.0,'','');
INSERT INTO `EmissionActivity` (region,emis_comm,input_comm,tech,vintage,output_comm,emis_act,emis_act_units,emis_act_notes) VALUES ('utopia','nox','GSL','TXG',2010,'TX',1.0,'','');
CREATE TABLE "Efficiency" (
	`region`	text,
	`input_comm`	text,
	`tech`	text,
	`vintage`	integer,
	`output_comm`	text,
	`efficiency`	real CHECK(efficiency > 0),
	`eff_notes`	text,
	PRIMARY KEY(region,input_comm,tech,vintage,output_comm),
	FOREIGN KEY(`input_comm`) REFERENCES `commodities`(`comm_name`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`),
	FOREIGN KEY(`vintage`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`output_comm`) REFERENCES `commodities`(`comm_name`)
);
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ethos','IMPDSL1',1990,'DSL',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ethos','IMPGSL1',1990,'GSL',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ethos','IMPHCO1',1990,'HCO',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ethos','IMPOIL1',1990,'OIL',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ethos','IMPURN1',1990,'URN',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ethos','IMPFEQ',1990,'FEQ',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ethos','IMPHYD',1990,'HYD',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','HCO','E01',1960,'ELC',0.32,'# 1/3.125');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','HCO','E01',1970,'ELC',0.32,'# 1/3.125');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','HCO','E01',1980,'ELC',0.32,'# 1/3.125');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','HCO','E01',1990,'ELC',0.32,'# 1/3.125');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','HCO','E01',2000,'ELC',0.32,'# 1/3.125');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','HCO','E01',2010,'ELC',0.32,'# 1/3.125');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','FEQ','E21',1990,'ELC',0.32,'# 1/3.125');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','FEQ','E21',2000,'ELC',0.32,'# 1/3.125');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','FEQ','E21',2010,'ELC',0.32,'# 1/3.125');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','URN','E21',1990,'ELC',0.4,'# 1/2.5');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','URN','E21',2000,'ELC',0.4,'# 1/2.5');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','URN','E21',2010,'ELC',0.4,'# 1/2.5');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','HYD','E31',1980,'ELC',0.32,'# 1/3.125');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','HYD','E31',1990,'ELC',0.32,'# 1/3.125');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','HYD','E31',2000,'ELC',0.32,'# 1/3.125');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','HYD','E31',2010,'ELC',0.32,'# 1/3.125');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','DSL','E70',1960,'ELC',0.294,'# 1/3.4');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','DSL','E70',1970,'ELC',0.294,'# 1/3.4');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','DSL','E70',1980,'ELC',0.294,'# 1/3.4');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','DSL','E70',1990,'ELC',0.294,'# 1/3.4');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','DSL','E70',2000,'ELC',0.294,'# 1/3.4');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','DSL','E70',2010,'ELC',0.294,'# 1/3.4');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ELC','E51',1980,'ELC',0.72,'# 1/1.3889');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ELC','E51',1990,'ELC',0.72,'# 1/1.3889');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ELC','E51',2000,'ELC',0.72,'# 1/1.3889');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ELC','E51',2010,'ELC',0.72,'# 1/1.3889');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ELC','RHE',1990,'RH',1.0,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ELC','RHE',2000,'RH',1.0,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ELC','RHE',2010,'RH',1.0,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','DSL','RHO',1970,'RH',0.7,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','DSL','RHO',1980,'RH',0.7,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','DSL','RHO',1990,'RH',0.7,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','DSL','RHO',2000,'RH',0.7,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','DSL','RHO',2010,'RH',0.7,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ELC','RL1',1980,'RL',1.0,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ELC','RL1',1990,'RL',1.0,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ELC','RL1',2000,'RL',1.0,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ELC','RL1',2010,'RL',1.0,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','OIL','SRE',1990,'DSL',1.0,'# direct translation from PRC_INP2, PRC_OUT');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','OIL','SRE',2000,'DSL',1.0,'# direct translation from PRC_INP2, PRC_OUT');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','OIL','SRE',2010,'DSL',1.0,'# direct translation from PRC_INP2, PRC_OUT');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','OIL','SRE',1990,'GSL',1.0,'# direct translation from PRC_INP2, PRC_OUT');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','OIL','SRE',2000,'GSL',1.0,'# direct translation from PRC_INP2, PRC_OUT');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','OIL','SRE',2010,'GSL',1.0,'# direct translation from PRC_INP2, PRC_OUT');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','DSL','TXD',1970,'TX',0.231,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','DSL','TXD',1980,'TX',0.231,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','DSL','TXD',1990,'TX',0.231,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','DSL','TXD',2000,'TX',0.231,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','DSL','TXD',2010,'TX',0.231,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ELC','TXE',1990,'TX',0.827,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ELC','TXE',2000,'TX',0.827,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','ELC','TXE',2010,'TX',0.827,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','GSL','TXG',1970,'TX',0.231,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','GSL','TXG',1980,'TX',0.231,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','GSL','TXG',1990,'TX',0.231,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','GSL','TXG',2000,'TX',0.231,'# direct translation from DMD_EFF');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('utopia','GSL','TXG',2010,'TX',0.231,'# direct translation from DMD_EFF');
CREATE TABLE "DiscountRate" (
	`region`	text,
	`tech`	text,
	`vintage`	integer,
	`tech_rate`	real,
	`tech_rate_notes`	text,
	PRIMARY KEY(region,tech,vintage),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`),
	FOREIGN KEY(`vintage`) REFERENCES `time_periods`(`t_periods`)
);
CREATE TABLE "DemandSpecificDistribution" (
	`region`	text,
	`season_name`	text,
	`time_of_day_name`	text,
	`demand_name`	text,
	`dds`	real CHECK(dds >= 0 AND dds <= 1),
	`dds_notes`	text,
	PRIMARY KEY(region,season_name,time_of_day_name,demand_name),
	FOREIGN KEY(`season_name`) REFERENCES `time_season`(`t_season`),
	FOREIGN KEY(`time_of_day_name`) REFERENCES `time_of_day`(`t_day`),
	FOREIGN KEY(`demand_name`) REFERENCES `commodities`(`comm_name`)
);
INSERT INTO `DemandSpecificDistribution` (region,season_name,time_of_day_name,demand_name,dds,dds_notes) VALUES ('utopia','inter','day','RH',0.12,'');
INSERT INTO `DemandSpecificDistribution` (region,season_name,time_of_day_name,demand_name,dds,dds_notes) VALUES ('utopia','inter','night','RH',0.06,'');
INSERT INTO `DemandSpecificDistribution` (region,season_name,time_of_day_name,demand_name,dds,dds_notes) VALUES ('utopia','winter','day','RH',0.5467,'');
INSERT INTO `DemandSpecificDistribution` (region,season_name,time_of_day_name,demand_name,dds,dds_notes) VALUES ('utopia','winter','night','RH',0.2733,'');
INSERT INTO `DemandSpecificDistribution` (region,season_name,time_of_day_name,demand_name,dds,dds_notes) VALUES ('utopia','inter','day','RL',0.15,'');
INSERT INTO `DemandSpecificDistribution` (region,season_name,time_of_day_name,demand_name,dds,dds_notes) VALUES ('utopia','inter','night','RL',0.05,'');
INSERT INTO `DemandSpecificDistribution` (region,season_name,time_of_day_name,demand_name,dds,dds_notes) VALUES ('utopia','summer','day','RL',0.15,'');
INSERT INTO `DemandSpecificDistribution` (region,season_name,time_of_day_name,demand_name,dds,dds_notes) VALUES ('utopia','summer','night','RL',0.05,'');
INSERT INTO `DemandSpecificDistribution` (region,season_name,time_of_day_name,demand_name,dds,dds_notes) VALUES ('utopia','winter','day','RL',0.5,'');
INSERT INTO `DemandSpecificDistribution` (region,season_name,time_of_day_name,demand_name,dds,dds_notes) VALUES ('utopia','winter','night','RL',0.1,'');
CREATE TABLE "Demand" (
	`region`	text,
	`periods`	integer,
	`demand_comm`	text,
	`demand`	real,
	`demand_units`	text,
	`demand_notes`	text,
	PRIMARY KEY(region,periods,demand_comm),
	FOREIGN KEY(`periods`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`demand_comm`) REFERENCES `commodities`(`comm_name`)
);
INSERT INTO `Demand` (region,periods,demand_comm,demand,demand_units,demand_notes) VALUES ('utopia',1990,'RH',25.2,'','');
INSERT INTO `Demand` (region,periods,demand_comm,demand,demand_units,demand_notes) VALUES ('utopia',2000,'RH',37.8,'','');
INSERT INTO `Demand` (region,periods,demand_comm,demand,demand_units,demand_notes) VALUES ('utopia',2010,'RH',56.7,'','');
INSERT INTO `Demand` (region,periods,demand_comm,demand,demand_units,demand_notes) VALUES ('utopia',1990,'RL',5.6,'','');
INSERT INTO `Demand` (region,periods,demand_comm,demand,demand_units,demand_notes) VALUES ('utopia',2000,'RL',8.4,'','');
INSERT INTO `Demand` (region,periods,demand_comm,demand,demand_units,demand_notes) VALUES ('utopia',2010,'RL',12.6,'','');
INSERT INTO `Demand` (region,periods,demand_comm,demand,demand_units,demand_notes) VALUES ('utopia',1990,'TX',5.2,'','');
INSERT INTO `Demand` (region,periods,demand_comm,demand,demand_units,demand_notes) VALUES ('utopia',2000,'TX',7.8,'','');
INSERT INTO `Demand` (region,periods,demand_comm,demand,demand_units,demand_notes) VALUES ('utopia',2010,'TX',11.69,'','');
CREATE TABLE "CostVariable" (
	`region`	text NOT NULL,
	`periods`	integer NOT NULL,
	`tech`	text NOT NULL,
	`vintage`	integer NOT NULL,
	`cost_variable`	real,
	`cost_variable_units`	text,
	`cost_variable_notes`	text,
	PRIMARY KEY(region,periods,tech,vintage),
	FOREIGN KEY(`periods`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`),
	FOREIGN KEY(`vintage`) REFERENCES `time_periods`(`t_periods`)
);
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',1990,'IMPDSL1',1990,10.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2000,'IMPDSL1',1990,10.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'IMPDSL1',1990,10.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',1990,'IMPGSL1',1990,15.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2000,'IMPGSL1',1990,15.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'IMPGSL1',1990,15.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',1990,'IMPHCO1',1990,2.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2000,'IMPHCO1',1990,2.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'IMPHCO1',1990,2.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',1990,'IMPOIL1',1990,8.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2000,'IMPOIL1',1990,8.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'IMPOIL1',1990,8.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',1990,'IMPURN1',1990,2.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2000,'IMPURN1',1990,2.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'IMPURN1',1990,2.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',1990,'E01',1960,0.3,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',1990,'E01',1970,0.3,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',1990,'E01',1980,0.3,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',1990,'E01',1990,0.3,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2000,'E01',1970,0.3,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2000,'E01',1980,0.3,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2000,'E01',1990,0.3,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2000,'E01',2000,0.3,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'E01',1980,0.3,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'E01',1990,0.3,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'E01',2000,0.3,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'E01',2010,0.3,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',1990,'E21',1990,1.5,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2000,'E21',1990,1.5,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'E21',1990,1.5,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2000,'E21',2000,1.5,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'E21',2000,1.5,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'E21',2010,1.5,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',1990,'E70',1960,0.4,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',1990,'E70',1970,0.4,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',1990,'E70',1980,0.4,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',1990,'E70',1990,0.4,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2000,'E70',1970,0.4,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2000,'E70',1980,0.4,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2000,'E70',1990,0.4,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2000,'E70',2000,0.4,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'E70',1980,0.4,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'E70',1990,0.4,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'E70',2000,0.4,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'E70',2010,0.4,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',1990,'SRE',1990,10.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2000,'SRE',1990,10.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2000,'SRE',2000,10.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'SRE',1990,10.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'SRE',2000,10.0,'','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('utopia',2010,'SRE',2010,10.0,'','');
CREATE TABLE "CostInvest" (
	`region`	text,
	`tech`	text,
	`vintage`	integer,
	`cost_invest`	real,
	`cost_invest_units`	text,
	`cost_invest_notes`	text,
	PRIMARY KEY(region,tech,vintage),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`),
	FOREIGN KEY(`vintage`) REFERENCES `time_periods`(`t_periods`)
);
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','E01',1990,2000.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','E01',2000,1300.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','E01',2010,1200.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','E21',1990,5000.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','E21',2000,5000.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','E21',2010,5000.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','E31',1990,3000.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','E31',2000,3000.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','E31',2010,3000.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','E51',1990,900.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','E51',2000,900.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','E51',2010,900.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','E70',1990,1000.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','E70',2000,1000.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','E70',2010,1000.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','RHE',1990,90.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','RHE',2000,90.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','RHE',2010,90.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','RHO',1990,100.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','RHO',2000,100.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','RHO',2010,100.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','SRE',1990,100.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','SRE',2000,100.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','SRE',2010,100.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','TXD',1990,1044.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','TXD',2000,1044.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','TXD',2010,1044.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','TXE',1990,2000.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','TXE',2000,1750.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','TXE',2010,1500.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','TXG',1990,1044.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','TXG',2000,1044.0,'','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('utopia','TXG',2010,1044.0,'','');
CREATE TABLE "CostFixed" (
	`region`	text NOT NULL,
	`periods`	integer NOT NULL,
	`tech`	text NOT NULL,
	`vintage`	integer NOT NULL,
	`cost_fixed`	real,
	`cost_fixed_units`	text,
	`cost_fixed_notes`	text,
	PRIMARY KEY(region,periods,tech,vintage),
	FOREIGN KEY(`periods`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`),
	FOREIGN KEY(`vintage`) REFERENCES `time_periods`(`t_periods`)
);
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'E01',1960,40.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'E01',1970,40.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'E01',1980,40.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'E01',1990,40.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'E01',1970,70.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'E01',1980,70.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'E01',1990,70.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'E01',2000,70.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E01',1980,100.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E01',1990,100.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E01',2000,100.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E01',2010,100.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'E21',1990,500.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'E21',1990,500.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E21',1990,500.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'E21',2000,500.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E21',2000,500.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E21',2010,500.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'E31',1980,75.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'E31',1990,75.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'E31',1980,75.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'E31',1990,75.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'E31',2000,75.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E31',1980,75.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E31',1990,75.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E31',2000,75.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E31',2010,75.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'E51',1980,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'E51',1990,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'E51',1980,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'E51',1990,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'E51',2000,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E51',1980,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E51',1990,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E51',2000,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E51',2010,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'E70',1960,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'E70',1970,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'E70',1980,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'E70',1990,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'E70',1970,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'E70',1980,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'E70',1990,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'E70',2000,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E70',1980,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E70',1990,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E70',2000,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'E70',2010,30.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'RHO',1970,1.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'RHO',1980,1.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'RHO',1990,1.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'RHO',1980,1.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'RHO',1990,1.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'RHO',2000,1.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'RHO',1990,1.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'RHO',2000,1.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'RHO',2010,1.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'RL1',1980,9.46,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'RL1',1990,9.46,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'RL1',2000,9.46,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'RL1',2010,9.46,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'TXD',1970,52.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'TXD',1980,52.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'TXD',1990,52.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'TXD',1980,52.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'TXD',1990,52.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'TXD',2000,52.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'TXD',2000,52.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'TXD',2010,52.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'TXE',1990,100.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'TXE',1990,90.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'TXE',2000,90.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'TXE',2000,80.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'TXE',2010,80.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'TXG',1970,48.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'TXG',1980,48.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',1990,'TXG',1990,48.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'TXG',1980,48.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'TXG',1990,48.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2000,'TXG',2000,48.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'TXG',2000,48.0,'','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('utopia',2010,'TXG',2010,48.0,'','');
CREATE TABLE "CapacityToActivity" (
	`region`	text,
	`tech`	text,
	`c2a`	real,
	`c2a_notes`	TEXT,
	PRIMARY KEY(region,tech),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`)
);
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('utopia','E01',31.54,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('utopia','E21',31.54,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('utopia','E31',31.54,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('utopia','E51',31.54,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('utopia','E70',31.54,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('utopia','RHE',1.0,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('utopia','RHO',1.0,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('utopia','RL1',1.0,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('utopia','SRE',1.0,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('utopia','TXD',1.0,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('utopia','TXE',1.0,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('utopia','TXG',1.0,'');
CREATE TABLE "CapacityFactorTech" (
	`region`	text,
	`season_name`	text,
	`time_of_day_name`	text,
	`tech`	text,
	`cf_tech`	real CHECK(cf_tech >= 0 AND cf_tech <= 1),
	`cf_tech_notes`	text,
	PRIMARY KEY(region,season_name,time_of_day_name,tech),
	FOREIGN KEY(`season_name`) REFERENCES `time_season`(`t_season`),
	FOREIGN KEY(`time_of_day_name`) REFERENCES `time_of_day`(`t_day`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`)
);
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','inter','day','E01',0.8,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','inter','night','E01',0.8,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','winter','day','E01',0.8,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','winter','night','E01',0.8,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','summer','day','E01',0.8,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','summer','night','E01',0.8,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','inter','day','E21',0.8,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','inter','night','E21',0.8,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','winter','day','E21',0.8,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','winter','night','E21',0.8,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','summer','day','E21',0.8,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','summer','night','E21',0.8,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','inter','day','E31',0.275,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','inter','night','E31',0.275,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','winter','day','E31',0.275,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','winter','night','E31',0.275,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','summer','day','E31',0.275,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','summer','night','E31',0.275,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','inter','day','E51',0.17,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','inter','night','E51',0.17,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','winter','day','E51',0.17,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','winter','night','E51',0.17,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','summer','day','E51',0.17,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','summer','night','E51',0.17,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','inter','day','E70',0.8,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','inter','night','E70',0.8,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','winter','day','E70',0.8,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','winter','night','E70',0.8,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','summer','day','E70',0.8,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('utopia','summer','night','E70',0.8,'');
CREATE TABLE "CapacityFactorProcess" (
	`region`	text,
	`season_name`	text,
	`time_of_day_name`	text,
	`tech`	text,
	`vintage`	integer,
	`cf_process`	real CHECK(cf_process >= 0 AND cf_process <= 1),
	`cf_process_notes`	text,
	PRIMARY KEY(region,season_name,time_of_day_name,tech,vintage),
	FOREIGN KEY(`season_name`) REFERENCES `time_season`(`t_season`),
	FOREIGN KEY(`time_of_day_name`) REFERENCES `time_of_day`(`t_day`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`)
);
INSERT INTO `CapacityFactorProcess` (region,season_name,time_of_day_name,tech,vintage,cf_process,cf_process_notes) VALUES ('utopia','inter','day','E31',2000,0.2753,'');
INSERT INTO `CapacityFactorProcess` (region,season_name,time_of_day_name,tech,vintage,cf_process,cf_process_notes) VALUES ('utopia','inter','night','E31',2000,0.2753,'');
INSERT INTO `CapacityFactorProcess` (region,season_name,time_of_day_name,tech,vintage,cf_process,cf_process_notes) VALUES ('utopia','winter','day','E31',2000,0.2753,'');
INSERT INTO `CapacityFactorProcess` (region,season_name,time_of_day_name,tech,vintage,cf_process,cf_process_notes) VALUES ('utopia','winter','night','E31',2000,0.2753,'');
INSERT INTO `CapacityFactorProcess` (region,season_name,time_of_day_name,tech,vintage,cf_process,cf_process_notes) VALUES ('utopia','summer','day','E31',2000,0.2753,'');
INSERT INTO `CapacityFactorProcess` (region,season_name,time_of_day_name,tech,vintage,cf_process,cf_process_notes) VALUES ('utopia','summer','night','E31',2000,0.2753,'');
INSERT INTO `CapacityFactorProcess` (region,season_name,time_of_day_name,tech,vintage,cf_process,cf_process_notes) VALUES ('utopia','inter','day','E31',2010,0.2756,'');
INSERT INTO `CapacityFactorProcess` (region,season_name,time_of_day_name,tech,vintage,cf_process,cf_process_notes) VALUES ('utopia','inter','night','E31',2010,0.2756,'');
INSERT INTO `CapacityFactorProcess` (region,season_name,time_of_day_name,tech,vintage,cf_process,cf_process_notes) VALUES ('utopia','winter','day','E31',2010,0.2756,'');
INSERT INTO `CapacityFactorProcess` (region,season_name,time_of_day_name,tech,vintage,cf_process,cf_process_notes) VALUES ('utopia','winter','night','E31',2010,0.2756,'');
INSERT INTO `CapacityFactorProcess` (region,season_name,time_of_day_name,tech,vintage,cf_process,cf_process_notes) VALUES ('utopia','summer','day','E31',2010,0.2756,'');
INSERT INTO `CapacityFactorProcess` (region,season_name,time_of_day_name,tech,vintage,cf_process,cf_process_notes) VALUES ('utopia','summer','night','E31',2010,0.2756,'');
CREATE TABLE `CapacityCredit` (
	`region`	text,
	`periods`	integer,
	`tech`	text,
	`cf_tech`	real CHECK(cf_tech >= 0 AND cf_tech <= 1),
	`cf_tech_notes`	text,
	PRIMARY KEY(`region`,`periods`,`tech`)
);
COMMIT;
