import sqlite3
import sys
import re

def query_table (t_properties, f):
    t_type = t_properties[0]  #table type (set or param)
    t_name = t_properties[1]  #table name
    t_flag = t_properties[3]  #table flag, if any
    t_index = t_properties[4] #table column index after which '#' should be specified
    if type(t_flag) is list:  #tech production table has a list for flags; this is currently hard-wired
        db_query = "SELECT * FROM " + t_name + " WHERE flag=='p' OR flag=='pb' OR flag=='ps'"
        dat_table_name = t_properties[2]
        if t_type == "set":
            f.write("set " + dat_table_name + " := \n")
        else:
            f.write("param " + dat_table_name + " := \n")
    elif t_flag != '':    #check to see if flag is empty, if not use it to make table
        db_query = "SELECT * FROM " + t_name + " WHERE flag=='" + t_flag + "'"
        dat_table_name = t_properties[2]
        if t_type == "set":
            f.write("set " + dat_table_name + " := \n")
        else:
            f.write("param " + dat_table_name + " := \n")
    else:    #Only other possible case is no flag
        db_query = "SELECT * FROM " + t_name
        if t_type == "set":
            f.write("set " + t_name + " := \n")
        else:
            f.write("param " + t_name + " := \n")
    cur.execute(db_query)
    if t_index == 0:    #make sure that units and descriptions are commented out in DAT file
        for line in cur:
            str_row = str(line[0]) + "\n"
            f.write(str_row)
            print str_row
    else:
        for line in cur:
            before_comments = line[:t_index+1]    
            before_comments = re.sub('[(]', '', str(before_comments))
            before_comments = re.sub('[\',)]', '    ', str(before_comments))
            after_comments = line[t_index+2:]
            after_comments = re.sub('[(]', '', str(after_comments))
            after_comments = re.sub('[\',)]', '    ', str(after_comments))            
            str_row = before_comments + "# " + after_comments + "\n"
            f.write(str_row)
            print str_row                
    f.write(';\n\n')

#[set or param, table_name, DAT fieldname, flag (if any), index (where to insert '#')
table_list =[['set','time_periods','time_exist','e',0], \
             ['set','time_periods','time_future','f',0], \
             ['set','time_season','','',0],    \
             ['set','time_of_day','','',0],    \
             ['set','technologies','tech_resource','r',0],  \
             ['set','technologies','tech_production',['p','pb','ps'],0], \
             ['set','technologies','tech_baseload','pb',0], \
             ['set','technologies','tech_storage','ps',0],  \
             ['set','commodities','commodity_physical','p',0],   \
             ['set','commodities','commodity_emissions','e',0],   \
             ['set','commodities','commodity_demand','d',0],   \
             ['param','SegFrac','','',2],        \
             ['param','DemandSpecificDistribution','','',3],  \
             ['param','CapacityToActivity','','',1],          \
             ['param','GlobalDiscountRate','','',0],          \
             ['param','EmissionActivity','','',5],            \
             ['param','Demand','','',2],                      \
             ['param','TechOutputSplit','','',2],             \
             ['param','MinCapacity','','',2],                 \
             ['param','MaxCapacity','','',2],                 \
             ['param','LifetimeTech','','',1],                \
             ['param','LifetimeProcess','','',2],             \
             ['param','LifetimeLoanTech','','',1],            \
             ['param','CapacityFactorTech','','',3],          \
             ['param','CapacityFactorProcess','','',4],       \
             ['param','Efficiency','','',4],                  \
             ['param','ExistingCapacity','','',2],            \
             ['param','CostInvest','','',2],                  \
             ['param','CostFixed','','',3],                   \
             ['param','CostVariable','','',3]]


             
#create a file to write output
f = open('temoa_input.dat', 'w')
f.write('data ;\n\n')
#connect to the database
con = sqlite3.connect('temoa_utopia_w_output_tables.db')
cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding

for table in table_list:
    query_table(table, f)


f.close()   
cur.close()
con.close()
