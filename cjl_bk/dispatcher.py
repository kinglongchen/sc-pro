import re

class Dispatcher(object):
    def __init__(self, handle404 = None):
        self.urls = dict()
        self.request_path = ''
        if handle404:
            self.handle404 = handle404
        else:
            self.handle404 = self._404

    def __call__(self, environ, start_response):
        self.request_path = environ.get('PATH_INFO', '')
        for url in self.urls:            
            regex = re.compile(url)
            if regex.match(self.request_path):
                m = regex.match(self.request_path)                        
                mod_name, func_name = self._get_mod_func(self.urls[url])                
                try:
                    callback = getattr(__import__(mod_name, {}, {}, ['']), func_name)
                except ImportError, e:
                    raise Exception, "Could not import %s. Error was: %s" % (mod_name, str(e))
                except AttributeError, e:
                    raise Exception, "Tried %s in module %s. Error was: %s" % (func_name, mod_name, str(e))                
                args = (environ, start_response)
                kwargs = dict()                
                for i in regex.groupindex:
                    kwargs[i] = m.group(i)
                # Run callback with environ, start_response and args
                return callback(*args, **kwargs)
        # No match with the defined urls
        return self.handle404(environ, start_response)
            
    def _get_mod_func(self, callback):
        """
        Converts 'path.to.module.funtion' to ['path.to.module', 'function']
        """
        try:
            d = callback.rindex('.')
        except ValueError:
            return callback, ''
        return callback[:d], callback[d+1:]
    
    def _404(self, environ, start_response):
        start_response("404 Not Found", [('content-type', 'text/html')])
        return ['Not Found']

    def add(self, regex, handler):
        self.urls[regex] = handler

