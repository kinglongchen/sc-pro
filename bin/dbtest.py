#!/bin/python
from dbop import Mysql
conn = Mysql()
conn.connect()
conn.insertsvtb('sv1','2','192.168.1.1','8090','http://asdfasdfasd')
