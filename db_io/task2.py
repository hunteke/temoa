import sqlite3
import sys, os
import xlwt
from xlwt import easyxf 

ifile = sys.argv[1]
tech = set()
period = set()
activity = []
row = 0
count = 0
flag = 0
header = ['Technologies', 'Time Period', 'Activity']


book = xlwt.Workbook(encoding="utf-8")
if os.path.exists("Test.xls") :
	os.remove("Test.xls")

sheet = book.add_sheet('Activity')
for col in range(0, len(header)) :
	sheet.write(row, col, header[col], easyxf('alignment: vertical centre, horizontal centre, wrap True;'))
	sheet.col(col).width_in_pixels = 3300
row += 1

	

con = sqlite3.connect(ifile)
cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding

cur.execute("SELECT tech FROM technologies")
for val in cur :
	tech.add(val[0])
	
cur.execute("SELECT t_periods FROM time_periods")
for val in cur :
	val = str(val[0])
	period.add(val)

for x in tech :
	for y in period :
		cur.execute("SELECT sum(vflow_out) FROM Output_VFlow_Out WHERE t_periods is '"+y+"' and tech is '"+x+"'")
		z = cur.fetchone()
		#activity.append((z[0]))
		if z[0] is not None :
			sheet.write(row, 1, int(y), easyxf('alignment: vertical centre, horizontal centre;'))
			sheet.write(row, 2, float(z[0]), easyxf('alignment: vertical centre, horizontal centre;'))
			count +=1
			row +=1
			flag = 1
	if flag :
		sheet.write_merge(row-count, row-1, 0, 0, x, easyxf('alignment: vertical centre, horizontal centre;'))
		flag = 0
		count = 0

#print activity
cur.close()
con.close()

book.save("Test.xls")