import sqlite3
import os
import sys
import getopt
import re

def send_query(inp_f, query_string):
	db_result = []
	try:
		con = sqlite3.connect(inp_f)
		cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
		con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding

		print(inp_f)
		cur.execute(query_string)
		
		for row in cur:
			db_result.append(row)
		
		cur.close()
		con.close()
		return "Query Result: %s" % "".join(db_result)

	except sqlite3.Error as e:
		print("Error in Query %s" % e.args[0])
		return "Query Result: Error in Query %s" % e.args[0]
		
		
def help_user():
	print('''Use as:
	python db_query.py -i (or --input) <input database name>
	| -q (or --query) <sqlite query>
	| -h (or --help) ''')

def get_flags(inputs):

	inp_file = None
	query_string = None
	
	if inputs is None:
		raise TypeError("no arguments found")
		
	for opt, arg in inputs.items():
	    
		print("%s == %s" %(opt, arg))
	    
		if opt in ("-i", "--input"):
			inp_file = arg
		elif opt in ("-q", "--query"):
			query_string = arg
		elif opt in ("-h", "--help") :
			help_user()                          
			sys.exit(2)
		
	if inp_file is None:
		raise Exception("Input file not specified")
	
	file_ty = re.search(r"(\w+)\.(\w+)\b", inp_file) # Extract the input filename and extension
	
	if not file_ty :
		raise "The file type %s is not recognized. Please specify a database file." % inp_f
		
	elif file_ty.group(2) not in ("db", "sqlite", "sqlite3", "sqlitedb") :
		raise "The file type %s is not recognized. Please specify a database file." % inp_f
	
	if query_string is None:
		print("No query specified.")
		return None
	
	return send_query(inp_file, query_string)
	
if __name__ == "__main__":
	try:
		argv = sys.argv[1:]
		opts, args = getopt.getopt(argv, "hi:q:", ["help", "input=", "query="])
		
		print(opts)
		
 	except getopt.GetoptError:          
 		help_user()                          
 		sys.exit(2)
	
	print(get_flags( dict(opts) ))