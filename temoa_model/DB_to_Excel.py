import sqlite3
import sys, os
import re
import getopt
import xlwt
from xlwt import easyxf 
from collections import defaultdict

def make_excel(ifile, ofile, scenario):
	tech = defaultdict(list)
	tech_set = set()
	sector = set()
	period = []
	emiss = set()
	row = 0
	count = 0
	sheet = []
	book = []
	book_no = 0
	flag = None
	flag1 = None
	flag2 = None
	i = 0 # Sheet ID
	header = ['Technologies', ]
	header_emiss = []
	header_v = ['Technologies', 'Output Name', 'Vintage', 'Cost']
	tables = {"Output_VFlow_Out" : ["Activity", "vflow_out"], "Output_CapacityByPeriodAndTech" : ["Capacity", "capacity"], "Output_Emissions" : ["Emissions", "emissions"], "Output_Costs" : ["Costs", "output_cost"]}

	
	if ifile is None :
		raise "You did not specify the input file, remember to use '-i' option"
		print "Use as :\n	python DB_to_Excel.py -i <input_file> (Optional -o <output_excel_file_name_only>)\n	Use -h for help."                          
		sys.exit(2)
	else :
		file_type = re.search(r"(\w+)\.(\w+)\b", ifile) # Extract the input filename and extension
	if not file_type :
		print "The file type %s is not recognized. Use a db file." % ifile
		sys.exit(2)
	if ofile is None :
		ofile = file_type.group(1)
		print "Look for output in %s_*.xls" % ofile
		
		
	con = sqlite3.connect(ifile)
	cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
	con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding

	for k in tables.keys() :
		if not scenario :
			cur.execute("SELECT DISTINCT scenario FROM "+k)
			for val in cur :
				scenario.add(val[0])
		
		for axy in cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='technologies';") :
			if axy[0] :
				fields = [ads[1] for ads in cur.execute('PRAGMA table_info(technologies)')]
				if 'sector' in fields :
					cur.execute("SELECT sector FROM technologies")
					for val in cur :
						sector.add(val[0])
					if not sector :
						sector.add('0')
					else :
						flag = 1
		
		if flag is None :
			cur.execute("SELECT DISTINCT tech FROM "+k)
			for val in cur :
				tech['0'].append(val[0])
				tech_set.add(val[0])
		else :
			for x in sector :
				cur.execute("SELECT DISTINCT tech  FROM technologies WHERE sector is '"+x+"'")
				for val in cur :
					if val[0] not in tech[x] :
						tech[x].append(val[0])
						tech_set.add(val[0])

		if k is "Output_Emissions" :
			cur.execute("SELECT DISTINCT emissions_comm FROM "+k)
			for val in cur :
				emiss.add(val[0])
		
		if k is "Output_Costs" :
			pass
		else:#if k is not "Output_V_Capacity":
			cur.execute("SELECT DISTINCT t_periods FROM "+k)
			for val in cur :
				val = str(val[0])
				if val not in period :
					period.append(val)
					header.append(val)
	header[1:].sort()
	period.sort()
	header_emiss = header[:]
	header_emiss.insert(1, "Emission Commodity")

	ostyle = easyxf('alignment: vertical centre, horizontal centre;')
	ostyle_header = easyxf('alignment: vertical centre, horizontal centre, wrap True;')

	for scene in scenario :	
		book.append(xlwt.Workbook(encoding="utf-8"))
		for z in sector :
			for a in tables.keys() :
				if z is '0' :
					sheet_name = str(tables[a][0])
					if a is "Output_Costs" :
						flag2 = '1'
					if a is "Output_Emissions" :
						flag1 = '1'
				elif (a is "Output_Costs" and flag2 is None) :
					sheet_name = str(tables[a][0])
					flag2 = '1'
				elif (a is "Output_Emissions" and flag1 is None) :
					sheet_name = str(tables[a][0])
					flag1 = '1'
				elif (a is "Output_Costs" and flag2 is not None) or (a is "Output_Emissions" and flag1 is not None) :
					continue
				else :
					sheet_name = str(tables[a][0])+"_"+str(z)
				sheet.append(book[book_no].add_sheet(sheet_name))
				if a is "Output_Emissions" and flag1 is '1':
					for col in range(0, len(header_emiss)) :
						sheet[i].write(row, col, header_emiss[col], ostyle_header)
						sheet[i].col(col).width_in_pixels = 3300
					row += 1
					for x in tech_set :
						for q in emiss :
							sheet[i].write(row, 0, x, ostyle)
							sheet[i].write(row, 1, q, ostyle)
							for y in period :
								cur.execute("SELECT sum("+tables[a][1]+") FROM "+a+" WHERE t_periods is '"+y+"' and scenario is '"+scene+"' and tech is '"+x+"' and emissions_comm is '"+q+"'")
								xyz = cur.fetchone()
								if xyz[0] is not None :
									sheet[i].write(row, count+2, float(xyz[0]), ostyle)
								else :
									sheet[i].write(row, count+2, '-', ostyle)
								count += 1
							row += 1
							count = 0
					row = 0
					i += 1
					flag1 = '2'
				elif a is "Output_Costs" and flag2 is '1':
					for col in range(0, len(header_v)) :
						sheet[i].write(row, col, header_v[col], ostyle_header)
						sheet[i].col(col).width_in_pixels = 3300
					row += 1
					for x in tech_set :			
						cur.execute("SELECT output_name, vintage, "+tables[a][1]+" FROM "+a+" WHERE scenario is '"+scene+"' and tech is '"+x+"'")
						for xyz in cur :
							if xyz[0] is not None :
								sheet[i].write(row, 0, x, ostyle)
								sheet[i].write(row, count+1, xyz[0], ostyle)
								sheet[i].write(row, count+2, xyz[1], ostyle)
								sheet[i].write(row, count+3, xyz[2], ostyle)
							else :
								sheet[i].write(row, 0, x, ostyle)
								sheet[i].write(row, count+1, '-', ostyle)
								sheet[i].write(row, count+2, '-', ostyle)
								sheet[i].write(row, count+3, '-', ostyle)
							row += 1
						count = 0
					row = 0
					i += 1
					flag2 = '2'
				elif (a is "Output_Costs" and flag2 is '2') or (a is "Output_Emissions" and flag1 is '2'):
					pass
				elif a is not "Output_V_Capacity":
					for col in range(0, len(header)) :
						sheet[i].write(row, col, header[col], ostyle_header)
						sheet[i].col(col).width_in_pixels = 3300
					row += 1
					for x in tech[z] :
						sheet[i].write(row, 0, x, ostyle)
						for y in period :
							cur.execute("SELECT sum("+tables[a][1]+") FROM "+a+" WHERE t_periods is '"+y+"' and scenario is '"+scene+"' and tech is '"+x+"'")
							xyz = cur.fetchone()
							if xyz[0] is not None :
								sheet[i].write(row, count+1, float(xyz[0]), ostyle)
							else :
								sheet[i].write(row, count+1, '-', ostyle)
							count += 1
						row += 1
						count = 0
					row = 0
					i += 1
		if len(scenario) is 1:
			book[book_no].save(ofile+".xls")
		else :
			book[book_no].save(ofile+"_"+scene+".xls")
		book_no += 1
		flag1 = None
		flag2 = None

	cur.close()
	con.close()


def get_data(inputs):

	ifile = None
	ofile = None
	scenario = set()
	
	if inputs is None:
		raise "no arguments found"
		
	for opt, arg in inputs.iteritems():
		if opt in ("-i", "--input"):
			ifile = arg
		elif opt in ("-o", "--output"):
			ofile = arg
		elif opt in ("-s", "--scenario"):
			scenario.add(arg)
		elif opt in ("-h", "--help") :
			print "Use as :\n	python DB_to_Excel.py -i <input_file> (Optional -o <output_excel_file_name_only>)\n	Use -h for help."                          
			sys.exit()
		
	make_excel(ifile, ofile, scenario)

if __name__ == "__main__":	
	
	try:
		argv = sys.argv[1:]
		opts, args = getopt.getopt(argv, "hi:o:s:", ["help", "input=", "output=", "scenario="])
	except getopt.GetoptError:          
		print "Something's Wrong. Use as :\n	python DB_to_Excel.py -i <input_file> (Optional -o <output_excel_file_name_only>)\n	Use -h for help."                          
		sys.exit(2) 
		
	print opts
		
	get_data( dict(opts) )
