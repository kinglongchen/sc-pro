from dispatcher import Dispatcher

dispatcher = Dispatcher()
dispatcher.add(r'^/$', 'views.uplaod_page')
dispatcher.add(r'^/upload_service$', 'views.upload_service')
dispatcher.add(r'^/uploadfile$', 'views.upload_handling')
HOST = '172.31.214.119'
PORT = 8089

if __name__ == "__main__": 
    from wsgiref.simple_server import make_server
    server = make_server(HOST, PORT, dispatcher)
    print 'Starting up HTTP server on %s: %i..........' %(HOST,PORT)
#    server.serve_forever()
    server.handle_request()

