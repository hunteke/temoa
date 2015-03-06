import sqlite3

#Below is a list of tables comprising sets and params that must be exported to
#the Temoa DAT file.
temoa_tables = [
'time_periods',
'time_season',
'time_of_day',
'technologies',
'commodities',
'SegFrac',
'DemandSpecificDistribution',
'CapacityToActivity',
'GlobalDiscountRate',
'EmissionActivity',
'Demand',
'TechOutputSplit',
'MinCapacity',
'MaxCapacity',
'LifetimeTech',
'LifetimeProcess',
'LifetimeLoanTech',
'CapacityFactorTech',
'CapacityFactorProcess',
'Efficiency',
'ExistingCapacity',
'CostInvest',
'CostFixed',
'CostVariable']

#create a file to write output
f = open('temoa_input.dat', 'w')
f.write('data ;\n\n')
#connect to the database
con = sqlite3.connect("temoa_utopia.db")
cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding

for i in temoa_tables:
	#Split 'time_periods' into 'time_exist' and 'time_future':
	if i == 'time_periods':  
		f.write("set  time_exist   :=\n")
		cur.execute("SELECT t_periods FROM  "+i+"  WHERE flag=='e'")
		for row in cur:
			str_row = str(row) + '\n'
			str_row_clean = str_row.replace('(','').replace(')','').replace(',',' ').replace('\'',' ')
			print str_row_clean
			f.write(str_row_clean)
		f.write(';\n\n')
		f.write("set  time_future   :=\n")
		cur.execute("SELECT t_periods FROM  "+i+"  WHERE flag=='f'")
		for row in cur:
			str_row = str(row) + '\n'
			str_row_clean = str_row.replace('(','').replace(')','').replace(',',' ').replace('\'',' ')
			print str_row_clean
			f.write(str_row_clean)
		f.write(';\n\n')
	#split technology table into production, baseload, and storage: 
	elif i == 'technologies':
		f.write("set  tech_resource   :=\n")
		cur.execute("SELECT tech, tech_desc FROM  "+i+"  WHERE flag=='r'")
		for row in cur:
			str_row = str(row) + '\n'
			str_row_clean = str_row.replace('(','').replace(')','').replace(',',' ').replace('\'',' ')
			print str_row_clean
			f.write(str_row_clean)
		f.write(';\n\n')
		f.write("set  tech_production   :=\n")
		cur.execute("SELECT tech, tech_desc FROM  "+i+"  WHERE flag=='p' OR flag=='pb' OR flag=='ps'")
		for row in cur:
			str_row = str(row) + '\n'
			str_row_clean = str_row.replace('(','').replace(')','').replace(',',' ').replace('\'',' ')
			print str_row_clean
			f.write(str_row_clean)
		f.write(';\n\n')
		f.write("set  tech_baseload   :=\n")
		cur.execute("SELECT tech, tech_desc FROM  "+i+"  WHERE flag=='pb'")
		for row in cur:
			str_row = str(row) + '\n'
			str_row_clean = str_row.replace('(','').replace(')','').replace(',',' ').replace('\'',' ')
			print str_row_clean
			f.write(str_row_clean)
		f.write(';\n\n')
		f.write("set  tech_storage   :=\n")
		cur.execute("SELECT tech, tech_desc FROM  "+i+"  WHERE flag=='ps'")
		for row in cur:
			str_row = str(row) + '\n'
			str_row_clean = str_row.replace('(','').replace(')','').replace(',',' ').replace('\'',' ')
			print str_row_clean
			f.write(str_row_clean)
		f.write(';\n\n')
	#split commodity table into physical, emissions, and demand commodities	
	elif i == 'commodities':
		f.write("set  commodity_physical   :=\n")
		cur.execute("SELECT comm_name, comm_desc FROM  "+i+"  WHERE flag=='p'")
		for row in cur:
			str_row = str(row) + '\n'
			str_row_clean = str_row.replace('(','').replace(')','').replace(',',' ').replace('\'',' ')
			print str_row_clean
			f.write(str_row_clean)
		f.write(';\n\n')
		f.write("set  commodity_emissions   :=\n")
		cur.execute("SELECT comm_name, comm_desc FROM  "+i+"  WHERE flag=='e'")
		for row in cur:
			str_row = str(row) + '\n'
			str_row_clean = str_row.replace('(','').replace(')','').replace(',',' ').replace('\'',' ')
			print str_row_clean
			f.write(str_row_clean)
		f.write(';\n\n')
		f.write("set  commodity_demand   :=\n")
		cur.execute("SELECT comm_name, comm_desc FROM  "+i+"  WHERE flag=='d'")
		for row in cur:
			str_row = str(row) + '\n'
			str_row_clean = str_row.replace('(','').replace(')','').replace(',',' ').replace('\'',' ')
			print str_row_clean
			f.write(str_row_clean)
		f.write(';\n\n')
		
	#Output remaining sets 'time_season' and 'time_of_day'	
	elif i == 'time_season' or i == 'time_of_day':
		f.write("set  "+i+"   :=\n")
		cur.execute("SELECT * FROM "+i)
		for row in cur:
			str_row = str(row) + '\n'
			str_row_clean = str_row.replace('(','').replace(')','').replace(',',' ').replace('\'',' ')
			print str_row_clean
			f.write(str_row_clean)
		f.write(';\n\n')
	#Now output all of the parameter values
	else:	
		f.write("param  "+i+"   :=\n")
		cur.execute("SELECT * FROM "+i)
		for row in cur:
			str_row = str(row) + '\n'
			str_row_clean = str_row.replace('(','').replace(')','').replace(',',' ').replace('\'',' ')
			print str_row_clean
			f.write(str_row_clean)
		f.write(';\n\n')

   
f.close()   
cur.close()
con.close()
