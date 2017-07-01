import sqlite3
import os
import sys
import pandas as pd



class DatabaseUtil(object):
	def __init__(self, databasePath, scenario=None):
		self.database = os.path.abspath(databasePath)
		self.scenario = scenario
		if (not os.path.exists(self.database)):
			raise ValueError("The database file path doesn't exist")
			
		try:
			self.con = sqlite3.connect(self.database)
		except:
			raise ValueError("Couldn't connect to the database")

		self.cur = self.con.cursor()
		self.con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding

	def close(self):
		self.cur.close()
		self.con.close()


	def getTimePeridosForFlags(self, flags=[]):
		query = ''
		if (flags is None) or (not flags):
			query = "SELECT t_periods FROM time_periods"
		else:
			flag = flags[0]
			query = "SELECT t_periods FROM time_periods WHERE flag is '"+flag+"'"
			for i in range(1, len(flags)):
				query += " OR flag is '"+flags[i]+"'"

		self.cur.execute(query)
		result = set()
		for row in self.cur:
			result.add(int(row[0]))

		return result

	def getTechnologiesForFlags(self, flags=[]):
		query = ''
		if (flags is None) or (not flags):
			query = "SELECT tech FROM technologies"
		else:
			flag = flags[0]
			query = "SELECT tech FROM technologies WHERE flag='"+flag+"'"
			for i in range(1, len(flags)):
				query += " OR flag='"+flags[i]+"'"

		result = set()
		for row in self.cur.execute(query):
			result.add(row[0])

		return result

	def getCommoditiesForFlags(self, flags=[]):
		query = ''
		if (flags is None) or (not flags):
			query = "SELECT comm_name FROM commodities"
		else:
			flag = flags[0]
			query = "SELECT comm_name FROM commodities WHERE flag is '"+flag+"'"
			for i in range(1, len(flags)):
				query += " OR flag is '"+flags[i]+"'"

		result = set()
		for row in self.cur.execute(query):
			result.add(row[0])

		return result

	# comm_type can be 'input' or 'output'
	def getCommoditiesByTechnology(self, comm_type='input'):
		query = ''
		if (comm_type == 'input'):
			query = 'SELECT DISTINCT input_comm, tech FROM Efficiency'
		elif (comm_type == 'output'):
			query = 'SELECT DISTINCT tech, output_comm FROM Efficiency'
		else:
			raise ValueError('Invalid commodity comm_type: can only be input or output')

		result = set()
		for row in self.cur.execute(query):
			result.add((row[0], row[1]))

		return result

	def getCapacityForTechAndPeriod(self, tech = None, period = None):
		if self.scenario is None or self.scenario == '':
			raise ValueError('For Output related queries, please set a scenario first')

		columns = []
		if tech is None:
			columns.append('tech')
		if period is None:
			columns.append('t_periods')
		columns.append('capacity')
		query = "SELECT "+columns[0]

		for col in columns[1:]:
			query += ", " + col

		query += " FROM Output_CapacityByPeriodAndTech WHERE scenario == '"+self.scenario+"'"
		if not tech is None:
			query += " AND tech is '"+tech+"'"
		if not period is None:
			query += " AND t_periods == '"+str(period)+"'"

		self.cur.execute(query)
		result = pd.DataFrame(self.cur.fetchall(), columns=columns)
		if (len(result) == 1 and len(columns) == 1):
			return result.iloc[0,0]
		else:
			return result

	def getOutputFlowForPeriod(self, period, comm_type='input', commodity=None):
		if self.scenario is None or self.scenario == '':
			raise ValueError('For Output related queries, please set a scenario first')
		columns = []
		table = ''
		col = ''
		if (comm_type =='input'):
			table = 'Output_VFlow_In'
			if (commodity is None):
				columns.append('input_comm')
			col = 'vflow_in'
		columns.append('tech')
		if (comm_type== 'output'):
			table = 'Output_VFlow_Out'
			if (commodity is None):
				columns.append('output_comm')
			col = 'vflow_out'
		columns.append('SUM('+col+') AS flow')

		query = "SELECT "
		for c in columns:
			query += c+", "
		query += 'SUM('+col+") AS flow FROM "+table+" WHERE scenario=='"+self.scenario+"'"
		query += " AND t_periods =='"+str(period)+"'"

		query2 = " GROUP BY tech"
		if (not commodity is None):
			query += comm_type+"_comm is '"+commodity+"'"
			if (comm_type == 'output'):
				query += " AND input_comm != 'ethos'"
		else:
			query2 += ", "+comm_type+'_comm'
		
		query += query2
		columns.append('flow')
		self.cur.execute(query)
		result = pd.DataFrame(self.cur.fetchall(), columns=columns)
		return result

	def getEmissionsActivityForPeriod(self, period):
		if self.scenario is None or self.scenario == '':
			raise ValueError('For Output related queries, please set a scenario first')
		query = "SELECT E.emis_comm, E.tech, SUM(E.emis_act*O.vflow_out) FROM EmissionActivity E, Output_VFlow_Out O " + \
		"WHERE E.input_comm == O.input_comm AND E.tech == O.tech AND E.vintage  == O.vintage AND E.output_comm == O.output_comm AND O.scenario == '"+ self.scenario +"' " + \
		"and O.t_periods == '"+str(period)+"' GROUP BY E.tech, E.emis_comm"
		self.cur.execute(query)
		result = pd.DataFrame(self.cur.fetchall(), columns=['emis_comm', 'tech', 'emis_activity'])
		return result

	
		