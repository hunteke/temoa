"""
    TEMOA (Tools for Energy Model Optimization and Analysis) 
    Copyright (C) 2010 TEMOA Developer Team 

    This file is part of TEMOA.
    TEMOA is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    TEMOA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with TEMOA.  If not, see <http://www.gnu.org/licenses/>.
"""


#!/usr/bin/env python
#!/home/kevin/ram/coopr/bin/python

# This is crap code.  It is not documented because it's only in the
# repository as a temporary measure, and I do *not* want to encourage
# anyone to rely on this code for anything even remotely mission critical.

import sys
import re

def parse_elc_output ( output ):
	data = {'xc':{}, 'xu':{} }

	i = 0
	num_lines = len(output)
	while (i < num_lines):
		line = output[i]
		line = line.strip()
		tokens = re.split( '[\[\]]', line )

		if 'xc' == tokens[0]:
			indices = re.split( ',', tokens[1] )
			tech = indices[0]
			iper = int(indices[1])

			i += 2
			line = output[ i ].strip()
			value = float(line.split( ': ' )[1])
			if tech not in data['xc']:
				data['xc'].update({tech : {} })

			data['xc'][tech].update({int(iper) : value })

		elif 'xu' == tokens[0]:
			indices = re.split( ',', tokens[1] )
			tech = indices[0]
			iper = int(indices[1])
			per  = int(indices[2])

			i += 2
			line = output[ i ].strip()
			value = float(line.split( ': ')[1] )
			if tech not in data['xu']:
				data['xu'].update({ tech : {} })
			if iper not in data['xu'][tech]:
				data['xu'][tech].update({ iper : {} })

			data['xu'][tech][iper].update({ per : value })

		i += 1

	return data

def graph_data ( data ):
	import numpy as NP
	import matplotlib as M
	from matplotlib import pyplot as P
	

	#x = [ i for i in data['xu']['gt_p'] ]
	x = range(2000,2100,10) # flat out kludge.
	y_xc = []
	y_xu = []

#	for tech in data['xc']:
#		y_row = []
#		for i in x:
#			value = 0
#			if i in data['xc'][tech]:
#				value = data['xc'][tech][i]
#			y_row.append( value )
#		y_xc.append( y_row )

	legend = []
	for tech in data['xu']:
		y_row = []
		legend.append( tech )
		# print tech,
		for i in x:
			value = 0
			for iper in data['xu'][tech]:
				if i in data['xu'][tech][iper]:
					value += data['xu'][tech][iper][i]
			y_row.append( value )
		y_xu.append( y_row )
		# print y_row

	colors = [
		'#000000',
		'#330000',
		'#003300',
		'#000033',
		'#660000',
		'#006600',
		'#000066',
		'#990000',
		'#009900',
		'#000099',
		'#CC0000',
		'#00CC00',
		'#0000CC',
		'#FF0000',
		'#00FF00',
		'#0000FF',
	]
	#return y_xu

#			for iper in data['xu'][tech]:
#				if i in data['xu'][tech][iper]:
#					year_util += data['xu'][tech][iper][i]

	#	y_xu.append(year_util)

#	print y_xc
	#for i in range(len(y_xc)):
	#	y_xu[i] += y_xc[i]
	x = NP.array(x)
	#y_data = NP.row_stack((y_xc))
	#y_stacked = NP.cumsum(y_xc, axis=0)
	y_xu = tuple([i for i in y_xu])
	y_data = NP.row_stack( y_xu )
	y_stacked = NP.cumsum(y_data, axis=0)
	fig = P.figure()
	#ax = fig.add_subplot(111)
	xu_axis = fig.add_axes([.1,.1,.8,.8], xlabel='Time Period (yrs)', ylabel='Utilization (GW*yrs)')
#	line1 = M.lines.Line2D(x, y_xu[0], label=legend[0], color=colors[0] );

	lines = []
	for line in range(len(y_xu) -1):
		for point in range(len(y_xu[line])):
			y_xu[line+1][point] += y_xu[line][point]
		lines.append( M.lines.Line2D(x, y_xu[line], label=legend[line], color=colors[line] ) )
	lines.append( M.lines.Line2D(x, y_xu[line], label=legend[line], color=colors[line] ) )

	#print line1.get_data(), line2.get_data()
	#xu_axis.add_line( line1 )
	#xu_axis.add_line( line2 )
	#xu_axis.legend()
	#xu_axis.set_xbound(lower=2000, upper=2100)
	#xu_axis.set_ybound(lower=0, upper=25 )
	last = 0
	for i in range(len(lines)):
		xu_axis.fill_between(x, last, y_stacked[i], facecolor=lines[i].get_color(), alpha=0.7)
		last = y_stacked[i]
		xu_axis.add_line(lines[i])

	xu_axis.legend()
	
	P.show()
	return


#	print y_xc
#	last = 0
#	for i in y_xc:
#		ax1.fill_between(x, last, i, facecolor='#CC0000', alpha=0.7 )
#		old = i
	# print y_xu
	last = 0
	c = 0
	lines  = []
	legend = []
	for i in y_stacked:
		c += 1
		c %= len(colors)
		P.fill_between(x, last, i, facecolor=colors[c], alpha=0.7, label='Line: %d' % c )
		#PLT.line
		#lines.append( i )
		#legend.append( "Line: %d" % c )
		last = i

	#PLT.figlegend()
	P.show()


if '__main__' == __name__:
	output = sys.stdin.readlines()
	data = parse_elc_output( output )
	graph_data( data )
#	import yaml

