import sqlite3
import sys, os
import xlwt
from xlwt import easyxf 
from collections import defaultdict

ifile = sys.argv[1]
tech = defaultdict(list)
sector = set()
period = []
row = 0
count = 0
sheet = []
i = 0 # Sheet ID
header = ['Technologies']


book = xlwt.Workbook(encoding="utf-8")
if os.path.exists("Test.xls") :
	os.remove("Test.xls")

con = sqlite3.connect(ifile)
cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding


cur.execute("SELECT sector FROM technologies")
for val in cur :
	sector.add(val[0])

for x in sector :
	cur.execute("SELECT tech FROM technologies WHERE sector is '"+x+"'")
	for val in cur :
		tech[x].append(val[0])
	
cur.execute("SELECT t_periods FROM time_periods")
for val in cur :
	val = str(val[0])
	if val not in period :
		period.append(val)
		header.append(val)
header[1:].sort()
period.sort()
	
	
for z in sector :
	sheet.append(book.add_sheet('Activity_'+z))
	for col in range(0, len(header)) :
		sheet[i].write(row, col, header[col], easyxf('alignment: vertical centre, horizontal centre, wrap True;'))
		sheet[i].col(col).width_in_pixels = 3300
	row += 1
	for x in tech[z] :
		sheet[i].write(row, 0, x, easyxf('alignment: vertical centre, horizontal centre;'))
		for y in period :
			cur.execute("SELECT sum(vflow_out) FROM Output_VFlow_Out WHERE t_periods is '"+y+"' and tech is '"+x+"'")
			z = cur.fetchone()
			if z[0] is not None :
				sheet[i].write(row, count+1, float(z[0]), easyxf('alignment: vertical centre, horizontal centre;'))
			else :
				sheet[i].write(row, count+1, '-', easyxf('alignment: vertical centre, horizontal centre;'))
			count += 1
		row += 1
		count = 0
	row = 0
	i += 1

cur.close()
con.close()

book.save("Test.xls")