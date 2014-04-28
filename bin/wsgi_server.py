from router import Router
from wsgi_app import Wsgi_Apps
import ConfigParser
config = ConfigParser.ConfigParser()
config.readfp(open('../conf/sc.conf',"rb"))
router = Router(config)
wsgi_app = Wsgi_Apps(config)
wsgi_app.init_router(router)
HOST = ''
PORT = 8089

if __name__ == "__main__":
#	from wsgiref.simple_server import make_server
	from eventlet import api,wsgi
	print 'Starting up HTTP server on %s: %i..........' %(HOST,PORT)
	wsgi.server(api.tcp_listener((HOST,PORT)),router)
#	server.handle_request()

