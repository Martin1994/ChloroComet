import json
import tornado.web

class DebugHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.set_header("Cache-control", "no-store, no-cache, must-revalidate, max-age=0")
        self.add_header('X-Powered-By', 'Tornado/' + tornado.version)
        self.set_header('Content-Type', 'application/json; charset=' + self.application.CharSet);
        client_number = {}
        for token in self.application.ClientPool:
            client_number[token] = len(self.application.ClientPool[token])
        self.write(json.dumps({'hosts' : self.application.Hosts, 'tokens' : self.application.ClientTokens, 'clients' : client_number}, indent = 4))