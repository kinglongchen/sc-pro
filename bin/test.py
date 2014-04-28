#!/bin/python
import ConfigParser
import re
config = ConfigParser.ConfigParser()
config.readfp(open('../conf/sc.conf',"rb"))
v=config.get("TEST","v")
print re.findall(v,"ab/c/d.asdf")
