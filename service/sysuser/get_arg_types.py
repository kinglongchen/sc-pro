#!/bin/python
'''
return the args type information as xml format:
for example:
<argtypes>
	<types>
		<id></id>
		<name></name>
	</types>
	<types>...</types>
	.
	.
	.
</argtypes>
'''
from dbop import Mysql
types_xml = '<?xml version="1.0" encoding="utf-8"?>\n'
types_xml += '<argtypes>\n'
sql_conn = Mysql()
sql_conn.connect()
data = sql_conn.query("select * from argtypestb")
for x in data:
	types_xml+= '<types>\n'
	types_xml+= '<id>'+str(x[0])+'</id>\n'
	types_xml+= '<name>'+str(x[1])+'</name>\n'
	types_xml+= '</types>\n'
types_xml+='</argtypes>'
sql_conn.close()
print types_xml
