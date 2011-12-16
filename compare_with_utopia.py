#!/usr/bin/env python

from subprocess import call
import sys, os
from sys import stdin as SI, stderr as SE
from cStringIO import StringIO
from zlib import decompress
from base64 import decodestring
from zipfile import ZipFile

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

cmd = ('rm', '-rf', 'ttt')
call( cmd )
os.mkdir( 'ttt' )
os.chdir( 'ttt' )

ZipFile(ods_base).extractall()
with open( 'content.xml', 'w' ) as f:
	f.write( content )
with open( 'styles.xml', 'w' ) as f:
	f.write( styles )
with open( 'settings.xml', 'w' ) as f:
	f.write( settings )

with ZipFile('../utopia.ods', 'w') as f:
	for root, dirs, files in os.walk('.'):
		for name in files:
			f.write( os.path.join(root, name) )

os.chdir( '..' )
print "Successfully wrote 'utopia.ods'"

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
