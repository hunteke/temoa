BEGIN TRANSACTION;


/*
-------------------------------------------------------
Tables in this section correspond to Sets
-------------------------------------------------------
*/

-- User-defined flags to split set elements into proper subsets
CREATE TABLE time_period_labels (
  t_period_labels text primary key,
  t_period_labels_desc text);
INSERT INTO "time_period_labels" VALUES('e', 'existing vintages');
INSERT INTO "time_period_labels" VALUES('f', 'future');


CREATE TABLE technology_labels (
  tech_labels text primary key,
  tech_labels_desc text);
INSERT INTO "technology_labels" VALUES('r', 'resource technology');
INSERT INTO "technology_labels" VALUES('p', 'production technology');
INSERT INTO "technology_labels" VALUES('pb', 'baseload production technology');
INSERT INTO "technology_labels" VALUES('ps', 'storage production technology');


CREATE TABLE commodity_labels (
  comm_labels text primary key,
  comm_labels_desc text);
INSERT INTO "commodity_labels" VALUES('p', 'physical commodity');
INSERT INTO "commodity_labels" VALUES('e', 'emissions commodity');
INSERT INTO "commodity_labels" VALUES('d', 'demand commodity');


CREATE TABLE sector_labels (
  sector text primary key);
INSERT INTO "sector_labels" VALUES('supply');
INSERT INTO "sector_labels" VALUES('electric');
INSERT INTO "sector_labels" VALUES('transport');
INSERT INTO "sector_labels" VALUES('commercial');
INSERT INTO "sector_labels" VALUES('residential');
INSERT INTO "sector_labels" VALUES('industrial');


--Tables below correspond to Temoa sets
CREATE TABLE time_periods (
  t_periods integer primary key,
  flag text,
  FOREIGN KEY(flag) REFERENCES time_period_labels(t_period_labels));  
INSERT INTO "time_periods" VALUES(2015,'e');
INSERT INTO "time_periods" VALUES(2020,'f');
INSERT INTO "time_periods" VALUES(2025,'f');
INSERT INTO "time_periods" VALUES(2030,'f');
INSERT INTO "time_periods" VALUES(2035,'f');


CREATE TABLE time_season (
  t_season text primary key );
INSERT INTO "time_season" VALUES('spring');
INSERT INTO "time_season" VALUES('summer');
INSERT INTO "time_season" VALUES('fall');
INSERT INTO "time_season" VALUES('winter');


CREATE TABLE time_of_day (
  t_day text primary key );
INSERT INTO "time_of_day" VALUES('day');
INSERT INTO "time_of_day" VALUES('night');


CREATE TABLE technologies (
  tech text primary key,
  flag text,
  sector text,
  tech_desc text,
  tech_category text,
  FOREIGN KEY(flag) REFERENCES technology_labels(tech_labels),
  FOREIGN KEY(sector) REFERENCES sector_labels(sector));
INSERT INTO "technologies" VALUES('S_IMPETH','r','supply',' imported ethanol','');
INSERT INTO "technologies" VALUES('S_IMPOIL','r','supply',' imported crude oil','');
INSERT INTO "technologies" VALUES('S_IMPNG','r','supply',' imported natural gas','');
INSERT INTO "technologies" VALUES('S_IMPURN','r','supply',' imported uranium','');
INSERT INTO "technologies" VALUES('S_OILREF','p','supply',' crude oil refinery','');
INSERT INTO "technologies" VALUES('E_NGCC','p','electric',' natural gas combined-cycle','');
INSERT INTO "technologies" VALUES('E_SOLPV','p','electric',' solar photovoltaic','');
INSERT INTO "technologies" VALUES('E_BATT','ps','electric',' lithium-ion battery','');
INSERT INTO "technologies" VALUES('E_NUCLEAR','pb','electric',' nuclear power plant','');
INSERT INTO "technologies" VALUES('T_BLND','p','transport','ethanol - gasoline blending process','');
INSERT INTO "technologies" VALUES('T_DSL','p','transport','diesel vehicle','');
INSERT INTO "technologies" VALUES('T_GSL','p','transport','gasoline vehicle','');
INSERT INTO "technologies" VALUES('T_EV','p','transport','electric vehicle','');
INSERT INTO "technologies" VALUES('R_EH','p','residential',' electric residential heating','');
INSERT INTO "technologies" VALUES('R_NGH','p','residential',' natural gas residential heating','');


--can include a column that designates the commodity type (physical, emissions, demand)
CREATE TABLE commodities (
  comm_name text primary key,
  flag text,  
  comm_desc text,
  FOREIGN KEY(flag) REFERENCES commodity_labels(comm_labels));
INSERT INTO "commodities" VALUES('ethos','p','dummy commodity to supply inputs (makes graph easier to read)');
INSERT INTO "commodities" VALUES('OIL','p','crude oil');
INSERT INTO "commodities" VALUES('NG','p','natural gas');
INSERT INTO "commodities" VALUES('URN','p','uranium');
INSERT INTO "commodities" VALUES('ETH','p','ethanol');
INSERT INTO "commodities" VALUES('SOL','p','solar insolation');
INSERT INTO "commodities" VALUES('GSL','p','gasoline');
INSERT INTO "commodities" VALUES('DSL','p','diesel');
INSERT INTO "commodities" VALUES('ELC','p','electricity');
INSERT INTO "commodities" VALUES('E10','p','gasoline blend with 10% ethanol');
INSERT INTO "commodities" VALUES('VMT','d','travel demand for vehicle-miles traveled');
INSERT INTO "commodities" VALUES('RH','d','demand for residential heating');
INSERT INTO "commodities" VALUES('CO2','e','CO2 emissions commodity');


/*
-------------------------------------------------------
Tables in this section correspond to Parameters
-------------------------------------------------------
*/

CREATE TABLE SegFrac (
   season_name text,
   time_of_day_name text,
   segfrac real check (segfrac>=0 AND segfrac<=1),
   segfrac_notes text,
   PRIMARY KEY(season_name, time_of_day_name), --here's where I define primary key as a combo of columns
   FOREIGN KEY(season_name) REFERENCES time_season(t_season),
   FOREIGN KEY(time_of_day_name) REFERENCES time_of_day(t_day) );
INSERT INTO "SegFrac" VALUES('spring','day',0.125,'Spring - Day');
INSERT INTO "SegFrac" VALUES('spring','night',0.125,'Spring - Night');
INSERT INTO "SegFrac" VALUES('summer','day',0.125,'Summer - Day');
INSERT INTO "SegFrac" VALUES('summer','night',0.125,'Summer - Night');
INSERT INTO "SegFrac" VALUES('fall','day',0.125,'Fall - Day');
INSERT INTO "SegFrac" VALUES('fall','night',0.125,'Fall - Night');
INSERT INTO "SegFrac" VALUES('winter','day',0.125,'Winter - Day');
INSERT INTO "SegFrac" VALUES('winter','night',0.125,'Winter - Night');
	

CREATE TABLE Demand (
   periods integer,
   demand_comm text,
   demand real,
   demand_units text,
   demand_notes text,
   PRIMARY KEY(periods, demand_comm),
   FOREIGN KEY(periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(demand_comm) REFERENCES commodities(comm_name) );
INSERT INTO "Demand" VALUES(2020,'RH',100,'','');
INSERT INTO "Demand" VALUES(2025,'RH',110,'','');
INSERT INTO "Demand" VALUES(2030,'RH',120,'','');
INSERT INTO "Demand" VALUES(2020,'VMT',120,'','');
INSERT INTO "Demand" VALUES(2025,'VMT',130,'','');
INSERT INTO "Demand" VALUES(2030,'VMT',140,'','');


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
INSERT INTO "DemandSpecificDistribution" VALUES('spring','day','RH',0.05,'');
INSERT INTO "DemandSpecificDistribution" VALUES('spring','night','RH',0.10,'');
INSERT INTO "DemandSpecificDistribution" VALUES('summer','day','RH',0,'');
INSERT INTO "DemandSpecificDistribution" VALUES('summer','night','RH',0,'');
INSERT INTO "DemandSpecificDistribution" VALUES('fall','day','RH',0.05,'');
INSERT INTO "DemandSpecificDistribution" VALUES('fall','night','RH',0.10,'');
INSERT INTO "DemandSpecificDistribution" VALUES('winter','day','RH',0.30,'');
INSERT INTO "DemandSpecificDistribution" VALUES('winter','night','RH',0.40,'');


CREATE TABLE CapacityToActivity (
   tech text primary key,
   c2a real,
   c2a_notes,
   FOREIGN KEY(tech) REFERENCES technologies(tech) );
INSERT INTO "CapacityToActivity" VALUES('S_IMPETH',1,'');
INSERT INTO "CapacityToActivity" VALUES('S_IMPOIL',1,'');
INSERT INTO "CapacityToActivity" VALUES('S_IMPNG',1,'');
INSERT INTO "CapacityToActivity" VALUES('S_IMPURN',1,'');
INSERT INTO "CapacityToActivity" VALUES('S_OILREF',1,'');
INSERT INTO "CapacityToActivity" VALUES('E_NGCC',31.54,'');
INSERT INTO "CapacityToActivity" VALUES('E_SOLPV',31.54,'');
INSERT INTO "CapacityToActivity" VALUES('E_BATT',31.54,'');
INSERT INTO "CapacityToActivity" VALUES('E_NUCLEAR',31.54,'');
INSERT INTO "CapacityToActivity" VALUES('T_BLND',1,'');
INSERT INTO "CapacityToActivity" VALUES('T_DSL',1,'');
INSERT INTO "CapacityToActivity" VALUES('T_GSL',1,'');
INSERT INTO "CapacityToActivity" VALUES('T_EV',1,'');
INSERT INTO "CapacityToActivity" VALUES('R_EH',1,'');
INSERT INTO "CapacityToActivity" VALUES('R_NGH',1,'');


CREATE TABLE `tech_curtailment` (
	`technology`	text,
	PRIMARY KEY(technology),
	FOREIGN KEY(`technology`) REFERENCES `technologies`(`tech`)
);
INSERT INTO `tech_curtailment` (technology) VALUES ('S_OILREF');


CREATE TABLE GlobalDiscountRate (
   rate real );
INSERT INTO "GlobalDiscountRate" VALUES(0.05);


CREATE TABLE DiscountRate (
   tech text,
   vintage integer,
   tech_rate real,
   tech_rate_notes text,
   PRIMARY KEY(tech, vintage),
   FOREIGN KEY(tech) REFERENCES technologies(tech),
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods));


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
INSERT INTO "EmissionActivity" VALUES('CO2','ethos','S_IMPNG',2020,'NG',50.3,'kT/PJ','taken from MIT Energy Fact Sheet');
INSERT INTO "EmissionActivity" VALUES('CO2','OIL','S_OILREF',2020,'GSL',67.2,'kT/PJ','taken from MIT Energy Fact Sheet');
INSERT INTO "EmissionActivity" VALUES('CO2','OIL','S_OILREF',2020,'DSL',69.4,'kT/PJ','taken from MIT Energy Fact Sheet');


CREATE TABLE EmissionLimit  (
   periods integer,
   emis_comm text,
   emis_limit real,
   emis_limit_units text,
   emis_limit_notes text,
   PRIMARY KEY(periods, emis_comm),
   FOREIGN KEY(periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(emis_comm) REFERENCES commodities(comm_name) );
INSERT INTO "EmissionLimit" VALUES(2020,'CO2', 25000,'kT CO2','');
INSERT INTO "EmissionLimit" VALUES(2025,'CO2', 24000,'kT CO2','');
INSERT INTO "EmissionLimit" VALUES(2030,'CO2', 23000,'kT CO2','');


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
 INSERT INTO "TechInputSplit" VALUES('2020','GSL','T_BLND',0.9,'');
 INSERT INTO "TechInputSplit" VALUES('2020','ETH','T_BLND',0.1,'');
 INSERT INTO "TechInputSplit" VALUES('2025','GSL','T_BLND',0.9,'');
 INSERT INTO "TechInputSplit" VALUES('2025','ETH','T_BLND',0.1,'');
  INSERT INTO "TechInputSplit" VALUES('2030','GSL','T_BLND',0.9,'');
 INSERT INTO "TechInputSplit" VALUES('2030','ETH','T_BLND',0.1,'');


CREATE TABLE TechOutputSplit (
   periods integer,
   tech text,
   output_comm text,
   to_split real,
   to_split_notes text,
   PRIMARY KEY(periods, tech, output_comm),
   FOREIGN KEY(periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(tech) REFERENCES technologies(tech),
   FOREIGN KEY(output_comm) REFERENCES commodities(comm_name) );
 INSERT INTO "TechOutputSplit" VALUES('2020','S_OILREF','GSL',0.90,'');
  INSERT INTO "TechOutputSplit" VALUES('2020','S_OILREF','DSL',0.10,'');
 INSERT INTO "TechOutputSplit" VALUES('2025','S_OILREF','GSL',0.90,'');
  INSERT INTO "TechOutputSplit" VALUES('2025','S_OILREF','DSL',0.10,'');
 INSERT INTO "TechOutputSplit" VALUES('2030','S_OILREF','GSL',0.90,'');
  INSERT INTO "TechOutputSplit" VALUES('2030','S_OILREF','DSL',0.10,'');


CREATE TABLE MinCapacity (
   periods integer,
   tech text,
   mincap real,
   mincap_units text,
   mincap_notes text,
   PRIMARY KEY(periods, tech),
   FOREIGN KEY(periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(tech) REFERENCES technologies(tech) );
	

CREATE TABLE MaxCapacity (
   periods integer,
   tech text,
   maxcap real,
   maxcap_units text,
   maxcap_notes text,
   PRIMARY KEY(periods, tech),
   FOREIGN KEY(periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(tech) REFERENCES technologies(tech) );


CREATE TABLE MinActivity (
   periods integer,
   tech text,
   minact real,
   minact_units text,
   minact_notes text,
   PRIMARY KEY(periods, tech),
   FOREIGN KEY(periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(tech) REFERENCES technologies(tech) ); 
 INSERT INTO "MinActivity" VALUES(2020,'T_GSL',50,'','');   
 INSERT INTO "MinActivity" VALUES(2025,'T_GSL',50,'','');   
 INSERT INTO "MinActivity" VALUES(2030,'T_GSL',50,'',''); 


CREATE TABLE MaxActivity (
   periods integer,
   tech text,
   maxact real,
   maxact_units text,
   maxact_notes text,
   PRIMARY KEY(periods, tech),
   FOREIGN KEY(periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(tech) REFERENCES technologies(tech) );


CREATE TABLE GrowthRateMax (
   tech text,
   growthrate_max real,
   growthrate_max_notes text,
   FOREIGN KEY(tech) REFERENCES technologies(tech) );


CREATE TABLE GrowthRateSeed (
   tech text,
   growthrate_seed real,
   growthrate_seed_units text,
   growthrate_seed_notes text,
   FOREIGN KEY(tech) REFERENCES technologies(tech) );	

 
CREATE TABLE  LifetimeTech (
   tech text,
   life real,
   life_notes text,
   PRIMARY KEY(tech),
   FOREIGN KEY(tech) REFERENCES technologies(tech) );
INSERT INTO "LifetimeTech" VALUES('S_IMPETH',100,'');
INSERT INTO "LifetimeTech" VALUES('S_IMPOIL',100,'');
INSERT INTO "LifetimeTech" VALUES('S_IMPNG',100,'');
INSERT INTO "LifetimeTech" VALUES('S_IMPURN',100,'');
INSERT INTO "LifetimeTech" VALUES('S_OILREF',100,'');
INSERT INTO "LifetimeTech" VALUES('E_NGCC',30,'');
INSERT INTO "LifetimeTech" VALUES('E_SOLPV',30,'');
INSERT INTO "LifetimeTech" VALUES('E_BATT',20,'');
INSERT INTO "LifetimeTech" VALUES('E_NUCLEAR',50,'');
INSERT INTO "LifetimeTech" VALUES('T_BLND',100,'');
INSERT INTO "LifetimeTech" VALUES('T_DSL',12,'');
INSERT INTO "LifetimeTech" VALUES('T_GSL',12,'');
INSERT INTO "LifetimeTech" VALUES('T_EV',12,'');
INSERT INTO "LifetimeTech" VALUES('R_EH',20,'');
INSERT INTO "LifetimeTech" VALUES('R_NGH',20,'');


CREATE TABLE LifetimeProcess (
   tech text,
   vintage integer,
   life_process real,
   life_process_notes text,
   PRIMARY KEY(tech, vintage),
   FOREIGN KEY(tech) REFERENCES technologies(tech),
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods) );

	
CREATE TABLE LifetimeLoanTech (
   tech text,
   loan real,
   loan_notes text,
   PRIMARY KEY(tech),
   FOREIGN KEY(tech) REFERENCES technologies(tech) );
INSERT INTO "LifetimeLoanTech" VALUES('S_IMPETH',100,'');
INSERT INTO "LifetimeLoanTech" VALUES('S_IMPOIL',100,'');
INSERT INTO "LifetimeLoanTech" VALUES('S_IMPNG',100,'');
INSERT INTO "LifetimeLoanTech" VALUES('S_IMPURN',100,'');
INSERT INTO "LifetimeLoanTech" VALUES('S_OILREF',100,'');
INSERT INTO "LifetimeLoanTech" VALUES('E_NGCC',30,'');
INSERT INTO "LifetimeLoanTech" VALUES('E_SOLPV',30,'');
INSERT INTO "LifetimeLoanTech" VALUES('E_BATT',20,'');
INSERT INTO "LifetimeLoanTech" VALUES('E_NUCLEAR',50,'');
INSERT INTO "LifetimeLoanTech" VALUES('T_BLND',100,'');
INSERT INTO "LifetimeLoanTech" VALUES('T_DSL',12,'');
INSERT INTO "LifetimeLoanTech" VALUES('T_GSL',12,'');
INSERT INTO "LifetimeLoanTech" VALUES('T_EV',12,'');
INSERT INTO "LifetimeLoanTech" VALUES('R_EH',20,'');
INSERT INTO "LifetimeLoanTech" VALUES('R_NGH',20,'');


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
/* Default value is 1 as defined in temoa_model.py */
INSERT INTO "CapacityFactorTech" VALUES('spring','day','E_SOLPV',0.60,'');
INSERT INTO "CapacityFactorTech" VALUES('spring','night','E_SOLPV',0.0,'');
INSERT INTO "CapacityFactorTech" VALUES('summer','day','E_SOLPV',0.60,'');
INSERT INTO "CapacityFactorTech" VALUES('summer','night','E_SOLPV',0.00,'');
INSERT INTO "CapacityFactorTech" VALUES('fall','day','E_SOLPV',0.60,'');
INSERT INTO "CapacityFactorTech" VALUES('fall','night','E_SOLPV',0.0,'');
INSERT INTO "CapacityFactorTech" VALUES('winter','day','E_SOLPV',0.60,'');
INSERT INTO "CapacityFactorTech" VALUES('winter','night','E_SOLPV',0.0,'');


CREATE TABLE StorageDuration (
   tech text,
   duration real,
   duration_notes text,
   PRIMARY KEY(tech) );
INSERT INTO "StorageDuration" VALUES ('E_BATT',8,'8-hour duration specified as fraction of a day');

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
INSERT INTO "Efficiency" VALUES('ethos','S_IMPETH',2020,'ETH',1.00,'');
INSERT INTO "Efficiency" VALUES('ethos','S_IMPOIL',2020,'OIL',1.00,'');
INSERT INTO "Efficiency" VALUES('ethos','S_IMPNG',2020,'NG',1.00,'');
INSERT INTO "Efficiency" VALUES('ethos','S_IMPURN',2020,'URN',1.00,'');
INSERT INTO "Efficiency" VALUES('OIL','S_OILREF',2020,'GSL',1.00,'');
INSERT INTO "Efficiency" VALUES('OIL','S_OILREF',2020,'DSL',1.00,'');
INSERT INTO "Efficiency" VALUES('ETH','T_BLND',2020,'E10',1.00,'');
INSERT INTO "Efficiency" VALUES('GSL','T_BLND',2020,'E10',1.00,'');
INSERT INTO "Efficiency" VALUES('NG','E_NGCC',2020,'ELC',0.55,'');
INSERT INTO "Efficiency" VALUES('NG','E_NGCC',2025,'ELC',0.55,'');
INSERT INTO "Efficiency" VALUES('NG','E_NGCC',2030,'ELC',0.55,'');
INSERT INTO "Efficiency" VALUES('SOL','E_SOLPV',2020,'ELC',1.0,'');
INSERT INTO "Efficiency" VALUES('SOL','E_SOLPV',2025,'ELC',1.0,'');
INSERT INTO "Efficiency" VALUES('SOL','E_SOLPV',2030,'ELC',1.0,'');
INSERT INTO "Efficiency" VALUES('URN','E_NUCLEAR',2015,'ELC',0.4,'');
INSERT INTO "Efficiency" VALUES('URN','E_NUCLEAR',2020,'ELC',0.4,'');
INSERT INTO "Efficiency" VALUES('URN','E_NUCLEAR',2025,'ELC',0.4,'');
INSERT INTO "Efficiency" VALUES('URN','E_NUCLEAR',2030,'ELC',0.4,'');
INSERT INTO "Efficiency" VALUES('ELC','E_BATT',2020,'ELC',0.85,'');
INSERT INTO "Efficiency" VALUES('ELC','E_BATT',2025,'ELC',0.85,'');
INSERT INTO "Efficiency" VALUES('ELC','E_BATT',2030,'ELC',0.85,'');
INSERT INTO "Efficiency" VALUES('E10','T_GSL',2020,'VMT',0.25,'');
INSERT INTO "Efficiency" VALUES('E10','T_GSL',2025,'VMT',0.25,'');
INSERT INTO "Efficiency" VALUES('E10','T_GSL',2030,'VMT',0.25,'');
INSERT INTO "Efficiency" VALUES('DSL','T_DSL',2020,'VMT',0.30,'');
INSERT INTO "Efficiency" VALUES('DSL','T_DSL',2025,'VMT',0.30,'');
INSERT INTO "Efficiency" VALUES('DSL','T_DSL',2030,'VMT',0.30,'');
INSERT INTO "Efficiency" VALUES('ELC','T_EV',2020,'VMT',0.89,'');
INSERT INTO "Efficiency" VALUES('ELC','T_EV',2025,'VMT',0.89,'');
INSERT INTO "Efficiency" VALUES('ELC','T_EV',2030,'VMT',0.89,'');
INSERT INTO "Efficiency" VALUES('ELC','R_EH',2020,'RH',1.0,'');
INSERT INTO "Efficiency" VALUES('ELC','R_EH',2025,'RH',1.0,'');
INSERT INTO "Efficiency" VALUES('ELC','R_EH',2030,'RH',1.0,'');
INSERT INTO "Efficiency" VALUES('NG','R_NGH',2020,'RH',0.85,'');
INSERT INTO "Efficiency" VALUES('NG','R_NGH',2025,'RH',0.85,'');
INSERT INTO "Efficiency" VALUES('NG','R_NGH',2030,'RH',0.85,'');


CREATE TABLE ExistingCapacity (
   tech text,
   vintage integer,
   exist_cap real,
   exist_cap_units text,
   exist_cap_notes text,
   PRIMARY KEY(tech, vintage),
   FOREIGN KEY(tech) REFERENCES technologies(tech),
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods) );
INSERT INTO "ExistingCapacity" VALUES('E_NUCLEAR',2015,0.1,'GW','');

 
CREATE TABLE CostInvest (
   tech text,
   vintage integer,
   cost_invest real,
   cost_invest_units text,
   cost_invest_notes text,
   PRIMARY KEY(tech, vintage),
   FOREIGN KEY(tech) REFERENCES technologies(tech),
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods) );
INSERT INTO "CostInvest" VALUES('E_NGCC',2020,1050,'$M/GW','');
INSERT INTO "CostInvest" VALUES('E_NGCC',2025,1025,'$M/GW','');
INSERT INTO "CostInvest" VALUES('E_NGCC',2030,1000,'$M/GW','');
INSERT INTO "CostInvest" VALUES('E_SOLPV',2020,900,'$M/GW',''); 
INSERT INTO "CostInvest" VALUES('E_SOLPV',2025,560,'$M/GW','');
INSERT INTO "CostInvest" VALUES('E_SOLPV',2030,800,'$M/GW','');
INSERT INTO "CostInvest" VALUES('E_NUCLEAR',2020,6145,'$M/GW','');
INSERT INTO "CostInvest" VALUES('E_NUCLEAR',2025,6045,'$M/GW','');
INSERT INTO "CostInvest" VALUES('E_NUCLEAR',2030,5890,'$M/GW','');
INSERT INTO "CostInvest" VALUES('E_BATT',2020,1150,'$M/GW','');
INSERT INTO "CostInvest" VALUES('E_BATT',2025,720,'$M/GW','');
INSERT INTO "CostInvest" VALUES('E_BATT',2030,480,'$M/GW','');
INSERT INTO "CostInvest" VALUES('T_GSL',2020,2570,'$/bvmt/yr','');
INSERT INTO "CostInvest" VALUES('T_GSL',2025,2700,'$/bvmt/yr','');
INSERT INTO "CostInvest" VALUES('T_GSL',2030,2700,'$/bvmt/yr','');
INSERT INTO "CostInvest" VALUES('T_DSL',2020,2715,'$/bvmt/yr','');
INSERT INTO "CostInvest" VALUES('T_DSL',2025,2810,'$/bvmt/yr','');
INSERT INTO "CostInvest" VALUES('T_DSL',2030,2810,'$/bvmt/yr','');
INSERT INTO "CostInvest" VALUES('T_EV',2020,3100,'$/bvmt/yr','');
INSERT INTO "CostInvest" VALUES('T_EV',2025,3030,'$/bvmt/yr','');
INSERT INTO "CostInvest" VALUES('T_EV',2030,2925,'$/bvmt/yr','');
INSERT INTO "CostInvest" VALUES('R_EH',2020,4.10,'$/PJ/yr','');
INSERT INTO "CostInvest" VALUES('R_EH',2025,4.10,'$/PJ/yr','');
INSERT INTO "CostInvest" VALUES('R_EH',2030,4.10,'$/PJ/yr','');
INSERT INTO "CostInvest" VALUES('R_NGH',2020,7.6,'$/PJ/yr','');
INSERT INTO "CostInvest" VALUES('R_NGH',2025,7.6,'$/PJ/yr','');
INSERT INTO "CostInvest" VALUES('R_NGH',2030,7.6,'$/PJ/yr','');


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
INSERT INTO "CostFixed" VALUES(2020,'E_NGCC',2020,30.6,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2025,'E_NGCC',2020,9.78,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2025,'E_NGCC',2025,9.78,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2030,'E_NGCC',2020,9.78,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2030,'E_NGCC',2025,9.78,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2030,'E_NGCC',2030,9.78,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2020,'E_SOLPV',2020,10.4,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2025,'E_SOLPV',2020,10.4,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2025,'E_SOLPV',2025,9.10,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2030,'E_SOLPV',2020,10.4,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2030,'E_SOLPV',2025,9.1,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2030,'E_SOLPV',2030,9.1,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2020,'E_NUCLEAR',2020,98.1,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2025,'E_NUCLEAR',2020,98.1,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2025,'E_NUCLEAR',2025,98.1,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2030,'E_NUCLEAR',2020,98.1,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2030,'E_NUCLEAR',2025,98.1,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2030,'E_NUCLEAR',2030,98.1,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2020,'E_BATT',2020,7.05,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2025,'E_BATT',2020,7.05,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2025,'E_BATT',2025,7.05,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2030,'E_BATT',2020,7.05,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2030,'E_BATT',2025,7.05,'$M/GWyr','');
INSERT INTO "CostFixed" VALUES(2030,'E_BATT',2030,7.05,'$M/GWyr','');

  
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
INSERT INTO "CostVariable" VALUES(2020,'S_IMPETH',2020,32,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2025,'S_IMPETH',2020,32,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2030,'S_IMPETH',2020,32,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2020,'S_IMPOIL',2020,20,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2025,'S_IMPOIL',2020,20,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2030,'S_IMPOIL',2020,20,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2020,'S_IMPNG',2020,4.0,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2025,'S_IMPNG',2020,4.0,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2030,'S_IMPNG',2020,4.0,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2020,'S_OILREF',2020,1.0,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2025,'S_OILREF',2020,1.0,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2030,'S_OILREF',2020,1.0,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2020,'E_NGCC',2020,1.6,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2025,'E_NGCC',2020,1.6,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2025,'E_NGCC',2025,1.7,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2030,'E_NGCC',2020,1.6,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2030,'E_NGCC',2025,1.7,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2030,'E_NGCC',2030,1.8,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2020,'E_NUCLEAR',2020,0.24,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2025,'E_NUCLEAR',2020,0.24,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2025,'E_NUCLEAR',2025,0.25,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2030,'E_NUCLEAR',2020,0.24,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2030,'E_NUCLEAR',2025,0.25,'$M/PJ','');
INSERT INTO "CostVariable" VALUES(2030,'E_NUCLEAR',2030,0.26,'$M/PJ','');

 
/*
-------------------------------------------------------
Tables in this section store model outputs
-------------------------------------------------------
*/


CREATE TABLE Output_VFlow_Out (
   scenario text,
   sector text,   
   t_periods integer,
   t_season text,
   t_day text,
   input_comm text,
   tech text,
   vintage integer,
   output_comm text,
   vflow_out real,
   PRIMARY KEY(scenario, t_periods, t_season, t_day, input_comm, tech, vintage, output_comm),
   FOREIGN KEY(sector) REFERENCES sector_labels(sector), 
   FOREIGN KEY(t_periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(t_season) REFERENCES time_periods(t_periods),   
   FOREIGN KEY(t_day) REFERENCES time_of_day(t_day),
   FOREIGN KEY(input_comm) REFERENCES commodities(comm_name),
   FOREIGN KEY(tech) REFERENCES technologies(tech),
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods), 
   FOREIGN KEY(output_comm) REFERENCES commodities(comm_name));



CREATE TABLE Output_VFlow_In (
   scenario text,
   sector text,
   t_periods integer,
   t_season text,
   t_day text,
   input_comm text,
   tech text,
   vintage integer,
   output_comm text,
   vflow_in real,
   PRIMARY KEY(scenario, t_periods, t_season, t_day, input_comm, tech, vintage, output_comm),
   FOREIGN KEY(sector) REFERENCES sector_labels(sector),   
   FOREIGN KEY(t_periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(t_season) REFERENCES time_periods(t_periods),   
   FOREIGN KEY(t_day) REFERENCES time_of_day(t_day),
   FOREIGN KEY(input_comm) REFERENCES commodities(comm_name),
   FOREIGN KEY(tech) REFERENCES technologies(tech),
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods), 
   FOREIGN KEY(output_comm) REFERENCES commodities(comm_name));
 

CREATE TABLE Output_V_Capacity (
   scenario text,
   sector text,
   tech text,
   vintage integer,
   capacity real,
   PRIMARY KEY(scenario, tech, vintage),
   FOREIGN KEY(sector) REFERENCES sector_labels(sector), 
   FOREIGN KEY(tech) REFERENCES technologies(tech),
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods));



CREATE TABLE Output_CapacityByPeriodAndTech (
   scenario text,
   sector text,
   t_periods integer,   
   tech text,
   capacity real,
   PRIMARY KEY(scenario, t_periods, tech),
   FOREIGN KEY(sector) REFERENCES sector_labels(sector), 
   FOREIGN KEY(t_periods) REFERENCES time_periods(t_periods),   
   FOREIGN KEY(tech) REFERENCES technologies(tech)); 



CREATE TABLE Output_Emissions (    
   scenario text,
   sector text,
   t_periods integer,
   emissions_comm text,
   tech text,
   vintage integer,
   emissions real,
   PRIMARY KEY(scenario, t_periods, emissions_comm, tech, vintage),
   FOREIGN KEY(sector) REFERENCES sector_labels(sector), 
   FOREIGN KEY(emissions_comm) REFERENCES EmissionActivity(emis_comm),
   FOREIGN KEY(t_periods) REFERENCES time_periods(t_periods),
   FOREIGN KEY(tech) REFERENCES technologies(tech)
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods));


CREATE TABLE Output_Costs (
   scenario text,
   sector text,
   output_name text,
   tech text,
   vintage integer,
   output_cost real,
   PRIMARY KEY(scenario, output_name, tech, vintage),
   FOREIGN KEY(sector) REFERENCES sector_labels(sector), 
   FOREIGN KEY(tech) REFERENCES technologies(tech),   
   FOREIGN KEY(vintage) REFERENCES time_periods(t_periods)); 

CREATE TABLE Output_Objective (
   scenario text,
   objective_name text,
   total_system_cost real );

CREATE TABLE Output_Curtailment (
	scenario text,
	sector text,
	t_periods integer,
	t_season text,
	t_day text,
	input_comm text,
	tech text,
	vintage integer,
	output_comm text,
	curtailment real,
	PRIMARY KEY(scenario,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm),
	FOREIGN KEY(t_periods) REFERENCES time_periods(t_periods),
	FOREIGN KEY(t_season) REFERENCES time_periods(t_periods),
	FOREIGN KEY(t_day) REFERENCES time_of_day(t_day),
	FOREIGN KEY(input_comm) REFERENCES commodities(comm_name),
	FOREIGN KEY(tech) REFERENCES technologies(tech),
	FOREIGN KEY(vintage) REFERENCES time_periods(t_periods),
	FOREIGN KEY(output_comm) REFERENCES commodities(comm_name)
);


COMMIT;
