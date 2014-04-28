#!/bin/python
class SCException(Exception):
	def __init__(self):
		Exception.__init__(self)
		self.errorcode='600'
		self.errorinfo='ERROR'

class ErrorURLException(SCException):
	def __init__(self):
		SCException.__init__(self)	
		self.errorcode='601'
		self.errorinfo='ERROR URL'

	def errorhandler(self):
		return self.errorinfo
		
class NoPageException(SCException):
	def __init__(self):
		SCException.__init__(self)
		self.errorcode='602'
		self.errorinfo=open('../page/errorpage.html').read()
	def errorhandler(self):
		return self.errorinfo
class NoExcutorException(SCException):
	def __init__(self):
		SCException.__init__(self)
		self.errorcode='603'
		self.errorinfo="No Excutor!"
	def errorhandler(self):
		return self.errorinfo
def errorpagehandler():
		xhtml=open('../page/errorpage.html').read()
		return xhtml

def errorurlhandler():
		return "ERROR URL"
