from __future__ import division
import time
start_time = time.time()
from joblib import Parallel, delayed
import multiprocessing
import sys
import os
from shutil import copyfile
import sqlite3
from numpy import array
from IPython import embed as IP
from SALib.analyze import morris
from SALib.sample.morris import sample
from SALib.util import read_param_file, compute_groups_matrix
import numpy as np

def evaluate(param_names, param_values,k): 

	m=len(param_values)
	for j in range(0,m):
		Newdbpath=os.getcwd()+'/data_files/Method_of_Morris'+str(k)+'.db'
		con=sqlite3.connect(Newdbpath)
		cur = con.cursor()
		filter1=param_names[j][1]
		filter2=param_names[j][2]
		table=param_names[j][0]
		cursor = con.execute("SELECT * FROM "+"'"+table+"'")
		col_names = list(map(lambda x: x[0], cursor.description))
		if len(param_names[j])==4:
			update_var=param_names[j][3]
			text="UPDATE "+"'"+table+"' SET "+"'"+update_var+"'=? WHERE "+"'"+col_names[0]+"'=? and "+"'"+col_names[1]+"'=?"
			text=text.replace("'","")
			con.execute(text, (param_values[j],filter1,filter2))
			con.commit()
		elif len(param_names[j])==5:
			filter3=param_names[j][3]
			update_var=param_names[j][4]
			text="UPDATE "+"'"+table+"' SET "+"'"+update_var+"'=? WHERE "+"'"+col_names[0]+"'=? and "+"'"+col_names[1]+"'=? and "+"'"+col_names[2]+"'=?"
			text=text.replace("'","")
			con.execute(text, (param_values[j],filter1,filter2,filter3))
			con.commit()
		else:
			filter3=param_names[j][3]
			filter4=param_names[j][4]
			update_var=param_names[j][5]
			text="UPDATE "+"'"+table+"' SET "+"'"+update_var+"'=? WHERE "+"'"+col_names[0]+"'=? and "+"'"+col_names[1]+"'=? and "+"'"+col_names[2]+"'=? and "+"'"+col_names[3]+"'=?"
			text=text.replace("'","")
			con.execute(text, (param_values[j],filter1,filter2,filter3,filter4))
			con.commit()
		con.close()
	NewConfigfilePath=os.getcwd()+'/temoa_model/config_sample'+str(k)
	copyfile(os.getcwd()+'/temoa_model/config_sample',NewConfigfilePath)
	with open(os.getcwd()+'/temoa_model/config_sample', 'r') as file:
		data = file.readlines()
	data[10]='--input=data_files/Method_of_Morris'+str(k)+'.db'  #10th line in the config file referring to input database
	data[14]='--output=data_files/Method_of_Morris'+str(k)+'.db' #14th line in the config file referring to output database
	with open(NewConfigfilePath, 'w') as file:
		file.writelines(data)
	os.system('python temoa_model/ --config=temoa_model/config_sample'+str(k))

	Newdbpath=os.getcwd()+'/data_files/Method_of_Morris'+str(k)+'.db'
	con=sqlite3.connect(Newdbpath)
	cur = con.cursor()
	cur.execute("SELECT * FROM Output_Objective")
	output_query = cur.fetchall()
	for row in output_query:
		Y_OF=row[-1]
	cur.execute("SELECT emissions_comm, SUM(emissions) FROM Output_Emissions WHERE emissions_comm='co2'")
	output_query = cur.fetchall()
	for row in output_query:
		Y_CumulativeCO2=row[-1]
	Morris_Objectives=[]
	Morris_Objectives.append(Y_OF)
	Morris_Objectives.append(Y_CumulativeCO2)
	con.close()
	return Morris_Objectives


perturbation_coefficient=0.2 #minus plus 10% of the baseline values
f= open(os.getcwd()+"/Method_of_Morris.txt","w+")
f.close()
param_names={}
con=sqlite3.connect('data_files/Method_of_Morris.db')
cur = con.cursor()
cur.execute("SELECT * FROM CostVariable WHERE MMAnalysis is not NULL")
output_query = cur.fetchall()
g1=len(output_query)
for i in range(0,len(output_query)):
	param_names[i]=['CostVariable',output_query[i][0],output_query[i][1],output_query[i][2],'cost_variable']
	with open(os.getcwd()+'/Method_of_Morris.txt','a') as file:
		file.write('x'+str(i))
		file.write(' ')
		file.write(str(output_query[i][3]*0.9))
		file.write(' ')
		file.write(str(output_query[i][3]*1.1))
		file.write(' ')
		file.write(output_query[i][-1])
		file.write("\n")
cur.execute("SELECT * FROM CostInvest WHERE MMAnalysis is not NULL")
output_query = cur.fetchall()
g2=len(output_query)
for i in range(0,len(output_query)):
	param_names[i+g1]=['CostInvest',output_query[i][0],output_query[i][1],'cost_invest']
	with open(os.getcwd()+'/Method_of_Morris.txt','a') as file:
		file.write('x'+str(i+g1))
		file.write(' ')
		file.write(str(output_query[i][2]*0.9))
		file.write(' ')
		file.write(str(output_query[i][2]*1.1))
		file.write(' ')
		file.write(output_query[i][-1])
		file.write("\n")
cur.execute("SELECT * FROM Efficiency WHERE MMAnalysis is not NULL")
output_query = cur.fetchall()
g3=len(output_query)
for i in range(0,len(output_query)):
	param_names[i+g1+g2]=['Efficiency',output_query[i][0],output_query[i][1],output_query[i][2],output_query[i][3],'efficiency']
	with open(os.getcwd()+'/Method_of_Morris.txt','a') as file:
		file.write('x'+str(i+g1+g2))
		file.write(' ')
		file.write(str(output_query[i][4]*0.9))
		file.write(' ')
		file.write(str(output_query[i][4]*1.1))
		file.write(' ')
		file.write(output_query[i][-1])
		file.write("\n")

problem = read_param_file(os.getcwd()+'/Method_of_Morris.txt')
param_values = sample(problem, N=3, num_levels=4, grid_jump=2, \
                      optimal_trajectories=False, local_optimization=False)
n=len(param_values)
for k in range(0,n):
	Newdbpath=os.getcwd()+'/data_files/Method_of_Morris'+str(k)+'.db'
	copyfile(os.getcwd()+'/data_files/Method_of_Morris.db',Newdbpath)
num_cores = multiprocessing.cpu_count()
Morris_Objectives = Parallel(n_jobs=num_cores)(delayed(evaluate)(param_names, param_values[i,:],i) for i in range(0,n))
Morris_Objectives=array(Morris_Objectives)
Si_OF = morris.analyze(problem, param_values, Morris_Objectives[:,0], conf_level=0.95, 
                    print_to_console=False,
                    num_levels=4, grid_jump=2, num_resamples=1000)

Si_CumulativeCO2 = morris.analyze(problem, param_values, Morris_Objectives[:,1], conf_level=0.95, 
                    print_to_console=False,
                    num_levels=4, grid_jump=2, num_resamples=1000)
num_vars = problem['num_vars']
groups, unique_group_names = compute_groups_matrix(problem['groups'], num_vars)
number_of_groups = len(unique_group_names)
print("{0:<30} {1:>10} {2:>10} {3:>15} {4:>10}".format(
	"Parameter",
	"Mu_Star",
	"Mu",
	"Mu_Star_Conf",
	"Sigma")
                  )
for j in list(range(number_of_groups)):
	print("{0:30} {1:10.3f} {2:10.3f} {3:15.3f} {4:10.3f}".format(
	Si_OF['names'][j],
	Si_OF['mu_star'][j],
	Si_OF['mu'][j],
	Si_OF['mu_star_conf'][j],
	Si_OF['sigma'][j]))
import csv
line1=Si_OF['mu_star']
line2=Si_OF['mu_star_conf']
line3=Si_CumulativeCO2['mu_star']
line4=Si_CumulativeCO2['mu_star_conf']
with open('MMResults.csv', 'w') as f:
	writer = csv.writer(f, delimiter=',')
	writer.writerow(unique_group_names)
	writer.writerow('Objective Function') 
	writer.writerow(line1)
	writer.writerow(line2)
	writer.writerow("Cumulative CO2 Emissions") 
	writer.writerow(line3)
	writer.writerow(line4)

f.close
print("--- %s seconds ---" % (time.time() - start_time))

