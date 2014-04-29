#!usr/bin/env python
from exception.excp_mod import *
from excu_midw_mod import extor_parser 
import os
import copy
import re
import cgi
import io
from dbop import Mysql
from fileupload import FileUpload
from MultiPartEncode import MultiPartEncode
#test mod

####################
status = '200 OK' # HTTP Status  
headers = [('Content-type', 'text/html')] # HTTP Headers
class Wsgi_Apps(object):
	def __init__(self,config):
		self.config = config
		self.mysql=Mysql()
		self.fileupload = FileUpload()
		self.multipartencode = MultiPartEncode()
	def init_router(self,router):
		@router.add_route('con_req')
		def con_response(environ, start_response):
			start_response(status, headers)
			try:
				file_path= self.get_file_path(environ['PATH_INFO'])
			except SCException,e:
				return e.errorhandler()
			try:
				xhtml=open('../'+file_path).read()
			except IOError:
				#xhtml = open ('../page/errorpage.html').read()
				xhtml = errorpagehandler()
			return xhtml
		@router.add_route('hd_req')
		def hd_response(environ, start_response):
			#response_headers=copy.deepcopy(headers)
			response_headers = [('Content-type', 'text/xml')]
			response_headers.append(('Cache-Control','no-cache, must-revalidate'))
			response_headers.append(('Expires','Mon, 26 Jul 1997 05:00:00 GMT'))
			try:
				svf_path = self.get_file_path(environ['PATH_INFO'])
				excutor,svp_path= self.excutor_parser(svf_path)
				try:
					request_body_size = int(environ.get('CONTENT_LENGTH',0))
				except ValueError:
					request_body_size=0
				request_body = environ['wsgi.input'].read(request_body_size)
				response_body = os.popen(excutor+' ../'+svp_path+' '+request_body).readlines()
				#response_headers.append(('Content-Length', str(len(response_body))))
			except SCException,e:
				response_body= e.errorhandler()
			except:
				response_body='unkown error'
			#headers.append(('Content-Length', str(len(response_body))))
			#return "the args is:"+request_body
			start_response(status,response_headers)
			return response_body
	#def excute_javaprocess(environ,start_response):
		@router.add_route('fileupload')
		def upload_handling(environ,start_response):
			self.mysql.connect()
			try:
				request_body_size = int(environ.get('CONTENT_LENGTH',0))
			except ValueError:
				request_body_size=0
			fileds=cgi.FieldStorage(environ["wsgi.input"],environ=environ)
			svname = fileds['svname'].value
			vm_id = fileds['vm_id'].value
			vm_ip = self.mysql.getvm_ip(vm_id);
			sv_port = '8089'
			user_id = '2'
			sv_id = self.mysql.insertsvtb(svname,user_id,vm_ip,sv_port)
			sv_name = sv_id+"."+fileds['svfile'].filename.split('.')[-1].strip()
			sv_url = 'http://'+vm_ip+":8089/service/demouser/pro/"+sv_name
			self.mysql.updatesv_url(sv_id,sv_url)
			#insert arg table
			arg_num = 1
			arg = "arg"+str(arg_num)
			while arg in fileds:
				self.mysql.insertsvargtb(sv_id,arg_num,fileds[arg].value)
				arg_num+=1
				arg = "arg"+str(arg_num)	

			#insert database for store the infromation of service
			#data = environ["wsgi.input"].read(request_body_size)
			contenttype = environ["CONTENT_TYPE"]
			boundary = contenttype.split(';')[-1].split('=')[-1].strip()
			sv_data = self.multipartencode.encode(sv_name,fileds['svfile'],boundary)
			self.fileupload.upload_file(vm_ip,contenttype,sv_data)
			'''
			f = file("../service/demouser/pro/"+fileds['svfile'].filename,'w')
			f.write(fileds['svfile'].value)
			f.close()
			'''
			self.mysql.close()
			start_response(status, headers)
			return "upload file successfully!!!"
	def get_file_path(self,req_path):
		if '.' not in req_path.split('/')[-1]:
			raise ErrorURLException()
		if req_path[1]=='/' or req_path[1:2]=='..':
			if req_path.split('/')[-1].split('.')[-1] in self.config.get("REQTYPE","conreq").split(','):
				raise NoPageException()
			else:
				raise ErrorURLException()
		return req_path[1:]
	def excutor_parser(self,sv_path):
		extension = sv_path.split('/')[-1].split('.')[-1]
		if extension not in self.config.get("EXECUTOR","extension").split(','):
			raise NoExcutorException()
		excu_and_svre = self.config.get("EXECUTOR",extension).split(',')
		excutor = excu_and_svre[0].strip()
		svre = excu_and_svre[1].strip()
		return excutor,re.findall(svre,sv_path)[0]
