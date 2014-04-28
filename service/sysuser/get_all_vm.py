#!/bin/python
'''
return the args type information as xml format:
for example:
<vms>
	<vm>
		<id></id>
		<name></name>
	</vm>
	<vm>...</vm>
	.
	.
	.
</vms>
'''
from dbop import Mysql
vms_xml = '<?xml version="1.0" encoding="utf-8"?>\n'
vms_xml += '<vms>\n'
sql_conn = Mysql()
sql_conn.connect()
data = sql_conn.query("select * from vmtb")
for x in data:
	vms_xml+= '<vm>\n'
	vms_xml+= '<id>'+str(x[0])+'</id>\n'
	vms_xml+= '<name>'+str(x[1])+'</name>\n'
	vms_xml+= '</vm>\n'
vms_xml+='</vms>'
sql_conn.close()
print vms_xml
