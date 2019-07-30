from __future__ import division
import sys
from IPython import embed as IP
import time
start_time = time.time()
from joblib import Parallel, delayed
import multiprocessing
from shutil import copyfile
import sqlite3
import os
from numpy import array

import csv
from pyDOE import *


from SALib.analyze import morris
from SALib.sample.morris import sample
from SALib.util import read_param_file, compute_groups_matrix
import numpy as np

def evaluate(param_values,k):
	param_names = {     #the first element is the name of the table, followed by fisrt, second ... filters. The name of the column which is to change comes at the end
	0:['CostInvest','E_SOLPVCEN_N',2020,'cost_invest'],
	1:['CostInvest','E_SOLPVCEN_N',2025,'cost_invest'],
	2:['CostInvest','E_SOLPVCEN_N',2030,'cost_invest'],
	3:['CostInvest','E_SOLPVCEN_N',2035,'cost_invest'],
	4:['CostInvest','E_SOLPVCEN_N',2040,'cost_invest'],
	5:['CostInvest','E_SOLPVENDUSE_N',2020,'cost_invest'],
	6:['CostInvest','E_SOLPVENDUSE_N',2025,'cost_invest'],
	7:['CostInvest','E_SOLPVENDUSE_N',2030,'cost_invest'],
	8:['CostInvest','E_SOLPVENDUSE_N',2035,'cost_invest'],
	9:['CostInvest','E_SOLPVENDUSE_N',2040,'cost_invest'],
	10:['CostVariable',2015,'IMPELCNGA',2015,'cost_variable'],
	11:['CostVariable',2020,'IMPELCNGA',2015,'cost_variable'],
	12:['CostVariable',2025,'IMPELCNGA',2015,'cost_variable'],
	13:['CostVariable',2030,'IMPELCNGA',2015,'cost_variable'],
	14:['CostVariable',2035,'IMPELCNGA',2015,'cost_variable'],
	15:['CostVariable',2040,'IMPELCNGA',2015,'cost_variable'],
	16:['CostVariable',2015,'IMPTRNCNG',2015,'cost_variable'],
	17:['CostVariable',2020,'IMPTRNCNG',2015,'cost_variable'],
	18:['CostVariable',2025,'IMPTRNCNG',2015,'cost_variable'],
	19:['CostVariable',2030,'IMPTRNCNG',2015,'cost_variable'],
	20:['CostVariable',2035,'IMPTRNCNG',2015,'cost_variable'],
	21:['CostVariable',2040,'IMPTRNCNG',2015,'cost_variable'],
	22:['CostVariable',2015,'IMPRESNGA',2015,'cost_variable'],
	23:['CostVariable',2020,'IMPRESNGA',2015,'cost_variable'],
	24:['CostVariable',2025,'IMPRESNGA',2015,'cost_variable'],
	25:['CostVariable',2030,'IMPRESNGA',2015,'cost_variable'],
	26:['CostVariable',2035,'IMPRESNGA',2015,'cost_variable'],
	27:['CostVariable',2040,'IMPRESNGA',2015,'cost_variable'],
	28:['CostVariable',2015,'IMPCOMNGA',2015,'cost_variable'],
	29:['CostVariable',2020,'IMPCOMNGA',2015,'cost_variable'],
	30:['CostVariable',2025,'IMPCOMNGA',2015,'cost_variable'],
	31:['CostVariable',2030,'IMPCOMNGA',2015,'cost_variable'],
	32:['CostVariable',2035,'IMPCOMNGA',2015,'cost_variable'],
	33:['CostVariable',2040,'IMPCOMNGA',2015,'cost_variable'],
	34:['CostInvest','E_WNDCL4_N',2020,'cost_invest'],
	35:['CostInvest','E_WNDCL4_N',2025,'cost_invest'],
	36:['CostInvest','E_WNDCL4_N',2030,'cost_invest'],
	37:['CostInvest','E_WNDCL4_N',2035,'cost_invest'],
	38:['CostInvest','E_WNDCL4_N',2040,'cost_invest'],
	39:['CostInvest','E_WNDCL5_N',2020,'cost_invest'],
	40:['CostInvest','E_WNDCL5_N',2025,'cost_invest'],
	41:['CostInvest','E_WNDCL5_N',2030,'cost_invest'],
	42:['CostInvest','E_WNDCL5_N',2035,'cost_invest'],
	43:['CostInvest','E_WNDCL5_N',2040,'cost_invest'],
	44:['CostInvest','E_WNDCL6_N',2020,'cost_invest'],
	45:['CostInvest','E_WNDCL6_N',2025,'cost_invest'],
	46:['CostInvest','E_WNDCL6_N',2030,'cost_invest'],
	47:['CostInvest','E_WNDCL6_N',2035,'cost_invest'],
	48:['CostInvest','E_WNDCL6_N',2040,'cost_invest'],
	49:['CostVariable',2015,'IMPELCCOAB',2015,'cost_variable'],
	50:['CostVariable',2020,'IMPELCCOAB',2015,'cost_variable'],
	51:['CostVariable',2025,'IMPELCCOAB',2015,'cost_variable'],
	52:['CostVariable',2030,'IMPELCCOAB',2015,'cost_variable'],
	53:['CostVariable',2035,'IMPELCCOAB',2015,'cost_variable'],
	54:['CostVariable',2040,'IMPELCCOAB',2015,'cost_variable'],
	55:['CostVariable',2015,'IMPELCCOAS',2015,'cost_variable'],
	56:['CostVariable',2020,'IMPELCCOAS',2015,'cost_variable'],
	57:['CostVariable',2025,'IMPELCCOAS',2015,'cost_variable'],
	58:['CostVariable',2030,'IMPELCCOAS',2015,'cost_variable'],
	59:['CostVariable',2035,'IMPELCCOAS',2015,'cost_variable'],
	60:['CostVariable',2040,'IMPELCCOAS',2015,'cost_variable'],
	61:['CostVariable',2015,'IMPELCCOAL',2015,'cost_variable'],
	62:['CostVariable',2020,'IMPELCCOAL',2015,'cost_variable'],
	63:['CostVariable',2025,'IMPELCCOAL',2015,'cost_variable'],
	64:['CostVariable',2030,'IMPELCCOAL',2015,'cost_variable'],
	65:['CostVariable',2035,'IMPELCCOAL',2015,'cost_variable'],
	66:['CostVariable',2040,'IMPELCCOAL',2015,'cost_variable'],
	67:['CostInvest','E_NGACC_N',2020,'cost_invest'],
	68:['CostInvest','E_NGACC_N',2025,'cost_invest'],
	69:['CostInvest','E_NGACC_N',2030,'cost_invest'],
	70:['CostInvest','E_NGACC_N',2035,'cost_invest'],
	71:['CostInvest','E_NGACC_N',2040,'cost_invest'],
	72:['CostInvest','E_NGAACC_N',2020,'cost_invest'],
	73:['CostInvest','E_NGAACC_N',2025,'cost_invest'],
	74:['CostInvest','E_NGAACC_N',2030,'cost_invest'],
	75:['CostInvest','E_NGAACC_N',2035,'cost_invest'],
	76:['CostInvest','E_NGAACC_N',2040,'cost_invest'],
	77:['CostInvest','T_LDV_CE85X_N',2020,'cost_invest'],
	78:['CostInvest','T_LDV_CE85X_N',2025,'cost_invest'],
	79:['CostInvest','T_LDV_CE85X_N',2030,'cost_invest'],
	80:['CostInvest','T_LDV_CE85X_N',2035,'cost_invest'],
	81:['CostInvest','T_LDV_CE85X_N',2040,'cost_invest'],
	82:['CostInvest','T_LDV_FE85X_N',2020,'cost_invest'],
	83:['CostInvest','T_LDV_FE85X_N',2025,'cost_invest'],
	84:['CostInvest','T_LDV_FE85X_N',2030,'cost_invest'],
	85:['CostInvest','T_LDV_FE85X_N',2035,'cost_invest'],
	86:['CostInvest','T_LDV_FE85X_N',2040,'cost_invest'],
	87:['CostInvest','T_LDV_SSE85X_N',2020,'cost_invest'],
	88:['CostInvest','T_LDV_SSE85X_N',2025,'cost_invest'],
	89:['CostInvest','T_LDV_SSE85X_N',2030,'cost_invest'],
	90:['CostInvest','T_LDV_SSE85X_N',2035,'cost_invest'],
	91:['CostInvest','T_LDV_SSE85X_N',2040,'cost_invest'],
	92:['CostInvest','T_LDV_LSE85X_N',2020,'cost_invest'],
	93:['CostInvest','T_LDV_LSE85X_N',2025,'cost_invest'],
	94:['CostInvest','T_LDV_LSE85X_N',2030,'cost_invest'],
	95:['CostInvest','T_LDV_LSE85X_N',2035,'cost_invest'],
	96:['CostInvest','T_LDV_LSE85X_N',2040,'cost_invest'],
	97:['CostInvest','T_LDV_MVE85X_N',2020,'cost_invest'],
	98:['CostInvest','T_LDV_MVE85X_N',2025,'cost_invest'],
	99:['CostInvest','T_LDV_MVE85X_N',2030,'cost_invest'],
	100:['CostInvest','T_LDV_MVE85X_N',2035,'cost_invest'],
	101:['CostInvest','T_LDV_MVE85X_N',2040,'cost_invest'],
	102:['CostInvest','T_LDV_PE85X_N',2020,'cost_invest'],
	103:['CostInvest','T_LDV_PE85X_N',2025,'cost_invest'],
	104:['CostInvest','T_LDV_PE85X_N',2030,'cost_invest'],
	105:['CostInvest','T_LDV_PE85X_N',2035,'cost_invest'],
	106:['CostInvest','T_LDV_PE85X_N',2040,'cost_invest'],
	107:['CostInvest','T_LDV_MCE10_N',2015,'cost_invest'],
	108:['CostInvest','T_LDV_MCE10_N',2020,'cost_invest'],
	109:['CostInvest','T_LDV_MCE10_N',2025,'cost_invest'],
	110:['CostInvest','T_LDV_MCE10_N',2030,'cost_invest'],
	111:['CostInvest','T_LDV_MCE10_N',2035,'cost_invest'],
	112:['CostInvest','T_LDV_MCE10_N',2040,'cost_invest'],
	113:['CostInvest','T_LDV_CE10_N',2015,'cost_invest'],
	114:['CostInvest','T_LDV_CE10_N',2020,'cost_invest'],
	115:['CostInvest','T_LDV_CE10_N',2025,'cost_invest'],
	116:['CostInvest','T_LDV_CE10_N',2030,'cost_invest'],
	117:['CostInvest','T_LDV_CE10_N',2035,'cost_invest'],
	118:['CostInvest','T_LDV_CE10_N',2040,'cost_invest'],
	119:['CostInvest','T_LDV_FE10_N',2015,'cost_invest'],
	120:['CostInvest','T_LDV_FE10_N',2020,'cost_invest'],
	121:['CostInvest','T_LDV_FE10_N',2025,'cost_invest'],
	122:['CostInvest','T_LDV_FE10_N',2030,'cost_invest'],
	123:['CostInvest','T_LDV_FE10_N',2035,'cost_invest'],
	124:['CostInvest','T_LDV_FE10_N',2040,'cost_invest'],
	125:['CostInvest','T_LDV_SSE10_N',2015,'cost_invest'],
	126:['CostInvest','T_LDV_SSE10_N',2020,'cost_invest'],
	127:['CostInvest','T_LDV_SSE10_N',2025,'cost_invest'],
	128:['CostInvest','T_LDV_SSE10_N',2030,'cost_invest'],
	129:['CostInvest','T_LDV_SSE10_N',2035,'cost_invest'],
	130:['CostInvest','T_LDV_SSE10_N',2040,'cost_invest'],
	131:['CostInvest','T_LDV_LSE10_N',2015,'cost_invest'],
	132:['CostInvest','T_LDV_LSE10_N',2020,'cost_invest'],
	133:['CostInvest','T_LDV_LSE10_N',2025,'cost_invest'],
	134:['CostInvest','T_LDV_LSE10_N',2030,'cost_invest'],
	135:['CostInvest','T_LDV_LSE10_N',2035,'cost_invest'],
	136:['CostInvest','T_LDV_LSE10_N',2040,'cost_invest'],
	137:['CostInvest','T_LDV_MVE10_N',2020,'cost_invest'],
	138:['CostInvest','T_LDV_MVE10_N',2025,'cost_invest'],
	139:['CostInvest','T_LDV_MVE10_N',2030,'cost_invest'],
	140:['CostInvest','T_LDV_MVE10_N',2035,'cost_invest'],
	141:['CostInvest','T_LDV_MVE10_N',2040,'cost_invest'],
	142:['CostInvest','T_LDV_PE10_N',2020,'cost_invest'],
	143:['CostInvest','T_LDV_PE10_N',2025,'cost_invest'],
	144:['CostInvest','T_LDV_PE10_N',2030,'cost_invest'],
	145:['CostInvest','T_LDV_PE10_N',2035,'cost_invest'],
	146:['CostInvest','T_LDV_PE10_N',2040,'cost_invest'],
	147:['CostInvest','T_HDV_BE10_N',2020,'cost_invest'],
	148:['CostInvest','T_HDV_BE10_N',2025,'cost_invest'],
	149:['CostInvest','T_HDV_BE10_N',2030,'cost_invest'],
	150:['CostInvest','T_HDV_BE10_N',2035,'cost_invest'],
	151:['CostInvest','T_HDV_BE10_N',2040,'cost_invest'],
	152:['CostInvest','T_HDV_BE10_10_N',2020,'cost_invest'],
	153:['CostInvest','T_HDV_BE10_10_N',2025,'cost_invest'],
	154:['CostInvest','T_HDV_BE10_10_N',2030,'cost_invest'],
	155:['CostInvest','T_HDV_BE10_10_N',2035,'cost_invest'],
	156:['CostInvest','T_HDV_BE10_10_N',2040,'cost_invest'],
	157:['CostInvest','T_HDV_TCE10_N',2020,'cost_invest'],
	158:['CostInvest','T_HDV_TCE10_N',2025,'cost_invest'],
	159:['CostInvest','T_HDV_TCE10_N',2030,'cost_invest'],
	160:['CostInvest','T_HDV_TCE10_N',2035,'cost_invest'],
	161:['CostInvest','T_HDV_TCE10_N',2040,'cost_invest'],
	162:['CostInvest','T_HDV_TCE1020_N',2020,'cost_invest'],
	163:['CostInvest','T_HDV_TCE1020_N',2025,'cost_invest'],
	164:['CostInvest','T_HDV_TCE1020_N',2030,'cost_invest'],
	165:['CostInvest','T_HDV_TCE1020_N',2035,'cost_invest'],
	166:['CostInvest','T_HDV_TCE1020_N',2040,'cost_invest'],
	167:['CostInvest','T_HDV_TCE1030_N',2030,'cost_invest'],
	168:['CostInvest','T_HDV_TCE1030_N',2035,'cost_invest'],
	169:['CostInvest','T_HDV_TCE1030_N',2040,'cost_invest'],
	170:['CostInvest','T_HDV_TCE10_20_N',2020,'cost_invest'],
	171:['CostInvest','T_HDV_TCE10_20_N',2025,'cost_invest'],
	172:['CostInvest','T_HDV_TCE10_20_N',2030,'cost_invest'],
	173:['CostInvest','T_HDV_TCE10_20_N',2035,'cost_invest'],
	174:['CostInvest','T_HDV_TCE10_20_N',2040,'cost_invest'],
	175:['CostInvest','T_HDV_TCE1030_20_N',2030,'cost_invest'],
	176:['CostInvest','T_HDV_TCE1030_20_N',2035,'cost_invest'],
	177:['CostInvest','T_HDV_TCE1030_20_N',2040,'cost_invest'],
	178:['CostInvest','T_HDV_TCE85X_N',2015,'cost_invest'],
	179:['CostInvest','T_HDV_TCE85X_N',2020,'cost_invest'],
	180:['CostInvest','T_HDV_TCE85X_N',2025,'cost_invest'],
	181:['CostInvest','T_HDV_TCE85X_N',2030,'cost_invest'],
	182:['CostInvest','T_HDV_TCE85X_N',2035,'cost_invest'],
	183:['CostInvest','T_HDV_TCE85X_N',2040,'cost_invest'],
	184:['CostInvest','T_HDV_TCLPG_N',2015,'cost_invest'],
	185:['CostInvest','T_HDV_TCLPG_N',2020,'cost_invest'],
	186:['CostInvest','T_HDV_TCLPG_N',2025,'cost_invest'],
	187:['CostInvest','T_HDV_TCLPG_N',2030,'cost_invest'],
	188:['CostInvest','T_HDV_TCLPG_N',2035,'cost_invest'],
	189:['CostInvest','T_HDV_TCLPG_N',2040,'cost_invest'],
	190:['CostInvest','T_HDV_THE10_N',2020,'cost_invest'],
	191:['CostInvest','T_HDV_THE10_N',2025,'cost_invest'],
	192:['CostInvest','T_HDV_THE10_N',2030,'cost_invest'],
	193:['CostInvest','T_HDV_THE10_N',2035,'cost_invest'],
	194:['CostInvest','T_HDV_THE10_N',2040,'cost_invest'],
	195:['CostInvest','T_HDV_THE1020_N',2020,'cost_invest'],
	196:['CostInvest','T_HDV_THE1020_N',2025,'cost_invest'],
	197:['CostInvest','T_HDV_THE1020_N',2030,'cost_invest'],
	198:['CostInvest','T_HDV_THE1020_N',2035,'cost_invest'],
	199:['CostInvest','T_HDV_THE1020_N',2040,'cost_invest'],
	200:['CostInvest','T_HDV_THLPG_N',2020,'cost_invest'],
	201:['CostInvest','T_HDV_THLPG_N',2025,'cost_invest'],
	202:['CostInvest','T_HDV_THLPG_N',2030,'cost_invest'],
	203:['CostInvest','T_HDV_THLPG_N',2035,'cost_invest'],
	204:['CostInvest','T_HDV_THLPG_N',2040,'cost_invest'],
	205:['CostVariable',2015,'IMPELCDSL',2015,'cost_variable'],
	206:['CostVariable',2020,'IMPELCDSL',2015,'cost_variable'],
	207:['CostVariable',2025,'IMPELCDSL',2015,'cost_variable'],
	208:['CostVariable',2030,'IMPELCDSL',2015,'cost_variable'],
	209:['CostVariable',2035,'IMPELCDSL',2015,'cost_variable'],
	210:['CostVariable',2040,'IMPELCDSL',2015,'cost_variable'],
	211:['CostVariable',2015,'IMPELCRFL',2015,'cost_variable'],
	212:['CostVariable',2020,'IMPELCRFL',2015,'cost_variable'],
	213:['CostVariable',2025,'IMPELCRFL',2015,'cost_variable'],
	214:['CostVariable',2030,'IMPELCRFL',2015,'cost_variable'],
	215:['CostVariable',2035,'IMPELCRFL',2015,'cost_variable'],
	216:['CostVariable',2040,'IMPELCRFL',2015,'cost_variable'],
	217:['CostVariable',2015,'IMPTRNDSL',2015,'cost_variable'],
	218:['CostVariable',2020,'IMPTRNDSL',2015,'cost_variable'],
	219:['CostVariable',2025,'IMPTRNDSL',2015,'cost_variable'],
	220:['CostVariable',2030,'IMPTRNDSL',2015,'cost_variable'],
	221:['CostVariable',2035,'IMPTRNDSL',2015,'cost_variable'],
	222:['CostVariable',2040,'IMPTRNDSL',2015,'cost_variable'],
	223:['CostVariable',2015,'IMPTRNE85',2015,'cost_variable'],
	224:['CostVariable',2020,'IMPTRNE85',2015,'cost_variable'],
	225:['CostVariable',2025,'IMPTRNE85',2015,'cost_variable'],
	226:['CostVariable',2030,'IMPTRNE85',2015,'cost_variable'],
	227:['CostVariable',2035,'IMPTRNE85',2015,'cost_variable'],
	228:['CostVariable',2040,'IMPTRNE85',2015,'cost_variable'],
	229:['CostVariable',2015,'IMPTRNE10',2015,'cost_variable'],
	230:['CostVariable',2020,'IMPTRNE10',2015,'cost_variable'],
	231:['CostVariable',2025,'IMPTRNE10',2015,'cost_variable'],
	232:['CostVariable',2030,'IMPTRNE10',2015,'cost_variable'],
	233:['CostVariable',2035,'IMPTRNE10',2015,'cost_variable'],
	234:['CostVariable',2040,'IMPTRNE10',2015,'cost_variable'],
	235:['CostVariable',2015,'IMPTRNLPG',2015,'cost_variable'],
	236:['CostVariable',2020,'IMPTRNLPG',2015,'cost_variable'],
	237:['CostVariable',2025,'IMPTRNLPG',2015,'cost_variable'],
	238:['CostVariable',2030,'IMPTRNLPG',2015,'cost_variable'],
	239:['CostVariable',2035,'IMPTRNLPG',2015,'cost_variable'],
	240:['CostVariable',2040,'IMPTRNLPG',2015,'cost_variable'],
	241:['CostVariable',2015,'IMPTRNBIODSL',2015,'cost_variable'],
	242:['CostVariable',2020,'IMPTRNBIODSL',2015,'cost_variable'],
	243:['CostVariable',2025,'IMPTRNBIODSL',2015,'cost_variable'],
	244:['CostVariable',2030,'IMPTRNBIODSL',2015,'cost_variable'],
	245:['CostVariable',2035,'IMPTRNBIODSL',2015,'cost_variable'],
	246:['CostVariable',2040,'IMPTRNBIODSL',2015,'cost_variable'],
	247:['CostVariable',2015,'IMPTRNJTF',2015,'cost_variable'],
	248:['CostVariable',2020,'IMPTRNJTF',2015,'cost_variable'],
	249:['CostVariable',2025,'IMPTRNJTF',2015,'cost_variable'],
	250:['CostVariable',2030,'IMPTRNJTF',2015,'cost_variable'],
	251:['CostVariable',2035,'IMPTRNJTF',2015,'cost_variable'],
	252:['CostVariable',2040,'IMPTRNJTF',2015,'cost_variable'],
	253:['CostVariable',2015,'IMPTRNRFO',2015,'cost_variable'],
	254:['CostVariable',2020,'IMPTRNRFO',2015,'cost_variable'],
	255:['CostVariable',2025,'IMPTRNRFO',2015,'cost_variable'],
	256:['CostVariable',2030,'IMPTRNRFO',2015,'cost_variable'],
	257:['CostVariable',2035,'IMPTRNRFO',2015,'cost_variable'],
	258:['CostVariable',2040,'IMPTRNRFO',2015,'cost_variable'],
	259:['CostVariable',2015,'IMPRESLPG',2015,'cost_variable'],
	260:['CostVariable',2020,'IMPRESLPG',2015,'cost_variable'],
	261:['CostVariable',2025,'IMPRESLPG',2015,'cost_variable'],
	262:['CostVariable',2030,'IMPRESLPG',2015,'cost_variable'],
	263:['CostVariable',2035,'IMPRESLPG',2015,'cost_variable'],
	264:['CostVariable',2040,'IMPRESLPG',2015,'cost_variable'],
	265:['CostVariable',2015,'IMPCOMLPG',2015,'cost_variable'],
	266:['CostVariable',2020,'IMPCOMLPG',2015,'cost_variable'],
	267:['CostVariable',2025,'IMPCOMLPG',2015,'cost_variable'],
	268:['CostVariable',2030,'IMPCOMLPG',2015,'cost_variable'],
	269:['CostVariable',2035,'IMPCOMLPG',2015,'cost_variable'],
	270:['CostVariable',2040,'IMPCOMLPG',2015,'cost_variable'],
	271:['CostVariable',2015,'IMPCOMDISTOIL',2015,'cost_variable'],
	272:['CostVariable',2020,'IMPCOMDISTOIL',2015,'cost_variable'],
	273:['CostVariable',2025,'IMPCOMDISTOIL',2015,'cost_variable'],
	274:['CostVariable',2030,'IMPCOMDISTOIL',2015,'cost_variable'],
	275:['CostVariable',2035,'IMPCOMDISTOIL',2015,'cost_variable'],
	276:['CostVariable',2040,'IMPCOMDISTOIL',2015,'cost_variable'],
	277:['CostVariable',2015,'IMPCOMRFO',2015,'cost_variable'],
	278:['CostVariable',2020,'IMPCOMRFO',2015,'cost_variable'],
	279:['CostVariable',2025,'IMPCOMRFO',2015,'cost_variable'],
	280:['CostVariable',2030,'IMPCOMRFO',2015,'cost_variable'],
	281:['CostVariable',2035,'IMPCOMRFO',2015,'cost_variable'],
	282:['CostVariable',2040,'IMPCOMRFO',2015,'cost_variable'],
	283:['CostVariable',2015,'IMPRESDISTOIL',2015,'cost_variable'],
	284:['CostVariable',2020,'IMPRESDISTOIL',2015,'cost_variable'],
	285:['CostVariable',2025,'IMPRESDISTOIL',2015,'cost_variable'],
	286:['CostVariable',2030,'IMPRESDISTOIL',2015,'cost_variable'],
	287:['CostVariable',2035,'IMPRESDISTOIL',2015,'cost_variable'],
	288:['CostVariable',2040,'IMPRESDISTOIL',2015,'cost_variable'],
	289:['CostVariable',2015,'IMPRESKER',2015,'cost_variable'],
	290:['CostVariable',2020,'IMPRESKER',2015,'cost_variable'],
	291:['CostVariable',2025,'IMPRESKER',2015,'cost_variable'],
	292:['CostVariable',2030,'IMPRESKER',2015,'cost_variable'],
	293:['CostVariable',2035,'IMPRESKER',2015,'cost_variable'],
	294:['CostVariable',2040,'IMPRESKER',2015,'cost_variable'],
	295:['CostInvest','T_LDV_CDSL_N',2020,'cost_invest'],
	296:['CostInvest','T_LDV_CDSL_N',2025,'cost_invest'],
	297:['CostInvest','T_LDV_CDSL_N',2030,'cost_invest'],
	298:['CostInvest','T_LDV_CDSL_N',2035,'cost_invest'],
	299:['CostInvest','T_LDV_CDSL_N',2040,'cost_invest'],
	300:['CostInvest','T_LDV_FDSL_N',2020,'cost_invest'],
	301:['CostInvest','T_LDV_FDSL_N',2025,'cost_invest'],
	302:['CostInvest','T_LDV_FDSL_N',2030,'cost_invest'],
	303:['CostInvest','T_LDV_FDSL_N',2035,'cost_invest'],
	304:['CostInvest','T_LDV_FDSL_N',2040,'cost_invest'],
	305:['CostInvest','T_LDV_SSDSL_N',2020,'cost_invest'],
	306:['CostInvest','T_LDV_SSDSL_N',2025,'cost_invest'],
	307:['CostInvest','T_LDV_SSDSL_N',2030,'cost_invest'],
	308:['CostInvest','T_LDV_SSDSL_N',2035,'cost_invest'],
	309:['CostInvest','T_LDV_SSDSL_N',2040,'cost_invest'],
	310:['CostInvest','T_LDV_LSDSL_N',2020,'cost_invest'],
	311:['CostInvest','T_LDV_LSDSL_N',2025,'cost_invest'],
	312:['CostInvest','T_LDV_LSDSL_N',2030,'cost_invest'],
	313:['CostInvest','T_LDV_LSDSL_N',2035,'cost_invest'],
	314:['CostInvest','T_LDV_LSDSL_N',2040,'cost_invest'],
	315:['CostInvest','T_LDV_MVDSL_N',2020,'cost_invest'],
	316:['CostInvest','T_LDV_MVDSL_N',2025,'cost_invest'],
	317:['CostInvest','T_LDV_MVDSL_N',2030,'cost_invest'],
	318:['CostInvest','T_LDV_MVDSL_N',2035,'cost_invest'],
	319:['CostInvest','T_LDV_MVDSL_N',2040,'cost_invest'],
	320:['CostInvest','T_LDV_PDSL_N',2020,'cost_invest'],
	321:['CostInvest','T_LDV_PDSL_N',2025,'cost_invest'],
	322:['CostInvest','T_LDV_PDSL_N',2030,'cost_invest'],
	323:['CostInvest','T_LDV_PDSL_N',2035,'cost_invest'],
	324:['CostInvest','T_LDV_PDSL_N',2040,'cost_invest'],
	325:['CostInvest','T_HDV_BDSL_N',2020,'cost_invest'],
	326:['CostInvest','T_HDV_BDSL_N',2025,'cost_invest'],
	327:['CostInvest','T_HDV_BDSL_N',2030,'cost_invest'],
	328:['CostInvest','T_HDV_BDSL_N',2035,'cost_invest'],
	329:['CostInvest','T_HDV_BDSL_N',2040,'cost_invest'],
	330:['CostInvest','T_HDV_BDSL_10_N',2020,'cost_invest'],
	331:['CostInvest','T_HDV_BDSL_10_N',2025,'cost_invest'],
	332:['CostInvest','T_HDV_BDSL_10_N',2030,'cost_invest'],
	333:['CostInvest','T_HDV_BDSL_10_N',2035,'cost_invest'],
	334:['CostInvest','T_HDV_BDSL_10_N',2040,'cost_invest'],
	335:['CostInvest','T_HDV_TCDSL_N',2020,'cost_invest'],
	336:['CostInvest','T_HDV_TCDSL_N',2025,'cost_invest'],
	337:['CostInvest','T_HDV_TCDSL_N',2030,'cost_invest'],
	338:['CostInvest','T_HDV_TCDSL_N',2035,'cost_invest'],
	339:['CostInvest','T_HDV_TCDSL_N',2040,'cost_invest'],
	340:['CostInvest','T_HDV_TCDSL20_N',2020,'cost_invest'],
	341:['CostInvest','T_HDV_TCDSL20_N',2025,'cost_invest'],
	342:['CostInvest','T_HDV_TCDSL20_N',2030,'cost_invest'],
	343:['CostInvest','T_HDV_TCDSL20_N',2035,'cost_invest'],
	344:['CostInvest','T_HDV_TCDSL20_N',2040,'cost_invest'],
	345:['CostInvest','T_HDV_TCBIODSL_N',2015,'cost_invest'],
	346:['CostInvest','T_HDV_TCBIODSL_N',2020,'cost_invest'],
	347:['CostInvest','T_HDV_TCBIODSL_N',2025,'cost_invest'],
	348:['CostInvest','T_HDV_TCBIODSL_N',2030,'cost_invest'],
	349:['CostInvest','T_HDV_TCBIODSL_N',2035,'cost_invest'],
	350:['CostInvest','T_HDV_TCBIODSL_N',2040,'cost_invest'],
	351:['CostInvest','T_HDV_THDSL_N',2020,'cost_invest'],
	352:['CostInvest','T_HDV_THDSL_N',2025,'cost_invest'],
	353:['CostInvest','T_HDV_THDSL_N',2030,'cost_invest'],
	354:['CostInvest','T_HDV_THDSL_N',2035,'cost_invest'],
	355:['CostInvest','T_HDV_THDSL_N',2040,'cost_invest'],
	356:['CostInvest','T_HDV_THDSL_10_N',2020,'cost_invest'],
	357:['CostInvest','T_HDV_THDSL_10_N',2025,'cost_invest'],
	358:['CostInvest','T_HDV_THDSL_10_N',2030,'cost_invest'],
	359:['CostInvest','T_HDV_THDSL_10_N',2035,'cost_invest'],
	360:['CostInvest','T_HDV_THDSL_10_N',2040,'cost_invest'],
	361:['CostInvest','T_HDV_THDSL20_10_N',2020,'cost_invest'],
	362:['CostInvest','T_HDV_THDSL20_10_N',2025,'cost_invest'],
	363:['CostInvest','T_HDV_THDSL20_10_N',2030,'cost_invest'],
	364:['CostInvest','T_HDV_THDSL20_10_N',2035,'cost_invest'],
	365:['CostInvest','T_HDV_THDSL20_10_N',2040,'cost_invest'],
	366:['CostInvest','T_HDV_THDSL20_N',2020,'cost_invest'],
	367:['CostInvest','T_HDV_THDSL20_N',2025,'cost_invest'],
	368:['CostInvest','T_HDV_THDSL20_N',2030,'cost_invest'],
	369:['CostInvest','T_HDV_THDSL20_N',2035,'cost_invest'],
	370:['CostInvest','T_HDV_THDSL20_N',2040,'cost_invest'],
	371:['CostInvest','T_HDV_THDSL_20_N',2020,'cost_invest'],
	372:['CostInvest','T_HDV_THDSL_20_N',2025,'cost_invest'],
	373:['CostInvest','T_HDV_THDSL_20_N',2030,'cost_invest'],
	374:['CostInvest','T_HDV_THDSL_20_N',2035,'cost_invest'],
	375:['CostInvest','T_HDV_THDSL_20_N',2040,'cost_invest'],
	376:['CostInvest','T_HDV_THDSL20_20_N',2020,'cost_invest'],
	377:['CostInvest','T_HDV_THDSL20_20_N',2025,'cost_invest'],
	378:['CostInvest','T_HDV_THDSL20_20_N',2030,'cost_invest'],
	379:['CostInvest','T_HDV_THDSL20_20_N',2035,'cost_invest'],
	380:['CostInvest','T_HDV_THDSL20_20_N',2040,'cost_invest'],
	381:['CostInvest','T_HDV_THDSL20_40_N',2020,'cost_invest'],
	382:['CostInvest','T_HDV_THDSL20_40_N',2025,'cost_invest'],
	383:['CostInvest','T_HDV_THDSL20_40_N',2030,'cost_invest'],
	384:['CostInvest','T_HDV_THDSL20_40_N',2035,'cost_invest'],
	385:['CostInvest','T_HDV_THDSL20_40_N',2040,'cost_invest'],
	386:['CostInvest','R_SH_HPELC_VER1_N',2020,'cost_invest'],
	387:['CostInvest','R_SH_HPELC_VER1_N',2025,'cost_invest'],
	388:['CostInvest','R_SH_HPELC_VER1_N',2030,'cost_invest'],
	389:['CostInvest','R_SH_HPELC_VER1_N',2035,'cost_invest'],
	390:['CostInvest','R_SH_HPELC_VER1_N',2040,'cost_invest'],
	391:['CostInvest','R_SH_HPELC_VER2_N',2020,'cost_invest'],
	392:['CostInvest','R_SH_HPELC_VER2_N',2025,'cost_invest'],
	393:['CostInvest','R_SH_HPELC_VER2_N',2030,'cost_invest'],
	394:['CostInvest','R_SH_HPELC_VER2_N',2035,'cost_invest'],
	395:['CostInvest','R_SH_HPELC_VER2_N',2040,'cost_invest'],
	396:['CostInvest','R_SH_HPELC_VER3_N',2020,'cost_invest'],
	397:['CostInvest','R_SH_HPELC_VER3_N',2025,'cost_invest'],
	398:['CostInvest','R_SH_HPELC_VER3_N',2030,'cost_invest'],
	399:['CostInvest','R_SH_HPELC_VER3_N',2035,'cost_invest'],
	400:['CostInvest','R_SH_HPELC_VER3_N',2040,'cost_invest'],
	401:['CostInvest','R_SH_HPELC_VER4_N',2020,'cost_invest'],
	402:['CostInvest','R_SH_HPELC_VER4_N',2025,'cost_invest'],
	403:['CostInvest','R_SH_HPELC_VER4_N',2030,'cost_invest'],
	404:['CostInvest','R_SH_HPELC_VER4_N',2035,'cost_invest'],
	405:['CostInvest','R_SH_HPELC_VER4_N',2040,'cost_invest'],
	406:['CostInvest','R_SH_HPGEO_N',2020,'cost_invest'],
	407:['CostInvest','R_SH_HPGEO_N',2025,'cost_invest'],
	408:['CostInvest','R_SH_HPGEO_N',2030,'cost_invest'],
	409:['CostInvest','R_SH_HPGEO_N',2035,'cost_invest'],
	410:['CostInvest','R_SH_HPGEO_N',2040,'cost_invest'],
	411:['CostInvest','R_SH_HPNGA_N',2020,'cost_invest'],
	412:['CostInvest','R_SH_HPNGA_N',2025,'cost_invest'],
	413:['CostInvest','R_SH_HPNGA_N',2030,'cost_invest'],
	414:['CostInvest','R_SH_HPNGA_N',2035,'cost_invest'],
	415:['CostInvest','R_SH_HPNGA_N',2040,'cost_invest'],
	416:['CostInvest','C_SH_AHPST_ELC_N',2020,'cost_invest'],
	417:['CostInvest','C_SH_AHPST_ELC_N',2025,'cost_invest'],
	418:['CostInvest','C_SH_AHPST_ELC_N',2030,'cost_invest'],
	419:['CostInvest','C_SH_AHPST_ELC_N',2035,'cost_invest'],
	420:['CostInvest','C_SH_AHPST_ELC_N',2040,'cost_invest'],
	421:['CostInvest','C_SH_AHPHE_ELC_N',2020,'cost_invest'],
	422:['CostInvest','C_SH_AHPHE_ELC_N',2025,'cost_invest'],
	423:['CostInvest','C_SH_AHPHE_ELC_N',2030,'cost_invest'],
	424:['CostInvest','C_SH_AHPHE_ELC_N',2035,'cost_invest'],
	425:['CostInvest','C_SH_AHPHE_ELC_N',2040,'cost_invest'],
	426:['CostInvest','C_SH_GHPST_ELC_N',2020,'cost_invest'],
	427:['CostInvest','C_SH_GHPST_ELC_N',2025,'cost_invest'],
	428:['CostInvest','C_SH_GHPST_ELC_N',2030,'cost_invest'],
	429:['CostInvest','C_SH_GHPST_ELC_N',2035,'cost_invest'],
	430:['CostInvest','C_SH_GHPST_ELC_N',2040,'cost_invest'],
	431:['CostInvest','C_SH_GHPHE_ELC_N',2020,'cost_invest'],
	432:['CostInvest','C_SH_GHPHE_ELC_N',2025,'cost_invest'],
	433:['CostInvest','C_SH_GHPHE_ELC_N',2030,'cost_invest'],
	434:['CostInvest','C_SH_GHPHE_ELC_N',2035,'cost_invest'],
	435:['CostInvest','C_SH_GHPHE_ELC_N',2040,'cost_invest'],
	436:['CostInvest','C_SH_HPST_NGA_N',2020,'cost_invest'],
	437:['CostInvest','C_SH_HPST_NGA_N',2025,'cost_invest'],
	438:['CostInvest','C_SH_HPST_NGA_N',2030,'cost_invest'],
	439:['CostInvest','C_SH_HPST_NGA_N',2035,'cost_invest'],
	440:['CostInvest','C_SH_HPST_NGA_N',2040,'cost_invest'],
	441:['CostInvest','T_LDV_MCELC_N',2025,'cost_invest'],
	442:['CostInvest','T_LDV_MCELC_N',2030,'cost_invest'],
	443:['CostInvest','T_LDV_MCELC_N',2035,'cost_invest'],
	444:['CostInvest','T_LDV_MCELC_N',2040,'cost_invest'],
	445:['CostInvest','T_LDV_CELC_N',2020,'cost_invest'],
	446:['CostInvest','T_LDV_CELC_N',2025,'cost_invest'],
	447:['CostInvest','T_LDV_CELC_N',2030,'cost_invest'],
	448:['CostInvest','T_LDV_CELC_N',2035,'cost_invest'],
	449:['CostInvest','T_LDV_CELC_N',2040,'cost_invest'],
	450:['CostInvest','T_LDV_FELC_N',2020,'cost_invest'],
	451:['CostInvest','T_LDV_FELC_N',2025,'cost_invest'],
	452:['CostInvest','T_LDV_FELC_N',2030,'cost_invest'],
	453:['CostInvest','T_LDV_FELC_N',2035,'cost_invest'],
	454:['CostInvest','T_LDV_FELC_N',2040,'cost_invest'],
	455:['CostInvest','T_LDV_SSELC_N',2020,'cost_invest'],
	456:['CostInvest','T_LDV_SSELC_N',2025,'cost_invest'],
	457:['CostInvest','T_LDV_SSELC_N',2030,'cost_invest'],
	458:['CostInvest','T_LDV_SSELC_N',2035,'cost_invest'],
	459:['CostInvest','T_LDV_SSELC_N',2040,'cost_invest'],
    }

	m=len(param_values)
	for j in range(0,m):
		Newdbpath=sys.path[0]+'/data_files/1st/Method_of_Morris'+str(k)+'.db'
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
	NewConfigfilePath=sys.path[0]+'/temoa_model/config_sample'+str(k)
	copyfile(sys.path[0]+'/temoa_model/config_sample',NewConfigfilePath)
	with open(sys.path[0]+'/temoa_model/config_sample', 'r') as file:
		data = file.readlines()
	data[13]='--input=data_files/1st/Method_of_Morris'+str(k)+'.db'
	data[20]='--output=data_files/1st/Method_of_Morris'+str(k)+'.db'
	with open(NewConfigfilePath, 'w') as file:
		file.writelines(data)
	os.system('python temoa_model/ --config=temoa_model/config_sample'+str(k))
	print(k)
	
	MonteCarlo_Objectives=[]
	
	Newdbpath=sys.path[0]+'/data_files/1st/Method_of_Morris'+str(k)+'.db'
	con=sqlite3.connect(Newdbpath)
	cur = con.cursor()
	cur.execute("SELECT * FROM Output_Objective")
	output_query = cur.fetchall()
	MonteCarlo_Objectives.append(output_query[-1][-1])
	
	cur.execute("SELECT emissions_comm, SUM(emissions) FROM Output_Emissions WHERE emissions_comm='co2'")
	output_query = cur.fetchall()
	MonteCarlo_Objectives.append(output_query[-1][-1])
		
	cur.execute("SELECT emissions_comm, SUM(emissions) FROM Output_Emissions WHERE emissions_comm='co2' and t_periods=2015 and (sector<>'supply' OR tech='IMPTRNE85' OR tech='IMPTRNBIODSL')")
	output_query = cur.fetchall()
	MonteCarlo_Objectives.append(output_query[-1][-1])
	
	cur.execute("SELECT emissions_comm, SUM(emissions) FROM Output_Emissions WHERE emissions_comm='co2' and t_periods=2020 and (sector<>'supply' OR tech='IMPTRNE85' OR tech='IMPTRNBIODSL')")
	output_query = cur.fetchall()
	MonteCarlo_Objectives.append(output_query[-1][-1])
	
	cur.execute("SELECT emissions_comm, SUM(emissions) FROM Output_Emissions WHERE emissions_comm='co2' and t_periods=2025 and (sector<>'supply' OR tech='IMPTRNE85' OR tech='IMPTRNBIODSL')")
	output_query = cur.fetchall()
	MonteCarlo_Objectives.append(output_query[-1][-1])
	
	cur.execute("SELECT emissions_comm, SUM(emissions) FROM Output_Emissions WHERE emissions_comm='co2' and t_periods=2030 and (sector<>'supply' OR tech='IMPTRNE85' OR tech='IMPTRNBIODSL')")
	output_query = cur.fetchall()
	MonteCarlo_Objectives.append(output_query[-1][-1])
	
	cur.execute("SELECT emissions_comm, SUM(emissions) FROM Output_Emissions WHERE emissions_comm='co2' and t_periods=2035 and (sector<>'supply' OR tech='IMPTRNE85' OR tech='IMPTRNBIODSL')")
	output_query = cur.fetchall()
	MonteCarlo_Objectives.append(output_query[-1][-1])
	
	cur.execute("SELECT emissions_comm, SUM(emissions) FROM Output_Emissions WHERE emissions_comm='co2' and t_periods=2040 and (sector<>'supply' OR tech='IMPTRNE85' OR tech='IMPTRNBIODSL')")
	output_query = cur.fetchall()
	MonteCarlo_Objectives.append(output_query[-1][-1])	

	cur.execute("SELECT emissions_comm, SUM(emissions) FROM Output_Emissions WHERE emissions_comm='co2' and tech='IMPELCNGA'")
	output_query = cur.fetchall()
	MonteCarlo_Objectives.append(output_query[-1][-1])	

	cur.execute("SELECT emissions_comm, SUM(emissions) FROM Output_Emissions WHERE emissions_comm='co2' and tech LIKE 'IMPELCCOA%'")
	output_query = cur.fetchall()
	MonteCarlo_Objectives.append(output_query[-1][-1])
	
	con.close()
	return MonteCarlo_Objectives

problem = read_param_file(sys.path[0]+'/Monte-Carlo-1st.txt')

Number_of_Simulations=1000
param_values=np.zeros((Number_of_Simulations,problem['num_vars']))

lhd = lhs(len(set(problem['groups'])), samples=Number_of_Simulations)
for k in range(0,Number_of_Simulations):
	c=0	#c points to each group of inputs
	param_values[k][0]=problem['bounds'][0][0]+lhd[k][c]*(problem['bounds'][0][1]-problem['bounds'][0][0])
	for i in range(1,problem['num_vars']):
		if problem['groups'][i]==problem['groups'][i-1]:
		   param_values[k,i]=problem['bounds'][i][0]+lhd[k][c]*(problem['bounds'][i][1]-problem['bounds'][i][0])
		else:
		   c=c+1
		   param_values[k,i]=problem['bounds'][i][0]+lhd[k][c]*(problem['bounds'][i][1]-problem['bounds'][i][0])
	Newdbpath=sys.path[0]+'/data_files/1st/Method_of_Morris'+str(k)+'.db'
	copyfile(sys.path[0]+'/data_files/1st/Method_of_Morris.db',Newdbpath)
num_cores = multiprocessing.cpu_count()
MonteCarlo_Objectives = Parallel(n_jobs=num_cores)(delayed(evaluate)(param_values[ii,:],ii) for ii in range(0,Number_of_Simulations))
MonteCarlo_Objectives=array(MonteCarlo_Objectives)

with open('MonteCarlo1st.csv', 'w') as f:
	writer = csv.writer(f, delimiter=',')
	for i in range(0,Number_of_Simulations):
		writer.writerow(np.append(lhd[i],MonteCarlo_Objectives[i]))
f.close()
print("--- %s seconds ---" % (time.time() - start_time))
