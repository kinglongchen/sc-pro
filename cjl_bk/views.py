#!usr/bin/env python
import urllib
import os
import commands
import sys
import cgi
from cgi import parse_qs, escape
from wsgiref.simple_server import make_server

status = '200 OK' # HTTP Status  
headers = [('Content-type', 'text/html')] # HTTP Headers
#xhtml = "this is test!!!"
def uplaod_page(environ, start_response):
    start_response(status, headers)
    xhtml=open('page/service_upload.html').read()
    return xhtml
def upload_service(environ, start_response):
    start_response(status, headers)
    a = "OK!"
    return a
#def excute_javaprocess(environ,start_response):
def upload_handling(environ,start_response):
	wenput=en["wsgi.input"]
	params=cgi.FieldStorage(fp=io.StringIO(winput.read(int(env.get("CONTENT_LENGTH","0"))).decode("ISO-8859-1")),environ=env,keep_blank_values=1)  
	print(params["file"].name)  
	print(params["file"].filename.encode("ISO-8859-1").decode("UTF-8"))  
	print(params["file"].value.encode("ISO-8859-1"))  	
	start_response(status, headers)
	return "upload file successfully!!!"
