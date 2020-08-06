BEGIN TRANSACTION;
CREATE TABLE time_season (
  t_season text primary key );
CREATE TABLE time_periods (
  t_periods integer primary key,
  flag text,
  FOREIGN KEY(flag) REFERENCES time_period_labels(t_period_labels));
CREATE TABLE time_period_labels (
  t_period_labels text primary key,
  t_period_labels_desc text);
CREATE TABLE time_of_day (
  t_day text primary key );
CREATE TABLE technology_labels (
  tech_labels text primary key,
  tech_labels_desc text);
CREATE TABLE technologies (
  tech text primary key,
  flag text,
  sector text,
  tech_desc text,
  tech_category text,
  FOREIGN KEY(flag) REFERENCES technology_labels(tech_labels),
  FOREIGN KEY(sector) REFERENCES sector_labels(sector));
CREATE TABLE `tech_reserve` (
	`tech`	text,
	`notes`	text,
	PRIMARY KEY(tech)
);
CREATE TABLE `tech_curtailment` (
	`technology`	text,
	PRIMARY KEY(`technology`),
	FOREIGN KEY(`technology`) REFERENCES `technologies`(`tech`)
);
CREATE TABLE `tech_annual` (
	`tech`	text,
	`region`	TEXT,
	PRIMARY KEY(tech),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`)
);
CREATE TABLE sector_labels (
  sector text primary key);
CREATE TABLE `regions` (
	`region`	TEXT,
	`region_note`	TEXT,
	PRIMARY KEY(`region`)
);
CREATE TABLE `groups` (
	`group_name`	text,
	`notes`	text,
	PRIMARY KEY(`group_name`)
);
CREATE TABLE commodity_labels (
  comm_labels text primary key,
  comm_labels_desc text);
CREATE TABLE commodities (
  comm_name text primary key,
  flag text,  
  comm_desc text,
  FOREIGN KEY(flag) REFERENCES commodity_labels(comm_labels));
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
	PRIMARY KEY(region,tech)
);
CREATE TABLE SegFrac (
   season_name text,
   time_of_day_name text,
   segfrac real check (segfrac>=0 AND segfrac<=1),
   segfrac_notes text,
   PRIMARY KEY(season_name, time_of_day_name), --here's where I define primary key as a combo of columns
   FOREIGN KEY(season_name) REFERENCES time_season(t_season),
   FOREIGN KEY(time_of_day_name) REFERENCES time_of_day(t_day) );
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
	PRIMARY KEY(tech,group_name)
);
CREATE TABLE `MinGenGroupTarget` (
	`period`	integer,
	`group_name`	text,
	`min_act_g`	real,
	`notes`	text,
	`region`	text,
	PRIMARY KEY(period,group_name)
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
CREATE TABLE "LifetimeLoanTech" (
	`region`	text,
	`tech`	text,
	`loan`	real,
	`loan_notes`	text,
	PRIMARY KEY(region,tech),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`)
);
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
CREATE TABLE "CapacityToActivity" (
	`region`	text,
	`tech`	text,
	`c2a`	real,
	`c2a_notes`	TEXT,
	PRIMARY KEY(region,tech),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`)
);
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
CREATE TABLE `CapacityCredit` (
	`region`	text,
	`periods`	integer,
	`tech`	text,
	`cf_tech`	real CHECK(cf_tech >= 0 AND cf_tech <= 1),
	`cf_tech_notes`	text,
	PRIMARY KEY(region,periods,tech)
);
COMMIT;
