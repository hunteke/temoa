import sqlite3
import sys, os
import re
import getopt
import pandas as pd
import xlsxwriter

def make_excel(ifile, ofile, scenario):
	
	if ifile is None :
		raise "You did not specify the input file, remember to use '-i' option"
		print("Use as :\n	python DB_to_Excel.py -i <input_file> (Optional -o <output_excel_file_name_only>)\n	Use -h for help.")                          
		sys.exit(2)
	else :
		file_type = re.search(r"(\w+)\.(\w+)\b", ifile) # Extract the input filename and extension
	if not file_type :
		print("The file type %s is not recognized. Use a db file." % ifile)
		sys.exit(2)
	if ofile is None :
		ofile = file_type.group(1)
		print("Look for output in %s_*.xls" % ofile)

	con = sqlite3.connect(ifile)
	cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
	con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding
	scenario = scenario.pop()
	writer = pd.ExcelWriter(ofile+'.xlsx', engine = 'xlsxwriter', options={'strings_to_formulas': False})

	workbook  = writer.book

	header_format = workbook.add_format({'bold': True,'text_wrap': True,'align': 'left',})

	query = "SELECT DISTINCT Efficiency.regions, Efficiency.tech, technologies.sector FROM Efficiency \
	INNER JOIN technologies ON Efficiency.tech=technologies.tech"
	all_techs = pd.read_sql_query(query, con)

	query = "SELECT regions, tech, sector, t_periods, capacity FROM Output_CapacityByPeriodAndTech WHERE scenario='" + scenario + "'"
	df_capacity = pd.read_sql_query(query, con)
	for sector in sorted(df_capacity['sector'].unique()):
		df_capacity_sector = df_capacity[df_capacity['sector']==sector]
		df_capacity_sector = df_capacity_sector.drop(columns=['sector']).pivot_table(values='capacity', index=['regions', 'tech'], columns='t_periods')
		df_capacity_sector.reset_index(inplace=True)
		sector_techs = all_techs[all_techs['sector']==sector]
		df_capacity_sector = pd.merge(sector_techs[['regions','tech']], df_capacity_sector, on=['regions','tech'], how='left')
		df_capacity_sector.rename(columns={'regions':'Region','tech':'Technology'}, inplace=True)
		df_capacity_sector.to_excel(writer, sheet_name='Capacity_' + sector, index=False, encoding='utf-8', startrow=1, header=False)
		worksheet = writer.sheets['Capacity_' + sector]
		worksheet.set_column('A:A', 10)
		worksheet.set_column('B:B', 10)
		for col, val in enumerate(df_capacity_sector.columns.values):
			worksheet.write(0, col, val, header_format)

	query = "SELECT regions, tech, sector, t_periods, sum(vflow_out) as vflow_out FROM Output_VFlow_Out WHERE scenario='" + scenario + "' GROUP BY \
	regions, tech, sector, t_periods"
	df_activity = pd.read_sql_query(query, con)
	for sector in sorted(df_activity['sector'].unique()):
		df_activity_sector = df_activity[df_activity['sector']==sector]
		df_activity_sector = df_activity_sector.drop(columns=['sector']).pivot_table(values='vflow_out', index=['regions', 'tech'], columns='t_periods')
		df_activity_sector.reset_index(inplace=True)
		sector_techs = all_techs[all_techs['sector']==sector]
		df_activity_sector = pd.merge(sector_techs[['regions','tech']], df_activity_sector, on=['regions','tech'], how='left')
		df_activity_sector.rename(columns={'regions':'Region','tech':'Technology'}, inplace=True)
		df_activity_sector.to_excel(writer, sheet_name='Activity_' + sector, index=False, encoding='utf-8', startrow=1, header=False)
		worksheet = writer.sheets['Activity_' + sector]
		worksheet.set_column('A:A', 10)
		worksheet.set_column('B:B', 10)
		for col, val in enumerate(df_activity_sector.columns.values):
			worksheet.write(0, col, val, header_format)

	query = "SELECT DISTINCT EmissionActivity.regions, EmissionActivity.tech, EmissionActivity.emis_comm as emissions_comm, technologies.sector FROM EmissionActivity \
	INNER JOIN technologies ON EmissionActivity.tech=technologies.tech"
	all_emis_techs = pd.read_sql_query(query, con)

	query = "SELECT regions, tech, sector, t_periods, emissions_comm, sum(emissions) as emissions FROM Output_Emissions WHERE scenario='" + scenario + "' GROUP BY \
	regions, tech, sector, t_periods, emissions_comm"
	df_emissions = pd.read_sql_query(query, con)
	df_emissions = df_emissions.pivot_table(values='emissions', index=['regions', 'tech', 'sector','emissions_comm'], columns='t_periods')
	df_emissions.reset_index(inplace=True)
	df_emissions = pd.merge(all_emis_techs, df_emissions, on=['regions','tech', 'sector', 'emissions_comm'], how='left')
	df_emissions.rename(columns={'regions':'Region', 'tech':'Technology', 'emissions_comm':'Emission Commodity', 'sector':'Sector'}, inplace=True)
	df_emissions.to_excel(writer, sheet_name='Emissions', index=False, encoding='utf-8', startrow=1, header=False)
	worksheet = writer.sheets['Emissions']
	worksheet.set_column('A:A', 10)
	worksheet.set_column('B:B', 10)
	worksheet.set_column('C:C', 10)
	worksheet.set_column('D:D', 20)
	for col, val in enumerate(df_emissions.columns.values):
		worksheet.write(0, col, val, header_format)

	query = "SELECT regions, tech, sector, output_name,  vintage, output_cost FROM Output_Costs WHERE output_name LIKE '%V_Discounted%' AND scenario='" + scenario + "'"
	df_costs = pd.read_sql_query(query, con)
	df_costs.columns = ['Region', 'Technology', 'Sector','Output Name', 'Vintage', 'Cost']
	df_costs.to_excel(writer, sheet_name='Costs', index=False, encoding='utf-8', startrow=1, header=False)
	worksheet = writer.sheets['Costs']
	worksheet.set_column('A:A', 10)
	worksheet.set_column('B:B', 10)
	worksheet.set_column('C:C', 10)
	worksheet.set_column('D:D', 30)
	for col, val in enumerate(df_costs.columns.values):
		worksheet.write(0, col, val, header_format)

	writer.save()


	cur.close()
	con.close()


def get_data(inputs):

	ifile = None
	ofile = None
	scenario = set()
	
	if inputs is None:
		raise "no arguments found"
		
	for opt, arg in inputs.items():
		if opt in ("-i", "--input"):
			ifile = arg
		elif opt in ("-o", "--output"):
			ofile = arg
		elif opt in ("-s", "--scenario"):
			scenario.add(arg)
		elif opt in ("-h", "--help") :
			print("Use as :\n	python DB_to_Excel.py -i <input_file> (Optional -o <output_excel_file_name_only>)\n	Use -h for help.")                         
			sys.exit()
		
	make_excel(ifile, ofile, scenario)

if __name__ == "__main__":	
	
	try:
		argv = sys.argv[1:]
		opts, args = getopt.getopt(argv, "hi:o:s:", ["help", "input=", "output=", "scenario="])
	except getopt.GetoptError:          
		print("Something's Wrong. Use as :\n	python DB_to_Excel.py -i <input_file> (Optional -o <output_excel_file_name_only>)\n	Use -h for help.")                          
		sys.exit(2) 
		
	print(opts)
		
	get_data( dict(opts) )