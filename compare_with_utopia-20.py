#!/usr/bin/env python

import os, shutil, sys

from base64 import decodestring
from cStringIO import StringIO
from subprocess import call
from sys import stdin as SI, stderr as SE
from tempfile import mkdtemp
from zipfile import ZipFile
from zlib import decompress

if SI.isatty():
	print """
This script is meant _solely_ for use in comparing Utopia as solved by MARKAL
and by Temoa.  This script is guaranteed "correct" only as the Temoa model is
formulated within the energysystem-process-match-MARKAL Temoa branch on 16 Dec
2011.  After any commits or changes, this script may have to be updated.  You
have been warned.

To run this program, use stdin:

$ %s  <  utopia.sol

It will create an OpenDocument spreadsheet, for which you may need LibreOffice
to read.
""" % sys.argv[0]
	sys.exit()

ods_base = StringIO(decodestring("""\
UEsDBBQAAAAIAO0Kej+FbDmKLAAAAC4AAAAIABwAbWltZXR5cGVVVAkAA96F0E7ehdBOdXgLAAEE
6AMAAAToAwAABcGBCQAgCATAjWwm0YeEUklr/u44c5lwW/h4rhRcVhQJ15C74U2VB6w1gf5QSwME
CgAAAAAAxAt6PwAAAAAAAAAAAAAAAAkAHABNRVRBLUlORi9VVAkAA2+H0E7ehdBOdXgLAAEE6AMA
AAToAwAAUEsDBBQAAAAIAMQLej9Zlvpo1QAAAJMCAAAVABwATUVUQS1JTkYvbWFuaWZlc3QueG1s
VVQJAANvh9BOb4fQTnV4CwABBOgDAAAE6AMAAK2STW7DIBCF9z6Fxd7QZlUh4+xygvYACMYNEgzI
M47i25dEip2q7aKSdwwz772Pn/54TbG9wEQhoxGv8kW0gC77gJ9GfLyfujdxHJo+WQwjEOvHoq06
pLU0Yp5QZ0uBNNoEpNnpXAB9dnMCZP19Xt+T1uoJ4CCGpt3yxhChq/pp2aYT+GA7XgoYYUuJwVmu
anVBL+8I8jlZUpnAejoD8F+R2/Y4x9gVy2cjlFD/QmG4sqrH/N0tAVt56+5pSsBcX4p2N3YZ+XZ3
uwPzEmHF7dWPfzU0X1BLAwQUAAAACADtCno/oYL9g2kBAADGAgAACAAcAG1ldGEueG1sVVQJAAPe
hdBO3oXQTnV4CwABBOgDAAAE6AMAAI2SzW6DMBCE730K5PYK5ichiQXkVlVqpF5SqbfImIW6BRsZ
E/L4BRNHtMqhki+e/dYzu3KyvzS1cwbVcSlSFHg+ckAwWXBRpej9+Oxu0T57SGRZcgakkKxvQGi3
AU2dsVV0ZC6lqFeCSNrxjgjaQEc0I7IFYVvIkibGaFYuNRffKfrUuiUYD8PgDZEnVYWD3W6HTdWi
Bbtxba9qQxUMQw2TQ4cDL8CWnRL+N9TELiNJKW9GEz6HNnah76/wfLd0pYqivjfAyEZ4TEg1dc8c
hkfkXMdfLDxEmd3uFCNLCkbGDshCPwhcfzpH3yfmJNgWJ4opoFqq7BXOXDgvvdCgDGELiZmrAgHK
3A88V/BmvHDkrZ8OXPSX08c2PsUrZ1E8tUp+AdM4XG9oEeVuGdOgZGsXAhqWeZTgPw/PRrfP0Wmq
eac5c4yuaV6Dy+QYcBwYzSKDurZaGG+uqswnX6v7CGcJ/rUcfO8jZj9QSwECHgMUAAAACADtCno/
hWw5iiwAAAAuAAAACAAYAAAAAAABAAAApIEAAAAAbWltZXR5cGVVVAUAA96F0E51eAsAAQToAwAA
BOgDAABQSwECHgMKAAAAAADEC3o/AAAAAAAAAAAAAAAACQAYAAAAAAAAABAA7UFuAAAATUVUQS1J
TkYvVVQFAANvh9BOdXgLAAEE6AMAAAToAwAAUEsBAh4DFAAAAAgAxAt6P1mW+mjVAAAAkwIAABUA
GAAAAAAAAQAAAKSBsQAAAE1FVEEtSU5GL21hbmlmZXN0LnhtbFVUBQADb4fQTnV4CwABBOgDAAAE
6AMAAFBLAQIeAxQAAAAIAO0Kej+hgv2DaQEAAMYCAAAIABgAAAAAAAEAAACkgdUBAABtZXRhLnht
bFVUBQAD3oXQTnV4CwABBOgDAAAE6AMAAFBLBQYAAAAABAAEAEYBAACAAwAAAAA=
"""))


content = decompress(decodestring("""\
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
"""))

settings = decompress(decodestring("""\
eNrtmVFv2jAQx78KyjtNoR0bUaGiTFvZuq0itFv3Mh3JAVYdX2Q7pOzTzyFQtWnSUUg6Ie2pJbF/
9+d8Pt+Zk9O7gNfmKBUj0bEaB4dWDYVHPhPTjnU1+lB/Z512T2gyYR46PnlRgELXFWptRqiamS2U
k77uWJEUDoFiyhEQoHK051CIYj3NeTjaWdpKn9xxJm471kzr0LHtOI4P4qMDklO70W637eXb9VCP
xIRNNzWVjn5oiojuDSUTUjFLY83Dw2M7/WzVViIfeKZp3fth/fW7JysD6Z860xgkvqmtHifSOpYx
6cwZxvdes/LmPZ5zzRQbc+xJhBGF1vqlXoTmJRPa6h6e2E8hLwJf4ERXQ/7OfD3LQzebrca7nfHn
yKazXOmNt+328ab8egBhnQkf79DP2sI4f5WWc0x8ycUmijEe+BmZSksTAlY3CYjGi5Qm0IzOERiP
/E3o4ylfQN4Cv1YjDAh+XWkKGWwQj/1IKpKXpJg22+FHiWHzmHxTIvmcJPtNQgN3Q870F/Ixuxgz
kjsEPErNvKroGfVrB5W5YR/qr4Df8zSb45I+BDEtcE9zO/hab8lJbI0dFmWYHbnlJvM19Yy0pqBE
8E+iYGQopUZ0Ar0GHmGe0Pa2LoApJon2WXhrS7g7o/ijZNkcPibiCMLqahlhPtl+/uiwn8vxm+6s
ZfYvOF7y0vzOeciTxPkYZPHx/vZ/vO0ab4mBM1Pk3F5KTIqEotibAFe4vZmfKGmpX708uDfhfyVd
FXq7Hfk3ckLtEyeZQXNK9lOj2TpqNt+0SljXCrxyDspIjwIxpPgcwTdNSyVG3BmiNmmnAvpAfYu0
afTQXQRj4spFXYURV0A4oiEojbKCnZWCB2rVrFRmYYjKrHdhKd7YOhFn8TdV4N1o7LM5U4XyS4Lf
lAgfqBTfu2PKXQhvJkmw3/h6pcGqUc0foFBvfheRPogkJAv8kkuJqs+NCwJ/aNIXCb6oYOtchT5o
/CBNqYFByM3/+3WK9Dg3x4ip7/QnGvdBeMj3NkXuYwroRZr6wL2omtBZrqwRjzrK9ohjUNg6PmMC
5MKy/2kBNlDvV1es7gxkcf7bIUKqLTRWbv5qPuT3Thv494KJ2zSbFF/7HG3r388oRU8xEJeR8HQE
ObcypTQBMMfr9Hb7m+hzUriX9VAvDPniSqF8DxrKj5b9LrdepaiuurmpruXrmwwGnlmAPgWhRJXs
hdJvIcorHF+lCyysLu0nv33ZRb8Kdv8A5iNY3Q==
"""))


styles = decompress(decodestring("""\
eNrdWG1v2zYQ/iuCAgwbMJmSnCCxZjvYVnQo0ARDm+47LVESV0oUSNpO9ut3JCVFb3a0rUG3OUAM
HZ87PrxXyuvbx4I5ByIk5eXGDRa+65Ay5gkts4376eGtd+Pebtc8TWlMooTH+4KUypPqiRHpgG4p
I7u4cfeijDiWVEYlLoiMVBzxipSNUtRFR2YnKzHG5qobcFdbkUc1V1lje7p4N39nA+5qJwIf5ypr
LLi0q57yucqPknkp92JeVFjRAYtHRsvPGzdXqooQOh6Pi+NywUWGgtVqhcxqSzhucdVeMINKYkQY
0ZtJFCwC1GALovBcfhrbpVTuix0Rs12DFR5FtRJEAgSOq9NynqGuTi+/Dtns7DpkJ9wc51jMzjMD
7qfKMpmfKsukq1tglZ+I7w26g0Xz7+79c16JYu5eGttzVSxoNfuYFt3V55y3VLWCLXZDN/T9S2Sf
O+jjWfhRUEVEBx6fhceYxa3HeTHlNMAFCBAeOeiUb9BCH/qk5SskSMWFaomk85sdeCdsSzVXBTtd
qnq1gWYiSdiJAywRlC0UjXeg5HjR62Xn/b9CBtSmtJRLNbXHwwek1zzdLqEh1B27MyRCtx0JKYdx
kOKYeAmJmdyubSm3Ysc+aydt3B8FxXBEqLIGUFD29CzvquoVLyMlERSiLo9Uyh6ioiqGujhg0NWH
QjO2DmbtjRMuStMRN+5PnCWvS+wN+R3/tnc+4lJOsPsGV1z+0MFYwXlKT1KR4h9xEpwmZjvnLWZs
h+PPp7mNsV+MIzqVZLXcXkOasyQkxXtWX04ayzVXk/heTBhzG3iFBc4ErnKvElArQlG40dglQIMV
XnkJlQqX+nLjL65o+ew3XRpjPcOzl+opjxgusz3OQEZKI4j5vlQCSH366A4VPWgpuBxmhcE0dhrI
H3mzUhtsFn6+H5vVQ42Rx/OGW1BOh6bbpXf3JjATHt+u7dyvx38vDNYn97pv9EBO/QRhpQVmXsUg
yFB20DLrlYKWHi0VycBiQjOqizIwFCZ2a6Iz3vqNZeq+nBYvRLYN0ESJPDvmBTbviZQPOS7P0HHa
JG3v297kUcwk6K4bL7d5XNvrnghSUNPNBMQ2gcgyDne1i3AZLpP4dIabxLXQ1HzcE0kfmCQ30iOh
WQ4jZqe76Gzv/CIIhrH/tx009O6X8lCa+vCZf457uFxhdm/y87Ui3WmSTTOsH/Fecbg60tjrd8lK
VzrDT3yvemzvqiJwJ0DjWtC3MniX8QqegB4Tnto9p01OcDIsx1qWcg5hHfhZ13dep4m/CFdX19R2
yQKLDNYYSfVKXyhqfF+640rpW5+/8Fc3l7Zbo9OsajpfgymMlkmafUpoFIsZMQz/ZzE0tchFot8n
w8XlqoITcwat98I3HwOocGJ/sAA1/zpo1MYlHPv6r3VRBwHjJyOjhBkd97+RUf9Wp72c3+hk96oX
CixbE21Pq4Xa0rmp362IiaZn6W/X5leiqv6WOSEWvb29vV2jobCWVAMnDMKvI9l0cSrhlgMjIMVM
9m7i2jft7r/qs9QPmra95myDZr+ObEShMdVz+lkKaOTHl1z7oX4jPuPZcORZ+yRIBu+RhtBfdLbz
rcUpqlgXYp+/Gzmit1NPZKposDvMV3Jm1DotyDtgtgdh6AeBF/heuHS3gY/CJdKSmoUGbr93GsLA
PriOwutoed2SnkqfPr+vllMO6gLNW8B2teoCreyVcg9NVzua/h16+ycmmCwq
"""))


data = SI.read().split('\n')
#with open( 'test.sol', 'r') as f:
#	data = f.read().split('\n')

if data[0] == "No solution found.":
	SE.write( "No data; likely an infeasible solution.\n" )
	sys.exit(1)

results = dict()
obj_name, obj_val = data[1].split(': ')
obj_val = float(obj_val)

for line in data:
	if not line: break
	if line[0] != ' ': continue
	val, name = line.split()
	results.update({name : float(val)})

content %= dict(
  obj_name  = obj_name,
  obj_value = obj_val,
  act_1990E01 = results.get('V_ActivityByPeriodAndTech(1990,E01)', 0),
  act_1990E21 = results.get('V_ActivityByPeriodAndTech(1990,E21)', 0),
  act_1990E31 = results.get('V_ActivityByPeriodAndTech(1990,E31)', 0),
  act_1990E51 = results.get('V_ActivityByPeriodAndTech(1990,E51)', 0),
  act_1990E70 = results.get('V_ActivityByPeriodAndTech(1990,E70)', 0),
  act_2000E01 = results.get('V_ActivityByPeriodAndTech(2000,E01)', 0),
  act_2000E21 = results.get('V_ActivityByPeriodAndTech(2000,E21)', 0),
  act_2000E31 = results.get('V_ActivityByPeriodAndTech(2000,E31)', 0),
  act_2000E51 = results.get('V_ActivityByPeriodAndTech(2000,E51)', 0),
  act_2000E70 = results.get('V_ActivityByPeriodAndTech(2000,E70)', 0),
  act_2010E01 = results.get('V_ActivityByPeriodAndTech(2010,E01)', 0),
  act_2010E21 = results.get('V_ActivityByPeriodAndTech(2010,E21)', 0),
  act_2010E31 = results.get('V_ActivityByPeriodAndTech(2010,E31)', 0),
  act_2010E51 = results.get('V_ActivityByPeriodAndTech(2010,E51)', 0),
  act_2010E70 = results.get('V_ActivityByPeriodAndTech(2010,E70)', 0),
  act_1990RHE = results.get('V_ActivityByPeriodAndTech(1990,RHE)', 0),
  act_1990RHO = results.get('V_ActivityByPeriodAndTech(1990,RHO)', 0),
  act_1990RL1 = results.get('V_ActivityByPeriodAndTech(1990,RL1)', 0),
  act_1990TXD = results.get('V_ActivityByPeriodAndTech(1990,TXD)', 0),
  act_1990TXE = results.get('V_ActivityByPeriodAndTech(1990,TXE)', 0),
  act_1990TXG = results.get('V_ActivityByPeriodAndTech(1990,TXG)', 0),
  act_2000RHE = results.get('V_ActivityByPeriodAndTech(2000,RHE)', 0),
  act_2000RHO = results.get('V_ActivityByPeriodAndTech(2000,RHO)', 0),
  act_2000RL1 = results.get('V_ActivityByPeriodAndTech(2000,RL1)', 0),
  act_2000TXD = results.get('V_ActivityByPeriodAndTech(2000,TXD)', 0),
  act_2000TXE = results.get('V_ActivityByPeriodAndTech(2000,TXE)', 0),
  act_2000TXG = results.get('V_ActivityByPeriodAndTech(2000,TXG)', 0),
  act_2010RHE = results.get('V_ActivityByPeriodAndTech(2010,RHE)', 0),
  act_2010RHO = results.get('V_ActivityByPeriodAndTech(2010,RHO)', 0),
  act_2010RL1 = results.get('V_ActivityByPeriodAndTech(2010,RL1)', 0),
  act_2010TXD = results.get('V_ActivityByPeriodAndTech(2010,TXD)', 0),
  act_2010TXE = results.get('V_ActivityByPeriodAndTech(2010,TXE)', 0),
  act_2010TXG = results.get('V_ActivityByPeriodAndTech(2010,TXG)', 0),
  act_1990IMPDSL1 = results.get('V_ActivityByPeriodAndTech(1990,IMPDSL1)', 0),
  act_2000IMPDSL1 = results.get('V_ActivityByPeriodAndTech(2000,IMPDSL1)', 0),
  act_2010IMPDSL1 = results.get('V_ActivityByPeriodAndTech(2010,IMPDSL1)', 0),
  act_1990IMPGSL1 = results.get('V_ActivityByPeriodAndTech(1990,IMPGSL1)', 0),
  act_2000IMPGSL1 = results.get('V_ActivityByPeriodAndTech(2000,IMPGSL1)', 0),
  act_2010IMPGSL1 = results.get('V_ActivityByPeriodAndTech(2010,IMPGSL1)', 0),
  act_1990IMPHCO1 = results.get('V_ActivityByPeriodAndTech(1990,IMPHCO1)', 0),
  act_2000IMPHCO1 = results.get('V_ActivityByPeriodAndTech(2000,IMPHCO1)', 0),
  act_2010IMPHCO1 = results.get('V_ActivityByPeriodAndTech(2010,IMPHCO1)', 0),
  cap_1990E01 = results.get('V_CapacityAvailableByPeriodAndTech(1990,E01)', 0),
  cap_2000E01 = results.get('V_CapacityAvailableByPeriodAndTech(2000,E01)', 0),
  cap_2010E01 = results.get('V_CapacityAvailableByPeriodAndTech(2010,E01)', 0),
  cap_1990E21 = results.get('V_CapacityAvailableByPeriodAndTech(1990,E21)', 0),
  cap_2000E21 = results.get('V_CapacityAvailableByPeriodAndTech(2000,E21)', 0),
  cap_2010E21 = results.get('V_CapacityAvailableByPeriodAndTech(2010,E21)', 0),
  cap_1990E31 = results.get('V_CapacityAvailableByPeriodAndTech(1990,E31)', 0),
  cap_2000E31 = results.get('V_CapacityAvailableByPeriodAndTech(2000,E31)', 0),
  cap_2010E31 = results.get('V_CapacityAvailableByPeriodAndTech(2010,E31)', 0),
  cap_1990E51 = results.get('V_CapacityAvailableByPeriodAndTech(1990,E51)', 0),
  cap_2000E51 = results.get('V_CapacityAvailableByPeriodAndTech(2000,E51)', 0),
  cap_2010E51 = results.get('V_CapacityAvailableByPeriodAndTech(2010,E51)', 0),
  cap_1990E70 = results.get('V_CapacityAvailableByPeriodAndTech(1990,E70)', 0),
  cap_2000E70 = results.get('V_CapacityAvailableByPeriodAndTech(2000,E70)', 0),
  cap_2010E70 = results.get('V_CapacityAvailableByPeriodAndTech(2010,E70)', 0),
  cap_1990SRE = results.get('V_CapacityAvailableByPeriodAndTech(1990,SRE)', 0),
  cap_2000SRE = results.get('V_CapacityAvailableByPeriodAndTech(2000,SRE)', 0),
  cap_2010SRE = results.get('V_CapacityAvailableByPeriodAndTech(2010,SRE)', 0),
  cap_1990RHE = results.get('V_CapacityAvailableByPeriodAndTech(1990,RHE)', 0),
  cap_2000RHE = results.get('V_CapacityAvailableByPeriodAndTech(2000,RHE)', 0),
  cap_2010RHE = results.get('V_CapacityAvailableByPeriodAndTech(2010,RHE)', 0),
  cap_1990RHO = results.get('V_CapacityAvailableByPeriodAndTech(1990,RHO)', 0),
  cap_2000RHO = results.get('V_CapacityAvailableByPeriodAndTech(2000,RHO)', 0),
  cap_2010RHO = results.get('V_CapacityAvailableByPeriodAndTech(2010,RHO)', 0),
  cap_1990RL1 = results.get('V_CapacityAvailableByPeriodAndTech(1990,RL1)', 0),
  cap_2000RL1 = results.get('V_CapacityAvailableByPeriodAndTech(2000,RL1)', 0),
  cap_2010RL1 = results.get('V_CapacityAvailableByPeriodAndTech(2010,RL1)', 0),
  cap_1990TXD = results.get('V_CapacityAvailableByPeriodAndTech(1990,TXD)', 0),
  cap_2000TXD = results.get('V_CapacityAvailableByPeriodAndTech(2000,TXD)', 0),
  cap_2010TXD = results.get('V_CapacityAvailableByPeriodAndTech(2010,TXD)', 0),
  cap_1990TXE = results.get('V_CapacityAvailableByPeriodAndTech(1990,TXE)', 0),
  cap_2000TXE = results.get('V_CapacityAvailableByPeriodAndTech(2000,TXE)', 0),
  cap_2010TXE = results.get('V_CapacityAvailableByPeriodAndTech(2010,TXE)', 0),
  cap_1990TXG = results.get('V_CapacityAvailableByPeriodAndTech(1990,TXG)', 0),
  cap_2000TXG = results.get('V_CapacityAvailableByPeriodAndTech(2000,TXG)', 0),
  cap_2010TXG = results.get('V_CapacityAvailableByPeriodAndTech(2010,TXG)', 0),
  newcap_1990E01 = results.get('V_Capacity(E01,1990)', 0),
  newcap_2000E01 = results.get('V_Capacity(E01,2000)', 0),
  newcap_2010E01 = results.get('V_Capacity(E01,2010)', 0),
  newcap_1990E21 = results.get('V_Capacity(E21,1990)', 0),
  newcap_2000E21 = results.get('V_Capacity(E21,2000)', 0),
  newcap_2010E21 = results.get('V_Capacity(E21,2010)', 0),
  newcap_1990E31 = results.get('V_Capacity(E31,1990)', 0),
  newcap_2000E31 = results.get('V_Capacity(E31,2000)', 0),
  newcap_2010E31 = results.get('V_Capacity(E31,2010)', 0),
  newcap_1990E51 = results.get('V_Capacity(E51,1990)', 0),
  newcap_2000E51 = results.get('V_Capacity(E51,2000)', 0),
  newcap_2010E51 = results.get('V_Capacity(E51,2010)', 0),
  newcap_1990E70 = results.get('V_Capacity(E70,1990)', 0),
  newcap_2000E70 = results.get('V_Capacity(E70,2000)', 0),
  newcap_2010E70 = results.get('V_Capacity(E70,2010)', 0),
  newcap_1990SRE = results.get('V_Capacity(SRE,1990)', 0),
  newcap_2000SRE = results.get('V_Capacity(SRE,2000)', 0),
  newcap_2010SRE = results.get('V_Capacity(SRE,2010)', 0),
  newcap_1990RHE = results.get('V_Capacity(RHE,1990)', 0),
  newcap_2000RHE = results.get('V_Capacity(RHE,2000)', 0),
  newcap_2010RHE = results.get('V_Capacity(RHE,2010)', 0),
  newcap_1990RHO = results.get('V_Capacity(RHO,1990)', 0),
  newcap_2000RHO = results.get('V_Capacity(RHO,2000)', 0),
  newcap_2010RHO = results.get('V_Capacity(RHO,2010)', 0),
  newcap_1990RL1 = results.get('V_Capacity(RL1,1990)', 0),
  newcap_2000RL1 = results.get('V_Capacity(RL1,2000)', 0),
  newcap_2010RL1 = results.get('V_Capacity(RL1,2010)', 0),
  newcap_1990TXD = results.get('V_Capacity(TXD,1990)', 0),
  newcap_2000TXD = results.get('V_Capacity(TXD,2000)', 0),
  newcap_2010TXD = results.get('V_Capacity(TXD,2010)', 0),
  newcap_1990TXE = results.get('V_Capacity(TXE,1990)', 0),
  newcap_2000TXE = results.get('V_Capacity(TXE,2000)', 0),
  newcap_2010TXE = results.get('V_Capacity(TXE,2010)', 0),
  newcap_1990TXG = results.get('V_Capacity(TXG,1990)', 0),
  newcap_2000TXG = results.get('V_Capacity(TXG,2000)', 0),
  newcap_2010TXG = results.get('V_Capacity(TXG,2010)', 0),
)

cur_dir = os.getcwd()
tmp_dir = mkdtemp( prefix='utopia-20.' )
os.chdir( tmp_dir )

ZipFile(ods_base).extractall()
with open( 'content.xml', 'wb' ) as f:
	f.write( content )
with open( 'styles.xml', 'wb' ) as f:
	f.write( styles )
with open( 'settings.xml', 'wb' ) as f:
	f.write( settings )

with ZipFile( os.path.join(cur_dir, 'utopia-20.ods'), 'w') as f:
	for root, dirs, files in os.walk('.'):
		for name in files:
			f.write( os.path.join(root, name) )

os.chdir( cur_dir )
shutil.rmtree( tmp_dir )
print "Successfully wrote 'utopia-20.ods'"

# import IPython
# IPython.embed()

# msg = """\
# Objective Value:,,36821,,=I1-C1,(Difference),,%(obj_name)s,%(obj_value).0f
#
# From TABLE04 (Energy Output of Each Supply Technology at Gate)
# ,,1990,2000,2010,,,Non-zero variable values:,1990,2000,2010
# E01,ELC,4.7,7.62,12.15,,,V_ActivityByPeriodAndTech[E01],%(act_1990E01).2f,%(act_2000E01).2f,%(act_2010E01).2f
# E31,ELC,1.13,1.13,1.13,,,V_ActivityByPeriodAndTech[E31],%(act_1990E31).2f,%(act_2000E31).2f,%(act_2010E31).2f
# E51,ELC,0.59,0.89,1.23,,,V_ActivityByPeriodAndTech[E51],%(act_1990E51).2f,%(act_2000E51).2f,%(act_2010E51).2f
# E70,ELC,0,0,0,,,V_ActivityByPeriodAndTech[E70],%(act_1990E70).2f,%(act_2000E70).2f,%(act_2010E70).2f
# ,,=SUM(C5:C8),=SUM(D5:D8),=SUM(E5:E8),,,,=SUM(I5:I8),=SUM(J5:J8),=SUM(K5:K8)
#
# From TABLE06 (useful energy output from demand devices)
# ,,1990,2000,2010,,,,1990,2000,2010
# RHO,RH,25.2,37.8,56.7             ,,,V_ActivityByPeriodAndTech[RHO],%(act_1990RHO).2f,%(act_2000RHO).2f,%(act_2010RHO).2f
# RL1,RL,5.6,8.4,12.6               ,,,V_ActivityByPeriodAndTech[RL1],%(act_1990RL1).2f,%(act_2000RL1).2f,%(act_2010RL1).2f
# TXD,TX,0.6,1.76,4.76              ,,,V_ActivityByPeriodAndTech[TXD],%(act_1990TXD).2f,%(act_2000TXD).2f,%(act_2010TXD).2f
# TXG,TX,4.6,6.04,6.93              ,,,V_ActivityByPeriodAndTech[TXG],%(act_1990TXG).2f,%(act_2000TXG).2f,%(act_2010TXG).2f
# ,,=SUM(C13:C16),=SUM(D13:D16),=SUM(E13:E16),,,,=SUM(I13:I16),=SUM(J13:J16),=SUM(K13:K16)
#
# Installed Capacity (CAP.C),,,,,,,,1990,2000,2010
# E01,0.5,0.38,0.6,,,,V_CapacityAvailableByPeriodAndTech[E01],%(cap_1990E01).2f,%(cap_1990E01).2f,%(cap_1990E01).2f
# E31,0.13,0.13,0.13,,,,V_CapacityAvailableByPeriodAndTech[E31],%(cap_1990E31).2f,%(cap_2000E31).2f,%(cap_2010E31).2f
# E51,0.5,0.5,0.5,,,,V_CapacityAvailableByPeriodAndTech[E51],%(cap_1990E51).2f,%(cap_2000E51).2f,%(cap_2010E51).2f
# E70,0.3,0.25,0.2,,,,V_CapacityAvailableByPeriodAndTech[E70],%(cap_1990E70).2f,%(cap_2000E70).2f,%(cap_2010E70).2f
# SRE,0.1,0.1,0.1,,,,V_CapacityAvailableByPeriodAndTech[SRE],%(cap_1990SRE).2f,%(cap_2000SRE).2f,%(cap_2010SRE).2f
# RHE,0,0,0,,,,V_CapacityAvailableByPeriodAndTech[RHE],%(cap_1990RHE).2f,%(cap_2000RHE).2f,%(cap_2010RHE).2f
# RHO,25.2,37.8,56.7,,,,V_CapacityAvailableByPeriodAndTech[RHO],%(cap_1990RHO).2f,%(cap_2000RHO).2f,%(cap_2010RHO).2f
# RL1,5.6,8.4,12.6,,,,V_CapacityAvailableByPeriodAndTech[RL1],%(cap_1990RL1).2f,%(cap_2000RL1).2f,%(cap_2010RL1).2f
# TXD,0.6,1.76,4.76,,,,V_CapacityAvailableByPeriodAndTech[TXD],%(cap_1990TXD).2f,%(cap_2000TXD).2f,%(cap_2010TXD).2f
# TXE,0,0,0,,,,V_CapacityAvailableByPeriodAndTech[TXE],%(cap_1990TXE).2f,%(cap_2000TXE).2f,%(cap_2010TXE).2f
# TXG,4.6,6.04,6.93,,,,V_CapacityAvailableByPeriodAndTech[TXG],%(cap_1990TXG).2f,%(cap_2000TXG).2f,%(cap_2010TXG).2f
#
# Resource Supply (SUPPLY.SEP),,,,,,,,1990,2000,2010
# IMPDSL1,38.6,61.6,101.59,,,,V_ActivityByPeriodAndTech[IMPDSL1],%(act_1990IMPDSL1).2f,%(act_2000IMPDSL1).2f,%(act_2010IMPDSL1).2f
# IMPGSL1,19.91,26.16,30.02,,,,V_ActivityByPeriodAndTech[IMPGSL1],%(act_1990IMPGSL1).2f,%(act_2000IMPGSL1).2f,%(act_2010IMPGSL1).2f
# IMPHCO1,14.7,23.8,37.97,,,,V_ActivityByPeriodAndTech[IMPHCo1],%(act_1990IMPHCO1).2f,%(act_2000IMPHCO1).2f,%(act_2010IMPHCO1).2f
# ,=SUM(B33:B35),=SUM(C33:C35),=SUM(D33:D35),,,,,=SUM(I33:I35),=SUM(J33:J35),=SUM(K33:K35)
# """
