BEGIN TRANSACTION;
CREATE TABLE time_season (
  t_season text primary key );
INSERT INTO `time_season` (t_season) VALUES ('spring');
INSERT INTO `time_season` (t_season) VALUES ('summer');
INSERT INTO `time_season` (t_season) VALUES ('fall');
INSERT INTO `time_season` (t_season) VALUES ('winter');
CREATE TABLE time_periods (
  t_periods integer primary key,
  flag text,
  FOREIGN KEY(flag) REFERENCES time_period_labels(t_period_labels));
INSERT INTO `time_periods` (t_periods,flag) VALUES (2015,'e');
INSERT INTO `time_periods` (t_periods,flag) VALUES (2020,'f');
INSERT INTO `time_periods` (t_periods,flag) VALUES (2025,'f');
INSERT INTO `time_periods` (t_periods,flag) VALUES (2030,'f');
INSERT INTO `time_periods` (t_periods,flag) VALUES (2035,'f');
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
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('S_IMPETH','r','supply',' imported ethanol','');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('S_IMPOIL','r','supply',' imported crude oil','');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('S_IMPNG','r','supply',' imported natural gas','');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('S_IMPURN','r','supply',' imported uranium','');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('S_OILREF','p','supply',' crude oil refinery','');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('E_NGCC','p','electric',' natural gas combined-cycle','');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('E_SOLPV','p','electric',' solar photovoltaic','');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('E_BATT','ps','electric',' lithium-ion battery','');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('E_NUCLEAR','pb','electric',' nuclear power plant','');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('T_BLND','p','transport','ethanol - gasoline blending process','');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('T_DSL','p','transport','diesel vehicle','');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('T_GSL','p','transport','gasoline vehicle','');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('T_EV','p','transport','electric vehicle','');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('R_EH','p','residential',' electric residential heating','');
INSERT INTO `technologies` (tech,flag,sector,tech_desc,tech_category) VALUES ('R_NGH','p','residential',' natural gas residential heating','');
CREATE TABLE `tech_reserve` (
	`tech`	text,
	`notes`	text,
	PRIMARY KEY(tech)
);
CREATE TABLE `tech_curtailment` (
	`technology`	text,
	PRIMARY KEY(technology),
	FOREIGN KEY(`technology`) REFERENCES `technologies`(`tech`)
);
INSERT INTO `tech_curtailment` (technology) VALUES ('S_OILREF');
CREATE TABLE `tech_annual` (
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
	PRIMARY KEY(region)
);
CREATE TABLE `groups` (
	`group_name`	text,
	`notes`	text,
	PRIMARY KEY(group_name)
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
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('ethos','p','dummy commodity to supply inputs (makes graph easier to read)');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('OIL','p','crude oil');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('NG','p','natural gas');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('URN','p','uranium');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('ETH','p','ethanol');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('SOL','p','solar insolation');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('GSL','p','gasoline');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('DSL','p','diesel');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('ELC','p','electricity');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('E10','p','gasoline blend with 10% ethanol');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('VMT','d','travel demand for vehicle-miles traveled');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('RH','d','demand for residential heating');
INSERT INTO `commodities` (comm_name,flag,comm_desc) VALUES ('CO2','e','CO2 emissions commodity');
CREATE TABLE "TechOutputSplit" (
	`region`	TEXT,
	`periods`	integer,
	`tech`	text,
	`output_comm`	text,
	`to_split`	real,
	`to_split_notes`	text,
	PRIMARY KEY(periods,tech,output_comm),
	FOREIGN KEY(`periods`) REFERENCES `time_periods`(`t_periods`),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`),
	FOREIGN KEY(`output_comm`) REFERENCES `commodities`(`comm_name`)
);
INSERT INTO `TechOutputSplit` (region,periods,tech,output_comm,to_split,to_split_notes) VALUES (NULL,2020,'S_OILREF','GSL',0.9,'');
INSERT INTO `TechOutputSplit` (region,periods,tech,output_comm,to_split,to_split_notes) VALUES (NULL,2020,'S_OILREF','DSL',0.1,'');
INSERT INTO `TechOutputSplit` (region,periods,tech,output_comm,to_split,to_split_notes) VALUES (NULL,2025,'S_OILREF','GSL',0.9,'');
INSERT INTO `TechOutputSplit` (region,periods,tech,output_comm,to_split,to_split_notes) VALUES (NULL,2025,'S_OILREF','DSL',0.1,'');
INSERT INTO `TechOutputSplit` (region,periods,tech,output_comm,to_split,to_split_notes) VALUES (NULL,2030,'S_OILREF','GSL',0.9,'');
INSERT INTO `TechOutputSplit` (region,periods,tech,output_comm,to_split,to_split_notes) VALUES (NULL,2030,'S_OILREF','DSL',0.1,'');
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
INSERT INTO `TechInputSplit` (region,periods,input_comm,tech,ti_split,ti_split_notes) VALUES (NULL,2020,'GSL','T_BLND',0.9,'');
INSERT INTO `TechInputSplit` (region,periods,input_comm,tech,ti_split,ti_split_notes) VALUES (NULL,2020,'ETH','T_BLND',0.1,'');
INSERT INTO `TechInputSplit` (region,periods,input_comm,tech,ti_split,ti_split_notes) VALUES (NULL,2025,'GSL','T_BLND',0.9,'');
INSERT INTO `TechInputSplit` (region,periods,input_comm,tech,ti_split,ti_split_notes) VALUES (NULL,2025,'ETH','T_BLND',0.1,'');
INSERT INTO `TechInputSplit` (region,periods,input_comm,tech,ti_split,ti_split_notes) VALUES (NULL,2030,'GSL','T_BLND',0.9,'');
INSERT INTO `TechInputSplit` (region,periods,input_comm,tech,ti_split,ti_split_notes) VALUES (NULL,2030,'ETH','T_BLND',0.1,'');
CREATE TABLE "StorageDuration" (
	`region`	text,
	`tech`	text,
	`duration`	real,
	`duration_notes`	text,
	PRIMARY KEY(region,tech)
);
INSERT INTO `StorageDuration` (region,tech,duration,duration_notes) VALUES ('R1','E_BATT',8.0,'8-hour duration specified as fraction of a day');
CREATE TABLE SegFrac (
   season_name text,
   time_of_day_name text,
   segfrac real check (segfrac>=0 AND segfrac<=1),
   segfrac_notes text,
   PRIMARY KEY(season_name, time_of_day_name), --here's where I define primary key as a combo of columns
   FOREIGN KEY(season_name) REFERENCES time_season(t_season),
   FOREIGN KEY(time_of_day_name) REFERENCES time_of_day(t_day) );
INSERT INTO `SegFrac` (season_name,time_of_day_name,segfrac,segfrac_notes) VALUES ('spring','day',0.125,'Spring - Day');
INSERT INTO `SegFrac` (season_name,time_of_day_name,segfrac,segfrac_notes) VALUES ('spring','night',0.125,'Spring - Night');
INSERT INTO `SegFrac` (season_name,time_of_day_name,segfrac,segfrac_notes) VALUES ('summer','day',0.125,'Summer - Day');
INSERT INTO `SegFrac` (season_name,time_of_day_name,segfrac,segfrac_notes) VALUES ('summer','night',0.125,'Summer - Night');
INSERT INTO `SegFrac` (season_name,time_of_day_name,segfrac,segfrac_notes) VALUES ('fall','day',0.125,'Fall - Day');
INSERT INTO `SegFrac` (season_name,time_of_day_name,segfrac,segfrac_notes) VALUES ('fall','night',0.125,'Fall - Night');
INSERT INTO `SegFrac` (season_name,time_of_day_name,segfrac,segfrac_notes) VALUES ('winter','day',0.125,'Winter - Day');
INSERT INTO `SegFrac` (season_name,time_of_day_name,segfrac,segfrac_notes) VALUES ('winter','night',0.125,'Winter - Night');
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
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','electric','E_NUCLEAR',2015,0.1);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','electric','E_SOLPV',2020,0.797032083630804);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','supply','S_IMPURN',2020,7.885);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','electric','E_NGCC',2025,0.356244611800246);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','residential','R_NGH',2020,320.0);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','transport','T_EV',2030,48.4);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','electric','E_NGCC',2030,0.356244611800247);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','transport','T_DSL',2030,3.6);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','electric','E_SOLPV',2030,3.77830676643529);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','transport','T_BLND',2020,200.0);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','transport','T_GSL',2020,50.0);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','supply','S_IMPOIL',2020,200.0);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','residential','R_NGH',2030,32.0);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','supply','S_OILREF',2020,200.0);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','residential','R_NGH',2025,32.0);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','transport','T_DSL',2020,6.0);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','electric','E_BATT',2030,2.43619279627768);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','transport','T_EV',2025,10.0);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','transport','T_GSL',2030,30.0);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','electric','E_SOLPV',2025,3.4299847952389);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','transport','T_EV',2020,64.0);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','supply','S_IMPETH',2020,20.0);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','supply','S_IMPNG',2020,617.633837649462);
INSERT INTO `Output_V_Capacity` (region,scenario,sector,tech,vintage,capacity) VALUES ('R1','test_run','electric','E_NGCC',2020,2.17996551552158);
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
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'spring','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'winter','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'winter','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'winter','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'spring','day','ELC','T_EV',2020,'VMT',8.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'winter','night','NG','E_NGCC',2020,'ELC',8.59451404494382);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'spring','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'spring','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'winter','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'spring','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'summer','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'fall','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'fall','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'fall','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'summer','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'spring','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'winter','night','ethos','S_IMPNG',2020,'NG',62.6852127020369);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'winter','day','DSL','T_DSL',2020,'VMT',0.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'summer','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'winter','day','ELC','T_EV',2020,'VMT',3.2);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'spring','day','ethos','S_IMPNG',2020,'NG',6.47058823529412);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'spring','night','ELC','T_EV',2020,'VMT',8.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'spring','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2030,'winter','night','NG','R_NGH',2025,'RH',4.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2020,'spring','night','NG','R_NGH',2020,'RH',10.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'fall','night','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'fall','night','ELC','T_EV',2020,'VMT',3.2);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'fall','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'fall','day','E10','T_GSL',2020,'VMT',6.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2025,'winter','night','NG','R_NGH',2020,'RH',40.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2025,'winter','day','NG','R_NGH',2025,'RH',3.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'fall','night','DSL','T_DSL',2020,'VMT',0.3);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'fall','night','ELC','T_EV',2030,'VMT',6.05);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'fall','night','ELC','E_BATT',2030,'ELC',6.40312673288318);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'winter','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'spring','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'winter','night','NG','E_NGCC',2020,'ELC',8.59451404494382);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'winter','night','E10','T_GSL',2020,'VMT',6.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'fall','night','ELC','T_EV',2025,'VMT',1.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'winter','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'winter','day','ELC','T_EV',2020,'VMT',8.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'fall','night','DSL','T_DSL',2030,'VMT',0.45);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'spring','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'winter','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2030,'spring','day','NG','R_NGH',2020,'RH',5.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'spring','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2025,'fall','day','NG','R_NGH',2025,'RH',0.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'summer','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'fall','day','DSL','T_DSL',2030,'VMT',0.45);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'summer','day','E10','T_GSL',2020,'VMT',6.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'winter','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2030,'fall','day','NG','R_NGH',2020,'RH',5.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'fall','day','DSL','T_DSL',2020,'VMT',0.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2020,'winter','night','NG','R_NGH',2020,'RH',40.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'spring','night','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2030,'fall','day','NG','R_NGH',2030,'RH',0.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'spring','night','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'summer','day','SOL','E_SOLPV',2025,'ELC',8.11362903313763);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'summer','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'fall','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'spring','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'fall','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2025,'spring','night','NG','R_NGH',2020,'RH',10.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'summer','night','DSL','T_DSL',2020,'VMT',0.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'fall','night','NG','E_NGCC',2020,'ELC',8.59451404494382);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'summer','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'spring','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'fall','day','SOL','E_SOLPV',2030,'ELC',8.93758465600268);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'spring','night','ELC','T_EV',2020,'VMT',3.2);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'spring','day','SOL','E_SOLPV',2030,'ELC',8.93758465600268);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'summer','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2030,'fall','night','NG','R_NGH',2025,'RH',1.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'summer','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'fall','day','ELC','T_EV',2020,'VMT',8.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'winter','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'spring','night','E10','T_GSL',2020,'VMT',6.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'winter','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'fall','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'spring','night','ELC','T_EV',2030,'VMT',6.05);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'spring','night','ELC','E_BATT',2030,'ELC',6.40312673288318);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'fall','day','DSL','T_DSL',2020,'VMT',0.3);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'winter','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'winter','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'summer','day','ethos','S_IMPNG',2020,'NG',12.1984266383912);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'fall','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'spring','day','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'fall','day','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'fall','day','ELC','T_EV',2020,'VMT',8.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'fall','night','E10','T_GSL',2020,'VMT',6.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'summer','night','E10','T_GSL',2020,'VMT',6.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'winter','night','ELC','T_EV',2030,'VMT',6.05);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'winter','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'summer','night','NG','E_NGCC',2020,'ELC',8.59451404494382);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'spring','night','DSL','T_DSL',2020,'VMT',0.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'spring','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'winter','day','E10','T_GSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'winter','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'winter','night','ELC','T_EV',2020,'VMT',3.2);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'summer','day','NG','E_NGCC',2020,'ELC',6.70913465111515);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'spring','night','ethos','S_IMPNG',2020,'NG',27.3910950549781);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'winter','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'spring','night','ELC','T_EV',2020,'VMT',8.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'fall','day','ELC','T_EV',2025,'VMT',1.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'summer','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'summer','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'fall','night','DSL','T_DSL',2020,'VMT',0.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'fall','day','DSL','T_DSL',2020,'VMT',0.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'fall','day','ethos','S_IMPNG',2020,'NG',7.05882352941176);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'winter','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'spring','night','ethos','S_IMPNG',2020,'NG',31.1211917923451);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'spring','night','NG','E_NGCC',2020,'ELC',5.00037607610559);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'spring','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'fall','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'winter','night','ethos','S_IMPNG',2020,'NG',69.9447212041098);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'spring','night','ELC','T_EV',2025,'VMT',1.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'fall','day','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'summer','day','E10','T_GSL',2030,'VMT',3.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'summer','night','E10','T_GSL',2030,'VMT',3.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'spring','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'fall','night','ELC','T_EV',2025,'VMT',1.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'summer','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'winter','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'fall','night','ELC','T_EV',2020,'VMT',8.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'winter','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'winter','day','E10','T_GSL',2020,'VMT',6.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'summer','night','E10','T_GSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'fall','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'spring','day','E10','T_GSL',2020,'VMT',6.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'summer','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'fall','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'spring','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'fall','day','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'summer','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'spring','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2025,'fall','night','NG','R_NGH',2025,'RH',1.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'summer','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'fall','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'fall','night','ELC','T_EV',2020,'VMT',8.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'fall','night','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'spring','day','ELC','T_EV',2025,'VMT',1.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'spring','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'winter','day','ELC','T_EV',2020,'VMT',8.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'winter','day','DSL','T_DSL',2030,'VMT',0.45);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'fall','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'winter','day','ethos','S_IMPNG',2020,'NG',38.8235294117647);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'fall','night','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'fall','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'summer','night','ethos','S_IMPNG',2020,'NG',18.1800153217569);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'winter','night','ethos','S_IMPNG',2020,'NG',77.2042297061828);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'summer','night','NG','E_NGCC',2020,'ELC',5.00037607610559);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'spring','day','NG','E_NGCC',2020,'ELC',6.70913465111515);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'spring','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'winter','night','NG','E_NGCC',2030,'ELC',1.40449438202248);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'fall','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'summer','day','ELC','T_EV',2020,'VMT',3.2);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'fall','night','ethos','S_IMPNG',2020,'NG',23.2092399244701);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'winter','night','NG','E_NGCC',2025,'ELC',1.40449438202247);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'fall','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'spring','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'winter','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'spring','night','E10','T_GSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'fall','day','SOL','E_SOLPV',2025,'ELC',8.11362903313763);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'fall','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2020,'fall','night','NG','R_NGH',2020,'RH',10.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'fall','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'spring','day','ELC','T_EV',2020,'VMT',8.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'summer','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2025,'spring','day','NG','R_NGH',2020,'RH',5.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'winter','night','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'spring','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'fall','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'fall','day','E10','T_GSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'spring','day','DSL','T_DSL',2020,'VMT',0.3);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'fall','night','ethos','S_IMPNG',2020,'NG',27.3910950549781);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'spring','night','ELC','T_EV',2025,'VMT',1.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'winter','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'winter','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'spring','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'summer','night','NG','E_NGCC',2025,'ELC',1.40449438202247);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'summer','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'fall','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'spring','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'spring','night','DSL','T_DSL',2020,'VMT',0.3);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'fall','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'spring','day','ELC','T_EV',2020,'VMT',3.2);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'spring','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'winter','night','ELC','T_EV',2025,'VMT',1.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'summer','day','ELC','T_EV',2025,'VMT',1.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2020,'fall','day','NG','R_NGH',2020,'RH',5.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'summer','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2030,'spring','night','NG','R_NGH',2025,'RH',1.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'summer','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'fall','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'winter','day','ethos','S_IMPNG',2020,'NG',42.3529411764706);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'fall','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'summer','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'winter','night','E10','T_GSL',2020,'VMT',6.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'winter','night','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'winter','day','ELC','T_EV',2025,'VMT',1.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'summer','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'summer','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'fall','day','ELC','T_EV',2030,'VMT',6.05);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'summer','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'winter','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'winter','day','ELC','T_EV',2025,'VMT',1.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2030,'winter','day','NG','R_NGH',2025,'RH',3.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'spring','day','E10','T_GSL',2020,'VMT',6.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'fall','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'summer','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'summer','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'summer','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'spring','day','ELC','T_EV',2025,'VMT',1.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'fall','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'winter','day','ELC','T_EV',2030,'VMT',6.05);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'winter','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'spring','day','DSL','T_DSL',2020,'VMT',0.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'fall','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'spring','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'winter','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'spring','day','ethos','S_IMPNG',2020,'NG',7.05882352941176);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'winter','day','SOL','E_SOLPV',2025,'ELC',8.11362903313763);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'winter','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'spring','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'summer','night','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'summer','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'summer','day','E10','T_GSL',2020,'VMT',6.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'summer','night','ELC','T_EV',2020,'VMT',3.2);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2025,'winter','night','NG','R_NGH',2025,'RH',4.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'fall','day','ethos','S_IMPNG',2020,'NG',6.47058823529412);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'summer','night','DSL','T_DSL',2020,'VMT',0.3);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'summer','night','ELC','T_EV',2030,'VMT',6.05);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'winter','night','DSL','T_DSL',2030,'VMT',0.45);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'summer','night','ELC','E_BATT',2030,'ELC',6.40312673288318);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'winter','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'winter','night','DSL','T_DSL',2020,'VMT',0.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'summer','night','ELC','T_EV',2025,'VMT',1.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2020,'winter','day','NG','R_NGH',2020,'RH',30.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'summer','night','DSL','T_DSL',2030,'VMT',0.45);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'winter','night','DSL','T_DSL',2020,'VMT',0.3);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2030,'spring','day','NG','R_NGH',2025,'RH',0.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'winter','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2025,'fall','day','NG','R_NGH',2020,'RH',5.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'winter','night','NG','E_NGCC',2020,'ELC',8.59451404494382);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'fall','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'summer','day','DSL','T_DSL',2030,'VMT',0.45);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'fall','day','E10','T_GSL',2020,'VMT',6.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2030,'winter','night','NG','R_NGH',2030,'RH',4.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'winter','day','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'spring','day','DSL','T_DSL',2020,'VMT',0.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'winter','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'summer','day','DSL','T_DSL',2020,'VMT',0.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'winter','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'winter','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'spring','day','SOL','E_SOLPV',2025,'ELC',8.11362903313763);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'fall','day','SOL','E_SOLPV',2025,'ELC',8.11362903313763);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'spring','day','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'fall','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'summer','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'summer','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'spring','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'spring','night','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'fall','night','DSL','T_DSL',2020,'VMT',0.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'summer','night','NG','E_NGCC',2020,'ELC',8.59451404494382);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'fall','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2030,'winter','night','NG','R_NGH',2020,'RH',40.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'summer','day','SOL','E_SOLPV',2030,'ELC',8.93758465600268);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'spring','night','E10','T_GSL',2030,'VMT',3.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'fall','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'fall','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'summer','day','ELC','T_EV',2020,'VMT',8.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'winter','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'summer','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'winter','day','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'spring','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'winter','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'summer','day','DSL','T_DSL',2020,'VMT',0.3);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'spring','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'winter','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'spring','day','ELC','T_EV',2030,'VMT',6.05);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'fall','day','ethos','S_IMPNG',2020,'NG',18.0807795795677);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'summer','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'spring','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'spring','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'spring','day','ethos','S_IMPNG',2020,'NG',18.0807795795677);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'summer','day','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'summer','day','ELC','T_EV',2020,'VMT',8.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'summer','night','E10','T_GSL',2020,'VMT',6.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'fall','night','E10','T_GSL',2020,'VMT',6.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'winter','day','NG','E_NGCC',2020,'ELC',6.70913465111515);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'fall','night','NG','E_NGCC',2020,'ELC',8.59451404494382);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'spring','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'winter','day','E10','T_GSL',2020,'VMT',6.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'winter','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'spring','night','NG','E_NGCC',2025,'ELC',1.40449438202247);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'fall','day','NG','E_NGCC',2020,'ELC',6.70913465111516);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'winter','day','SOL','E_SOLPV',2025,'ELC',8.11362903313763);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'winter','night','E10','T_GSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'summer','day','ELC','T_EV',2025,'VMT',1.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'fall','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'fall','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'summer','night','DSL','T_DSL',2020,'VMT',0.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'winter','night','DSL','T_DSL',2020,'VMT',0.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'winter','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'summer','day','DSL','T_DSL',2020,'VMT',0.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'spring','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'winter','day','E10','T_GSL',2030,'VMT',3.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'winter','night','E10','T_GSL',2030,'VMT',3.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'winter','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'summer','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'winter','day','ethos','S_IMPNG',2020,'NG',47.49254428545);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'winter','night','ELC','T_EV',2020,'VMT',8.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'spring','night','ethos','S_IMPNG',2020,'NG',23.2092399244701);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2030,'fall','day','NG','R_NGH',2025,'RH',0.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'fall','day','E10','T_GSL',2030,'VMT',3.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'summer','day','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'fall','night','E10','T_GSL',2030,'VMT',3.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'spring','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2030,'winter','day','NG','R_NGH',2030,'RH',3.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'summer','night','ELC','T_EV',2025,'VMT',1.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'fall','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'spring','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'spring','day','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'spring','day','SOL','E_SOLPV',2025,'ELC',2.46591815298608);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'summer','night','ELC','T_EV',2020,'VMT',8.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'winter','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'fall','night','E10','T_GSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'summer','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'fall','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'winter','night','ELC','T_EV',2020,'VMT',8.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'summer','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'winter','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'summer','day','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'fall','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'winter','day','SOL','E_SOLPV',2030,'ELC',8.93758465600268);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2025,'spring','day','NG','R_NGH',2025,'RH',0.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'fall','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'summer','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'summer','night','ELC','T_EV',2020,'VMT',8.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2025,'fall','night','NG','R_NGH',2020,'RH',10.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'summer','night','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'spring','night','DSL','T_DSL',2030,'VMT',0.45);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2025,'winter','day','NG','R_NGH',2020,'RH',30.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'winter','day','DSL','T_DSL',2020,'VMT',0.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'winter','night','NG','E_NGCC',2025,'ELC',1.40449438202247);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'summer','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'summer','night','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'spring','day','E10','T_GSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'spring','night','NG','E_NGCC',2020,'ELC',8.59451404494382);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'summer','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'winter','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'fall','night','ethos','S_IMPNG',2020,'NG',31.1211917923451);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'spring','night','E10','T_GSL',2020,'VMT',6.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'spring','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'fall','night','NG','E_NGCC',2020,'ELC',5.00037607610559);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'spring','night','DSL','T_DSL',2020,'VMT',0.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'summer','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'spring','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2030,'fall','night','NG','R_NGH',2030,'RH',1.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'spring','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'fall','day','ELC','T_EV',2020,'VMT',3.2);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'summer','night','ethos','S_IMPNG',2020,'NG',9.09159286564652);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'summer','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'winter','day','DSL','T_DSL',2020,'VMT',0.3);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'winter','day','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'spring','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'summer','day','SOL','E_SOLPV',2025,'ELC',8.11362903313763);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'summer','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'summer','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'fall','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'spring','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2025,'spring','night','NG','R_NGH',2025,'RH',1.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'summer','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'summer','day','E10','T_GSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'summer','night','ethos','S_IMPNG',2020,'NG',15.6263891726251);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'fall','night','NG','E_NGCC',2025,'ELC',1.40449438202247);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2030,'fall','night','NG','R_NGH',2020,'RH',10.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'fall','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2030,'spring','day','NG','R_NGH',2030,'RH',0.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2025,'summer','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'winter','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'spring','day','E10','T_GSL',2030,'VMT',3.75);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'winter','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2020,'winter','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'spring','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'spring','day','DSL','T_DSL',2030,'VMT',0.45);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'summer','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'winter','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'winter','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'fall','day','ELC','T_EV',2025,'VMT',1.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2030,'spring','night','NG','R_NGH',2020,'RH',10.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'spring','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'fall','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'winter','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'fall','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'summer','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'summer','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2030,'spring','night','NG','R_NGH',2030,'RH',1.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'fall','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2025,'spring','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2020,'spring','day','NG','R_NGH',2020,'RH',5.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'winter','night','ELC','T_EV',2025,'VMT',1.25);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2030,'winter','night','URN','E_NUCLEAR',2015,'ELC',0.39425);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'fall','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2030,'fall','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','electric',2020,'spring','night','NG','E_NGCC',2020,'ELC',8.59451404494382);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'spring','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2020,'spring','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','transport',2030,'summer','day','ELC','T_EV',2030,'VMT',6.05);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','residential',2030,'winter','day','NG','R_NGH',2020,'RH',30.0);
INSERT INTO `Output_VFlow_Out` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_out) VALUES ('R1','test_run','supply',2025,'fall','night','ethos','S_IMPETH',2020,'ETH',2.5);
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
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'summer','day','ELC','E_BATT',2030,'ELC',7.53309027398021);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'fall','day','ELC','E_BATT',2030,'ELC',7.53309027398021);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'winter','day','ELC','E_BATT',2030,'ELC',7.53309027398021);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'spring','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'winter','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'winter','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'winter','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'spring','day','ELC','T_EV',2020,'VMT',8.98876404494382);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'winter','night','NG','E_NGCC',2020,'ELC',15.6263891726251);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'spring','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'spring','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'winter','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'spring','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'summer','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'fall','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'fall','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'fall','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'summer','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'spring','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'winter','night','ethos','S_IMPNG',2020,'NG',62.6852127020369);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'winter','day','DSL','T_DSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'summer','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'winter','day','ELC','T_EV',2020,'VMT',3.59550561797753);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'spring','day','ethos','S_IMPNG',2020,'NG',6.47058823529412);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'spring','night','ELC','T_EV',2020,'VMT',8.98876404494382);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'spring','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2030,'winter','night','NG','R_NGH',2025,'RH',4.70588235294118);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2020,'spring','night','NG','R_NGH',2020,'RH',11.7647058823529);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'fall','night','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'fall','night','ELC','T_EV',2020,'VMT',3.59550561797753);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'fall','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'fall','day','E10','T_GSL',2020,'VMT',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2025,'winter','night','NG','R_NGH',2020,'RH',47.0588235294118);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2025,'winter','day','NG','R_NGH',2025,'RH',3.52941176470588);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'fall','night','DSL','T_DSL',2020,'VMT',1.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'fall','night','ELC','T_EV',2030,'VMT',6.79775280898876);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'winter','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'spring','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'winter','night','NG','E_NGCC',2020,'ELC',15.6263891726251);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'winter','night','E10','T_GSL',2020,'VMT',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'fall','night','ELC','T_EV',2025,'VMT',1.40449438202247);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'winter','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'winter','day','ELC','T_EV',2020,'VMT',8.98876404494382);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'fall','night','DSL','T_DSL',2030,'VMT',1.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'spring','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'winter','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2030,'spring','day','NG','R_NGH',2020,'RH',5.88235294117647);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'spring','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2025,'fall','day','NG','R_NGH',2025,'RH',0.588235294117647);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'summer','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'fall','day','DSL','T_DSL',2030,'VMT',1.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'summer','day','E10','T_GSL',2020,'VMT',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'winter','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2030,'fall','day','NG','R_NGH',2020,'RH',5.88235294117647);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'fall','day','DSL','T_DSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2020,'winter','night','NG','R_NGH',2020,'RH',47.0588235294118);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'spring','night','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2030,'fall','day','NG','R_NGH',2030,'RH',0.588235294117647);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'spring','night','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'summer','day','SOL','E_SOLPV',2025,'ELC',8.11362903313763);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'summer','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'fall','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'spring','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'fall','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2025,'spring','night','NG','R_NGH',2020,'RH',11.7647058823529);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'summer','night','DSL','T_DSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'fall','night','NG','E_NGCC',2020,'ELC',15.6263891726251);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'summer','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'spring','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'fall','day','SOL','E_SOLPV',2030,'ELC',8.93758465600268);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'spring','night','ELC','T_EV',2020,'VMT',3.59550561797753);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'spring','day','SOL','E_SOLPV',2030,'ELC',8.93758465600268);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'summer','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2030,'fall','night','NG','R_NGH',2025,'RH',1.17647058823529);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'summer','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'fall','day','ELC','T_EV',2020,'VMT',8.98876404494382);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'winter','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'spring','night','E10','T_GSL',2020,'VMT',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'winter','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'fall','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'spring','night','ELC','T_EV',2030,'VMT',6.79775280898876);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'fall','day','DSL','T_DSL',2020,'VMT',1.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'winter','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'winter','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'summer','day','ethos','S_IMPNG',2020,'NG',12.1984266383912);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'fall','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'spring','day','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'fall','day','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'fall','day','ELC','T_EV',2020,'VMT',8.98876404494382);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'fall','night','E10','T_GSL',2020,'VMT',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'summer','night','E10','T_GSL',2020,'VMT',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'winter','night','ELC','T_EV',2030,'VMT',6.79775280898876);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'winter','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'summer','night','NG','E_NGCC',2020,'ELC',15.6263891726251);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'spring','night','DSL','T_DSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'spring','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'winter','day','E10','T_GSL',2020,'VMT',10.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'winter','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'winter','night','ELC','T_EV',2020,'VMT',3.59550561797753);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'summer','day','NG','E_NGCC',2020,'ELC',12.1984266383912);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'spring','night','ethos','S_IMPNG',2020,'NG',27.3910950549781);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'winter','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'spring','night','ELC','T_EV',2020,'VMT',8.98876404494382);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'fall','day','ELC','T_EV',2025,'VMT',1.40449438202247);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'summer','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'summer','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'fall','night','DSL','T_DSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'fall','day','DSL','T_DSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'fall','day','ethos','S_IMPNG',2020,'NG',7.05882352941176);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'winter','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'spring','night','ethos','S_IMPNG',2020,'NG',31.1211917923451);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'spring','night','NG','E_NGCC',2020,'ELC',9.09159286564652);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'spring','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'fall','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'winter','night','ethos','S_IMPNG',2020,'NG',69.9447212041098);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'spring','night','ELC','T_EV',2025,'VMT',1.40449438202247);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'fall','day','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'summer','day','E10','T_GSL',2030,'VMT',15.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'summer','night','E10','T_GSL',2030,'VMT',15.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'spring','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'fall','night','ELC','T_EV',2025,'VMT',1.40449438202247);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'summer','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'winter','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'fall','night','ELC','T_EV',2020,'VMT',8.98876404494382);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'winter','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'winter','day','E10','T_GSL',2020,'VMT',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'summer','night','E10','T_GSL',2020,'VMT',10.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'fall','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'spring','day','E10','T_GSL',2020,'VMT',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'summer','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'fall','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'spring','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'fall','day','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'summer','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'spring','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2025,'fall','night','NG','R_NGH',2025,'RH',1.17647058823529);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'summer','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'fall','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'fall','night','ELC','T_EV',2020,'VMT',8.98876404494382);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'fall','night','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'spring','day','ELC','T_EV',2025,'VMT',1.40449438202247);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'spring','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'winter','day','ELC','T_EV',2020,'VMT',8.98876404494382);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'winter','day','DSL','T_DSL',2030,'VMT',1.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'fall','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'winter','day','ethos','S_IMPNG',2020,'NG',38.8235294117647);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'fall','night','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'fall','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'summer','night','ethos','S_IMPNG',2020,'NG',18.1800153217569);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'winter','night','ethos','S_IMPNG',2020,'NG',77.2042297061828);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'summer','night','NG','E_NGCC',2020,'ELC',9.09159286564652);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'spring','day','NG','E_NGCC',2020,'ELC',12.1984266383912);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'spring','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'winter','night','NG','E_NGCC',2030,'ELC',2.55362614913177);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'fall','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'summer','day','ELC','T_EV',2020,'VMT',3.59550561797753);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'fall','night','ethos','S_IMPNG',2020,'NG',23.2092399244701);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'winter','night','NG','E_NGCC',2025,'ELC',2.55362614913176);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'fall','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'spring','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'winter','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'spring','night','E10','T_GSL',2020,'VMT',10.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'fall','day','SOL','E_SOLPV',2025,'ELC',8.11362903313763);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'fall','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2020,'fall','night','NG','R_NGH',2020,'RH',11.7647058823529);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'fall','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'spring','day','ELC','T_EV',2020,'VMT',8.98876404494382);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'summer','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2025,'spring','day','NG','R_NGH',2020,'RH',5.88235294117647);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'winter','night','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'spring','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'fall','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'fall','day','E10','T_GSL',2020,'VMT',10.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'spring','day','DSL','T_DSL',2020,'VMT',1.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'fall','night','ethos','S_IMPNG',2020,'NG',27.3910950549781);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'spring','night','ELC','T_EV',2025,'VMT',1.40449438202247);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'winter','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'winter','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'spring','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'summer','night','NG','E_NGCC',2025,'ELC',2.55362614913176);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'summer','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'fall','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'spring','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'spring','night','DSL','T_DSL',2020,'VMT',1.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'fall','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'spring','day','ELC','T_EV',2020,'VMT',3.59550561797753);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'spring','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'winter','night','ELC','T_EV',2025,'VMT',1.40449438202247);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'summer','day','ELC','T_EV',2025,'VMT',1.40449438202247);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2020,'fall','day','NG','R_NGH',2020,'RH',5.88235294117647);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'summer','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2030,'spring','night','NG','R_NGH',2025,'RH',1.17647058823529);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'summer','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'fall','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'winter','day','ethos','S_IMPNG',2020,'NG',42.3529411764706);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'fall','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'summer','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'winter','night','E10','T_GSL',2020,'VMT',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'winter','night','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'winter','day','ELC','T_EV',2025,'VMT',1.40449438202247);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'summer','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'summer','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'fall','day','ELC','T_EV',2030,'VMT',6.79775280898876);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'summer','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'winter','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'winter','day','ELC','T_EV',2025,'VMT',1.40449438202247);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2030,'winter','day','NG','R_NGH',2025,'RH',3.52941176470588);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'spring','day','E10','T_GSL',2020,'VMT',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'fall','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'summer','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'summer','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'summer','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'spring','day','ELC','T_EV',2025,'VMT',1.40449438202247);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'fall','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'winter','day','ELC','T_EV',2030,'VMT',6.79775280898876);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'winter','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'spring','day','DSL','T_DSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'fall','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'spring','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'winter','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'spring','day','ethos','S_IMPNG',2020,'NG',7.05882352941176);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'winter','day','SOL','E_SOLPV',2025,'ELC',8.11362903313763);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'winter','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'spring','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'summer','night','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'summer','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'summer','day','E10','T_GSL',2020,'VMT',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'summer','night','ELC','T_EV',2020,'VMT',3.59550561797753);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2025,'winter','night','NG','R_NGH',2025,'RH',4.70588235294118);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'fall','day','ethos','S_IMPNG',2020,'NG',6.47058823529412);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'summer','night','DSL','T_DSL',2020,'VMT',1.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'summer','night','ELC','T_EV',2030,'VMT',6.79775280898876);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'winter','night','DSL','T_DSL',2030,'VMT',1.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'winter','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'winter','night','DSL','T_DSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'summer','night','ELC','T_EV',2025,'VMT',1.40449438202247);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2020,'winter','day','NG','R_NGH',2020,'RH',35.2941176470588);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'summer','night','DSL','T_DSL',2030,'VMT',1.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'winter','night','DSL','T_DSL',2020,'VMT',1.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2030,'spring','day','NG','R_NGH',2025,'RH',0.588235294117647);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'winter','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2025,'fall','day','NG','R_NGH',2020,'RH',5.88235294117647);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'winter','night','NG','E_NGCC',2020,'ELC',15.6263891726251);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'fall','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'summer','day','DSL','T_DSL',2030,'VMT',1.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'fall','day','E10','T_GSL',2020,'VMT',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2030,'winter','night','NG','R_NGH',2030,'RH',4.70588235294118);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'winter','day','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'spring','day','DSL','T_DSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'winter','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'summer','day','DSL','T_DSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'winter','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'winter','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'spring','day','SOL','E_SOLPV',2025,'ELC',8.11362903313763);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'fall','day','SOL','E_SOLPV',2025,'ELC',8.11362903313763);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'spring','day','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'fall','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'summer','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'summer','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'spring','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'spring','night','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'fall','night','DSL','T_DSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'summer','night','NG','E_NGCC',2020,'ELC',15.6263891726251);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'fall','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2030,'winter','night','NG','R_NGH',2020,'RH',47.0588235294118);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'summer','day','SOL','E_SOLPV',2030,'ELC',8.93758465600268);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'spring','night','E10','T_GSL',2030,'VMT',15.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'fall','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'fall','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'summer','day','ELC','T_EV',2020,'VMT',8.98876404494382);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'winter','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'summer','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'winter','day','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'spring','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'winter','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'summer','day','DSL','T_DSL',2020,'VMT',1.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'spring','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'winter','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'spring','day','ELC','T_EV',2030,'VMT',6.79775280898876);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'fall','day','ethos','S_IMPNG',2020,'NG',18.0807795795677);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'summer','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'spring','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'spring','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'spring','day','ethos','S_IMPNG',2020,'NG',18.0807795795677);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'summer','day','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'summer','day','ELC','T_EV',2020,'VMT',8.98876404494382);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'summer','night','E10','T_GSL',2020,'VMT',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'fall','night','E10','T_GSL',2020,'VMT',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'winter','day','NG','E_NGCC',2020,'ELC',12.1984266383912);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'fall','night','NG','E_NGCC',2020,'ELC',15.6263891726251);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'spring','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'winter','day','E10','T_GSL',2020,'VMT',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'winter','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'spring','night','NG','E_NGCC',2025,'ELC',2.55362614913176);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'fall','day','NG','E_NGCC',2020,'ELC',12.1984266383912);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'winter','day','SOL','E_SOLPV',2025,'ELC',8.11362903313763);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'winter','night','E10','T_GSL',2020,'VMT',10.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'summer','day','ELC','T_EV',2025,'VMT',1.40449438202247);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'fall','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'fall','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'summer','night','DSL','T_DSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'winter','night','DSL','T_DSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'winter','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'summer','day','DSL','T_DSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'spring','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'winter','day','E10','T_GSL',2030,'VMT',15.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'winter','night','E10','T_GSL',2030,'VMT',15.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'winter','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'summer','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'winter','day','ethos','S_IMPNG',2020,'NG',47.49254428545);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'winter','night','ELC','T_EV',2020,'VMT',8.98876404494382);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'spring','night','ethos','S_IMPNG',2020,'NG',23.2092399244701);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2030,'fall','day','NG','R_NGH',2025,'RH',0.588235294117647);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'fall','day','E10','T_GSL',2030,'VMT',15.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'summer','day','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'fall','night','E10','T_GSL',2030,'VMT',15.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'spring','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2030,'winter','day','NG','R_NGH',2030,'RH',3.52941176470588);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'summer','night','ELC','T_EV',2025,'VMT',1.40449438202247);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'fall','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'spring','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'spring','day','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'spring','day','SOL','E_SOLPV',2025,'ELC',2.46591815298608);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'summer','night','ELC','T_EV',2020,'VMT',8.98876404494382);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'winter','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'fall','night','E10','T_GSL',2020,'VMT',10.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'summer','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'fall','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'winter','night','ELC','T_EV',2020,'VMT',8.98876404494382);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'summer','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'winter','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'summer','day','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'fall','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'winter','day','SOL','E_SOLPV',2030,'ELC',8.93758465600268);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2025,'spring','day','NG','R_NGH',2025,'RH',0.588235294117647);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'fall','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'summer','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'summer','night','ELC','T_EV',2020,'VMT',8.98876404494382);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2025,'fall','night','NG','R_NGH',2020,'RH',11.7647058823529);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'summer','night','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'spring','night','DSL','T_DSL',2030,'VMT',1.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2025,'winter','day','NG','R_NGH',2020,'RH',35.2941176470588);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'winter','day','DSL','T_DSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'winter','night','NG','E_NGCC',2025,'ELC',2.55362614913176);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'summer','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'summer','night','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'spring','day','E10','T_GSL',2020,'VMT',10.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'spring','night','NG','E_NGCC',2020,'ELC',15.6263891726251);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'summer','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'winter','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'fall','night','ethos','S_IMPNG',2020,'NG',31.1211917923451);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'spring','night','E10','T_GSL',2020,'VMT',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'spring','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'fall','night','NG','E_NGCC',2020,'ELC',9.09159286564652);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'spring','night','DSL','T_DSL',2020,'VMT',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'summer','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'spring','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2030,'fall','night','NG','R_NGH',2030,'RH',1.17647058823529);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'spring','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'fall','day','ELC','T_EV',2020,'VMT',3.59550561797753);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'summer','night','ethos','S_IMPNG',2020,'NG',9.09159286564652);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'summer','day','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'winter','day','DSL','T_DSL',2020,'VMT',1.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'winter','day','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'spring','night','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'summer','day','SOL','E_SOLPV',2025,'ELC',8.11362903313763);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'summer','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'summer','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'fall','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'spring','night','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2025,'spring','night','NG','R_NGH',2025,'RH',1.17647058823529);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'summer','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'summer','day','E10','T_GSL',2020,'VMT',10.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'summer','night','ethos','S_IMPNG',2020,'NG',15.6263891726251);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'fall','night','NG','E_NGCC',2025,'ELC',2.55362614913176);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2030,'fall','night','NG','R_NGH',2020,'RH',11.7647058823529);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'fall','day','ethos','S_IMPOIL',2020,'OIL',25.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2030,'spring','day','NG','R_NGH',2030,'RH',0.588235294117647);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2025,'summer','day','SOL','E_SOLPV',2020,'ELC',1.88537939382867);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'winter','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'spring','day','E10','T_GSL',2030,'VMT',15.0);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'winter','day','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2020,'winter','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'spring','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'spring','day','DSL','T_DSL',2030,'VMT',1.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'summer','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'winter','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'winter','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'fall','day','ELC','T_EV',2025,'VMT',1.40449438202247);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2030,'spring','night','NG','R_NGH',2020,'RH',11.7647058823529);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'spring','night','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'fall','day','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'winter','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'fall','day','ETH','T_BLND',2020,'E10',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'summer','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'summer','day','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2030,'spring','night','NG','R_NGH',2030,'RH',1.17647058823529);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'fall','night','OIL','S_OILREF',2020,'GSL',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2025,'spring','night','GSL','T_BLND',2020,'E10',22.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2020,'spring','day','NG','R_NGH',2020,'RH',5.88235294117647);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'winter','night','ELC','T_EV',2025,'VMT',1.40449438202247);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2030,'winter','night','URN','E_NUCLEAR',2015,'ELC',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'fall','day','ethos','S_IMPETH',2020,'ETH',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2030,'fall','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','electric',2020,'spring','night','NG','E_NGCC',2020,'ELC',15.6263891726251);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'spring','night','ethos','S_IMPURN',2020,'URN',0.985625);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2020,'spring','night','OIL','S_OILREF',2020,'DSL',2.5);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','transport',2030,'summer','day','ELC','T_EV',2030,'VMT',6.79775280898876);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','residential',2030,'winter','day','NG','R_NGH',2020,'RH',35.2941176470588);
INSERT INTO `Output_VFlow_In` (region,scenario,sector,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm,vflow_in) VALUES ('R1','test_run','supply',2025,'fall','night','ethos','S_IMPETH',2020,'ETH',2.5);
CREATE TABLE Output_Objective (
   scenario text,
   objective_name text,
   total_system_cost real );
INSERT INTO `Output_Objective` (scenario,objective_name,total_system_cost) VALUES ('test_run','TotalCost',525192.254438427);
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
INSERT INTO `Output_Emissions` (region,scenario,sector,t_periods,emissions_comm,tech,vintage,emissions) VALUES ('R1','test_run','supply',2020,'CO2','S_OILREF',2020,13484.0);
INSERT INTO `Output_Emissions` (region,scenario,sector,t_periods,emissions_comm,tech,vintage,emissions) VALUES ('R1','test_run','supply',2020,'CO2','S_IMPNG',2020,11516.0);
INSERT INTO `Output_Emissions` (region,scenario,sector,t_periods,emissions_comm,tech,vintage,emissions) VALUES ('R1','test_run','supply',2025,'CO2','S_IMPNG',2020,10167.2308474434);
INSERT INTO `Output_Emissions` (region,scenario,sector,t_periods,emissions_comm,tech,vintage,emissions) VALUES ('R1','test_run','supply',2030,'CO2','S_OILREF',2020,13484.0);
INSERT INTO `Output_Emissions` (region,scenario,sector,t_periods,emissions_comm,tech,vintage,emissions) VALUES ('R1','test_run','supply',2025,'CO2','S_OILREF',2020,13484.0);
INSERT INTO `Output_Emissions` (region,scenario,sector,t_periods,emissions_comm,tech,vintage,emissions) VALUES ('R1','test_run','supply',2030,'CO2','S_IMPNG',2020,9515.99999999999);
CREATE TABLE "Output_Curtailment" (
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
	PRIMARY KEY(region,scenario,t_periods,t_season,t_day,input_comm,tech,vintage,output_comm),
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
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_UndiscountedInvestmentByProcess','E_NGCC',2020,1545.53502066123);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_DiscountedInvestmentByProcess','E_NGCC',2020,1622.81177169429);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_UndiscountedInvestmentByProcess','E_NGCC',2025,183.418839253273);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_DiscountedInvestmentByProcess','E_NGCC',2025,150.899132977122);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_UndiscountedInvestmentByProcess','E_NGCC',2030,100.332258865544);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_DiscountedInvestmentByProcess','E_NGCC',2030,64.6750686490017);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_UndiscountedInvestmentByProcess','E_SOLPV',2020,484.34881419827);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_DiscountedInvestmentByProcess','E_SOLPV',2020,508.566254908183);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_UndiscountedInvestmentByProcess','E_SOLPV',2025,964.832652779003);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_DiscountedInvestmentByProcess','E_SOLPV',2025,793.770211201302);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_UndiscountedInvestmentByProcess','E_SOLPV',2030,851.29383576694);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_DiscountedInvestmentByProcess','E_SOLPV',2030,548.751596856619);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_UndiscountedInvestmentByProcess','E_BATT',2030,406.249854691252);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_DiscountedInvestmentByProcess','E_BATT',2030,261.872278546165);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','transport','V_UndiscountedInvestmentByProcess','T_GSL',2020,128500.0);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','transport','V_DiscountedInvestmentByProcess','T_GSL',2020,134925.0);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','transport','V_UndiscountedInvestmentByProcess','T_GSL',2030,39566.4734236976);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','transport','V_DiscountedInvestmentByProcess','T_GSL',2030,25504.90155221);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','transport','V_UndiscountedInvestmentByProcess','T_DSL',2020,16290.0);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','transport','V_DiscountedInvestmentByProcess','T_DSL',2020,17104.5);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','transport','V_UndiscountedInvestmentByProcess','T_DSL',2030,4941.41290313735);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','transport','V_DiscountedInvestmentByProcess','T_DSL',2030,3185.27881607601);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','transport','V_UndiscountedInvestmentByProcess','T_EV',2020,198400.0);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','transport','V_DiscountedInvestmentByProcess','T_EV',2020,208320.0);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','transport','V_UndiscountedInvestmentByProcess','T_EV',2025,26397.5996565571);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','transport','V_DiscountedInvestmentByProcess','T_EV',2025,21717.3705660148);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','transport','V_UndiscountedInvestmentByProcess','T_EV',2030,69153.4029949738);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','transport','V_DiscountedInvestmentByProcess','T_EV',2030,44576.9001573626);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','residential','V_UndiscountedInvestmentByProcess','R_NGH',2020,2025.58997601626);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','residential','V_DiscountedInvestmentByProcess','R_NGH',2020,2126.86947481708);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','residential','V_UndiscountedInvestmentByProcess','R_NGH',2025,150.689635559064);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','residential','V_DiscountedInvestmentByProcess','R_NGH',2025,123.972736099929);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','residential','V_UndiscountedInvestmentByProcess','R_NGH',2030,84.4897251255039);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','residential','V_DiscountedInvestmentByProcess','R_NGH',2030,54.4628301446907);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_UndiscountedFixedCostsByProcess','E_NGCC',2020,109.347070258562);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_DiscountedFixedCostsByProcess','E_NGCC',2020,438.68622790407);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_UndiscountedFixedCostsByProcess','E_NGCC',2025,6.96814460681281);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_DiscountedFixedCostsByProcess','E_NGCC',2025,22.133232799929);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_UndiscountedFixedCostsByProcess','E_NGCC',2030,3.48407230340642);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_DiscountedFixedCostsByProcess','E_NGCC',2030,9.72341610306789);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_UndiscountedFixedCostsByProcess','E_SOLPV',2020,24.8674010092811);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_DiscountedFixedCostsByProcess','E_SOLPV',2020,90.3402915711257);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_UndiscountedFixedCostsByProcess','E_SOLPV',2025,62.425723273348);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_DiscountedFixedCostsByProcess','E_SOLPV',2025,198.28564759722);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_UndiscountedFixedCostsByProcess','E_SOLPV',2030,34.3825915745611);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_DiscountedFixedCostsByProcess','E_SOLPV',2030,95.9555989278492);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_UndiscountedFixedCostsByProcess','E_BATT',2030,17.1751592137577);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_DiscountedFixedCostsByProcess','E_BATT',2030,47.9327652036747);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','supply','V_UndiscountedVariableCostsByProcess','S_IMPETH',2020,1920.0);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','supply','V_DiscountedVariableCostsByProcess','S_IMPETH',2020,6975.13020165736);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','supply','V_UndiscountedVariableCostsByProcess','S_IMPOIL',2020,12000.0);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','supply','V_DiscountedVariableCostsByProcess','S_IMPOIL',2020,43594.5637603585);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','supply','V_UndiscountedVariableCostsByProcess','S_IMPNG',2020,2481.05215486627);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','supply','V_DiscountedVariableCostsByProcess','S_IMPNG',2020,9154.90803782949);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','supply','V_UndiscountedVariableCostsByProcess','S_OILREF',2020,600.0);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','supply','V_DiscountedVariableCostsByProcess','S_OILREF',2020,2179.72818801793);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_UndiscountedVariableCostsByProcess','E_NGCC',2020,190.701269179635);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_DiscountedVariableCostsByProcess','E_NGCC',2020,746.52783723679);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_UndiscountedVariableCostsByProcess','E_NGCC',2025,11.938202247191);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_DiscountedVariableCostsByProcess','E_NGCC',2025,40.6813437017317);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_UndiscountedVariableCostsByProcess','E_NGCC',2030,2.52808988764046);
INSERT INTO `Output_Costs` (region,scenario,sector,output_name,tech,vintage,output_cost) VALUES ('R1','test_run','electric','V_DiscountedVariableCostsByProcess','E_NGCC',2030,7.05544196067703);
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
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','supply',2030,'S_IMPETH',20.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','electric',2030,'E_SOLPV',8.005323645305);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','transport',2025,'T_GSL',50.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','electric',2025,'E_NGCC',2.53621012732182);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','supply',2030,'S_OILREF',200.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','transport',2020,'T_DSL',6.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','electric',2025,'E_NUCLEAR',0.1);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','supply',2025,'S_OILREF',200.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','transport',2025,'T_DSL',6.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','supply',2025,'S_IMPNG',617.633837649462);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','supply',2020,'S_OILREF',200.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','transport',2030,'T_DSL',6.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','supply',2025,'S_IMPURN',7.885);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','supply',2025,'S_IMPETH',20.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','supply',2020,'S_IMPURN',7.885);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','electric',2030,'E_NGCC',2.89245473912207);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','electric',2030,'E_NUCLEAR',0.1);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','electric',2020,'E_NGCC',2.17996551552158);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','supply',2030,'S_IMPURN',7.885);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','supply',2025,'S_IMPOIL',200.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','electric',2030,'E_BATT',2.43619279627768);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','transport',2030,'T_GSL',50.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','transport',2020,'T_GSL',50.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','supply',2020,'S_IMPNG',617.633837649462);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','supply',2030,'S_IMPNG',617.633837649462);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','supply',2020,'S_IMPOIL',200.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','transport',2020,'T_EV',64.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','transport',2030,'T_EV',84.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','electric',2020,'E_SOLPV',0.797032083630804);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','supply',2030,'S_IMPOIL',200.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','electric',2020,'E_NUCLEAR',0.1);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','residential',2025,'R_NGH',352.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','transport',2025,'T_BLND',200.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','transport',2025,'T_EV',74.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','transport',2020,'T_BLND',200.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','residential',2030,'R_NGH',384.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','residential',2020,'R_NGH',320.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','supply',2020,'S_IMPETH',20.0);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','electric',2025,'E_SOLPV',4.22701687886971);
INSERT INTO `Output_CapacityByPeriodAndTech` (region,scenario,sector,t_periods,tech,capacity) VALUES ('R1','test_run','transport',2030,'T_BLND',200.0);
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
INSERT INTO `MinActivity` (region,periods,tech,minact,minact_units,minact_notes) VALUES ('R1',2020,'T_GSL',50.0,'','');
INSERT INTO `MinActivity` (region,periods,tech,minact,minact_units,minact_notes) VALUES ('R1',2025,'T_GSL',50.0,'','');
INSERT INTO `MinActivity` (region,periods,tech,minact,minact_units,minact_notes) VALUES ('R1',2030,'T_GSL',50.0,'','');
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
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('R1','S_IMPETH',100.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('R1','S_IMPOIL',100.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('R1','S_IMPNG',100.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('R1','S_IMPURN',100.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('R1','S_OILREF',100.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('R1','E_NGCC',30.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('R1','E_SOLPV',30.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('R1','E_BATT',20.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('R1','E_NUCLEAR',50.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('R1','T_BLND',100.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('R1','T_DSL',12.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('R1','T_GSL',12.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('R1','T_EV',12.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('R1','R_EH',20.0,'');
INSERT INTO `LifetimeTech` (region,tech,life,life_notes) VALUES ('R1','R_NGH',20.0,'');
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
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('R1','S_IMPETH',100.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('R1','S_IMPOIL',100.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('R1','S_IMPNG',100.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('R1','S_IMPURN',100.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('R1','S_OILREF',100.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('R1','E_NGCC',30.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('R1','E_SOLPV',30.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('R1','E_BATT',20.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('R1','E_NUCLEAR',50.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('R1','T_BLND',100.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('R1','T_DSL',12.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('R1','T_GSL',12.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('R1','T_EV',12.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('R1','R_EH',20.0,'');
INSERT INTO `LifetimeLoanTech` (region,tech,loan,loan_notes) VALUES ('R1','R_NGH',20.0,'');
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
INSERT INTO `ExistingCapacity` (region,tech,vintage,exist_cap,exist_cap_units,exist_cap_notes) VALUES ('R1','E_NUCLEAR',2015,0.1,'GW','');
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
INSERT INTO `EmissionLimit` (region,periods,emis_comm,emis_limit,emis_limit_units,emis_limit_notes) VALUES ('R1',2020,'CO2',25000.0,'kT CO2','');
INSERT INTO `EmissionLimit` (region,periods,emis_comm,emis_limit,emis_limit_units,emis_limit_notes) VALUES ('R1',2025,'CO2',24000.0,'kT CO2','');
INSERT INTO `EmissionLimit` (region,periods,emis_comm,emis_limit,emis_limit_units,emis_limit_notes) VALUES ('R1',2030,'CO2',23000.0,'kT CO2','');
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
INSERT INTO `EmissionActivity` (region,emis_comm,input_comm,tech,vintage,output_comm,emis_act,emis_act_units,emis_act_notes) VALUES ('R1','CO2','ethos','S_IMPNG',2020,'NG',50.3,'kT/PJ','taken from MIT Energy Fact Sheet');
INSERT INTO `EmissionActivity` (region,emis_comm,input_comm,tech,vintage,output_comm,emis_act,emis_act_units,emis_act_notes) VALUES ('R1','CO2','OIL','S_OILREF',2020,'GSL',67.2,'kT/PJ','taken from MIT Energy Fact Sheet');
INSERT INTO `EmissionActivity` (region,emis_comm,input_comm,tech,vintage,output_comm,emis_act,emis_act_units,emis_act_notes) VALUES ('R1','CO2','OIL','S_OILREF',2020,'DSL',69.4,'kT/PJ','taken from MIT Energy Fact Sheet');
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
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','ethos','S_IMPETH',2020,'ETH',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','ethos','S_IMPOIL',2020,'OIL',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','ethos','S_IMPNG',2020,'NG',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','ethos','S_IMPURN',2020,'URN',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','OIL','S_OILREF',2020,'GSL',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','OIL','S_OILREF',2020,'DSL',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','ETH','T_BLND',2020,'E10',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','GSL','T_BLND',2020,'E10',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','NG','E_NGCC',2020,'ELC',0.55,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','NG','E_NGCC',2025,'ELC',0.55,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','NG','E_NGCC',2030,'ELC',0.55,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','SOL','E_SOLPV',2020,'ELC',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','SOL','E_SOLPV',2025,'ELC',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','SOL','E_SOLPV',2030,'ELC',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','URN','E_NUCLEAR',2015,'ELC',0.4,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','URN','E_NUCLEAR',2020,'ELC',0.4,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','URN','E_NUCLEAR',2025,'ELC',0.4,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','URN','E_NUCLEAR',2030,'ELC',0.4,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','ELC','E_BATT',2020,'ELC',0.85,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','ELC','E_BATT',2025,'ELC',0.85,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','ELC','E_BATT',2030,'ELC',0.85,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','E10','T_GSL',2020,'VMT',0.25,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','E10','T_GSL',2025,'VMT',0.25,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','E10','T_GSL',2030,'VMT',0.25,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','DSL','T_DSL',2020,'VMT',0.3,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','DSL','T_DSL',2025,'VMT',0.3,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','DSL','T_DSL',2030,'VMT',0.3,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','ELC','T_EV',2020,'VMT',0.89,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','ELC','T_EV',2025,'VMT',0.89,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','ELC','T_EV',2030,'VMT',0.89,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','ELC','R_EH',2020,'RH',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','ELC','R_EH',2025,'RH',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','ELC','R_EH',2030,'RH',1.0,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','NG','R_NGH',2020,'RH',0.85,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','NG','R_NGH',2025,'RH',0.85,'');
INSERT INTO `Efficiency` (region,input_comm,tech,vintage,output_comm,efficiency,eff_notes) VALUES ('R1','NG','R_NGH',2030,'RH',0.85,'');
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
INSERT INTO `DemandSpecificDistribution` (region,season_name,time_of_day_name,demand_name,dds,dds_notes) VALUES ('R1','spring','day','RH',0.05,'');
INSERT INTO `DemandSpecificDistribution` (region,season_name,time_of_day_name,demand_name,dds,dds_notes) VALUES ('R1','spring','night','RH',0.1,'');
INSERT INTO `DemandSpecificDistribution` (region,season_name,time_of_day_name,demand_name,dds,dds_notes) VALUES ('R1','summer','day','RH',0.0,'');
INSERT INTO `DemandSpecificDistribution` (region,season_name,time_of_day_name,demand_name,dds,dds_notes) VALUES ('R1','summer','night','RH',0.0,'');
INSERT INTO `DemandSpecificDistribution` (region,season_name,time_of_day_name,demand_name,dds,dds_notes) VALUES ('R1','fall','day','RH',0.05,'');
INSERT INTO `DemandSpecificDistribution` (region,season_name,time_of_day_name,demand_name,dds,dds_notes) VALUES ('R1','fall','night','RH',0.1,'');
INSERT INTO `DemandSpecificDistribution` (region,season_name,time_of_day_name,demand_name,dds,dds_notes) VALUES ('R1','winter','day','RH',0.3,'');
INSERT INTO `DemandSpecificDistribution` (region,season_name,time_of_day_name,demand_name,dds,dds_notes) VALUES ('R1','winter','night','RH',0.4,'');
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
INSERT INTO `Demand` (region,periods,demand_comm,demand,demand_units,demand_notes) VALUES ('R1',2020,'RH',100.0,'','');
INSERT INTO `Demand` (region,periods,demand_comm,demand,demand_units,demand_notes) VALUES ('R1',2025,'RH',110.0,'','');
INSERT INTO `Demand` (region,periods,demand_comm,demand,demand_units,demand_notes) VALUES ('R1',2030,'RH',120.0,'','');
INSERT INTO `Demand` (region,periods,demand_comm,demand,demand_units,demand_notes) VALUES ('R1',2020,'VMT',120.0,'','');
INSERT INTO `Demand` (region,periods,demand_comm,demand,demand_units,demand_notes) VALUES ('R1',2025,'VMT',130.0,'','');
INSERT INTO `Demand` (region,periods,demand_comm,demand,demand_units,demand_notes) VALUES ('R1',2030,'VMT',140.0,'','');
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
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2020,'S_IMPETH',2020,32.0,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2025,'S_IMPETH',2020,32.0,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2030,'S_IMPETH',2020,32.0,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2020,'S_IMPOIL',2020,20.0,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2025,'S_IMPOIL',2020,20.0,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2030,'S_IMPOIL',2020,20.0,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2020,'S_IMPNG',2020,4.0,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2025,'S_IMPNG',2020,4.0,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2030,'S_IMPNG',2020,4.0,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2020,'S_OILREF',2020,1.0,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2025,'S_OILREF',2020,1.0,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2030,'S_OILREF',2020,1.0,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2020,'E_NGCC',2020,1.6,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2025,'E_NGCC',2020,1.6,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2025,'E_NGCC',2025,1.7,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2030,'E_NGCC',2020,1.6,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2030,'E_NGCC',2025,1.7,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2030,'E_NGCC',2030,1.8,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2020,'E_NUCLEAR',2020,0.24,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2025,'E_NUCLEAR',2020,0.24,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2025,'E_NUCLEAR',2025,0.25,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2030,'E_NUCLEAR',2020,0.24,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2030,'E_NUCLEAR',2025,0.25,'$M/PJ','');
INSERT INTO `CostVariable` (region,periods,tech,vintage,cost_variable,cost_variable_units,cost_variable_notes) VALUES ('R1',2030,'E_NUCLEAR',2030,0.26,'$M/PJ','');
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
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','E_NGCC',2020,1050.0,'$M/GW','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','E_NGCC',2025,1025.0,'$M/GW','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','E_NGCC',2030,1000.0,'$M/GW','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','E_SOLPV',2020,900.0,'$M/GW','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','E_SOLPV',2025,560.0,'$M/GW','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','E_SOLPV',2030,800.0,'$M/GW','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','E_NUCLEAR',2020,6145.0,'$M/GW','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','E_NUCLEAR',2025,6045.0,'$M/GW','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','E_NUCLEAR',2030,5890.0,'$M/GW','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','E_BATT',2020,1150.0,'$M/GW','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','E_BATT',2025,720.0,'$M/GW','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','E_BATT',2030,480.0,'$M/GW','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','T_GSL',2020,2570.0,'$/bvmt/yr','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','T_GSL',2025,2700.0,'$/bvmt/yr','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','T_GSL',2030,2700.0,'$/bvmt/yr','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','T_DSL',2020,2715.0,'$/bvmt/yr','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','T_DSL',2025,2810.0,'$/bvmt/yr','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','T_DSL',2030,2810.0,'$/bvmt/yr','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','T_EV',2020,3100.0,'$/bvmt/yr','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','T_EV',2025,3030.0,'$/bvmt/yr','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','T_EV',2030,2925.0,'$/bvmt/yr','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','R_EH',2020,4.1,'$/PJ/yr','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','R_EH',2025,4.1,'$/PJ/yr','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','R_EH',2030,4.1,'$/PJ/yr','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','R_NGH',2020,7.6,'$/PJ/yr','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','R_NGH',2025,7.6,'$/PJ/yr','');
INSERT INTO `CostInvest` (region,tech,vintage,cost_invest,cost_invest_units,cost_invest_notes) VALUES ('R1','R_NGH',2030,7.6,'$/PJ/yr','');
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
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2020,'E_NGCC',2020,30.6,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2025,'E_NGCC',2020,9.78,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2025,'E_NGCC',2025,9.78,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2030,'E_NGCC',2020,9.78,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2030,'E_NGCC',2025,9.78,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2030,'E_NGCC',2030,9.78,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2020,'E_SOLPV',2020,10.4,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2025,'E_SOLPV',2020,10.4,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2025,'E_SOLPV',2025,9.1,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2030,'E_SOLPV',2020,10.4,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2030,'E_SOLPV',2025,9.1,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2030,'E_SOLPV',2030,9.1,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2020,'E_NUCLEAR',2020,98.1,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2025,'E_NUCLEAR',2020,98.1,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2025,'E_NUCLEAR',2025,98.1,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2030,'E_NUCLEAR',2020,98.1,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2030,'E_NUCLEAR',2025,98.1,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2030,'E_NUCLEAR',2030,98.1,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2020,'E_BATT',2020,7.05,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2025,'E_BATT',2020,7.05,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2025,'E_BATT',2025,7.05,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2030,'E_BATT',2020,7.05,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2030,'E_BATT',2025,7.05,'$M/GWyr','');
INSERT INTO `CostFixed` (region,periods,tech,vintage,cost_fixed,cost_fixed_units,cost_fixed_notes) VALUES ('R1',2030,'E_BATT',2030,7.05,'$M/GWyr','');
CREATE TABLE "CapacityToActivity" (
	`region`	text,
	`tech`	text,
	`c2a`	real,
	`c2a_notes`	TEXT,
	PRIMARY KEY(region,tech),
	FOREIGN KEY(`tech`) REFERENCES `technologies`(`tech`)
);
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('R1','S_IMPETH',1.0,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('R1','S_IMPOIL',1.0,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('R1','S_IMPNG',1.0,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('R1','S_IMPURN',1.0,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('R1','S_OILREF',1.0,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('R1','E_NGCC',31.54,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('R1','E_SOLPV',31.54,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('R1','E_BATT',31.54,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('R1','E_NUCLEAR',31.54,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('R1','T_BLND',1.0,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('R1','T_DSL',1.0,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('R1','T_GSL',1.0,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('R1','T_EV',1.0,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('R1','R_EH',1.0,'');
INSERT INTO `CapacityToActivity` (region,tech,c2a,c2a_notes) VALUES ('R1','R_NGH',1.0,'');
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
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('R1','spring','day','E_SOLPV',0.6,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('R1','spring','night','E_SOLPV',0.0,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('R1','summer','day','E_SOLPV',0.6,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('R1','summer','night','E_SOLPV',0.0,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('R1','fall','day','E_SOLPV',0.6,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('R1','fall','night','E_SOLPV',0.0,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('R1','winter','day','E_SOLPV',0.6,'');
INSERT INTO `CapacityFactorTech` (region,season_name,time_of_day_name,tech,cf_tech,cf_tech_notes) VALUES ('R1','winter','night','E_SOLPV',0.0,'');
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
