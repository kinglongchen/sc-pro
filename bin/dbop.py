#!/usr/bin/python
#Filename: mysql.py

import MySQLdb
import os, sys

class Mysql(object):
	def __init__(self):
		self.conn = ''
		self.cursor  = ''
	def connect(self, host='localhost', usr='root', passwd='12345', db='sc', charset='utf8'):
		try:
			self.conn = MySQLdb.connect(host, usr, passwd, db)
		except Exception, e:
			print e
			sys.exit()
		self.cursor = self.conn.cursor()
	def insertMysql(self, sql):
		self.cursor.execute(sql)
		self.conn.commit()
	def query(self,sql):
		return self.cursor.execute(sql)
	def show(self):
		data=self.cursor.fetchall()
		for x in data:
			print x
	def get_nsid(self,sid):
		sql='select nsid from sct where sid=' + str(sid)
		self.cursor.execute(sql)
		data=self.cursor.fetchall()
		for x in data:
			return x
	def get_nsurl(self,sid):
		sql='select nsurl from sct where sid='+str(sid)
		self.cursor.execute(sql)
		data=self.cursor.fetchall()
		for x in data:
			return x
	def getvm_ip(self,vm_id):
		sql = 'select vm_ip from vmtb where vm_id='+vm_id
		self.cursor.execute(sql)
		data = self.cursor.fetchall()
		return data[0][0]
	def insertsvtb(self,svname,user_id,sv_ip,sv_port,sv_url):
		sql = 'insert into svtb(sv_name,user_id,sv_ip,sv_port,sv_url) values ("'+svname+'","'+user_id+'","'+sv_ip+'","'+sv_port+'","'+sv_url+'");'
		#print sql
		self.cursor.execute(sql)
		self.conn.commit()
	def close(self):
		self.cursor.close()
		self.conn.close()
