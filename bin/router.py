#!/bin/python
class Router(object):
	def __init__(self,config):
		self.path_info = {}
		self.config = config
	def add_route(self, path): 
		def wrapper(application): 
			self.path_info[path] = application 
		return wrapper
	def __call__(self, environ, start_response):
	#***************************************************
		self.config.readfp(open('../conf/sc.conf',"rb"))
		if environ['PATH_INFO'].split('/')[-1].split('.')[-1]=='app':
			application = self.path_info['fileupload']
		elif environ['PATH_INFO'].split('/')[-1].split('.')[-1] in self.config.get("REQTYPE","conreq").split(','): 
			application = self.path_info['con_req']
		else:
			application = self.path_info['hd_req']
		return application(environ, start_response) 
