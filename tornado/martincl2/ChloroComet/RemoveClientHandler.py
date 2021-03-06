import json
import tornado.web

class RemoveClientHandler(tornado.web.RequestHandler):
    def get(self):
        self.handle()

    def post(self):
        self.handle()

    def handle(self):
        self.set_header("Cache-control", "no-store, no-cache, must-revalidate, max-age=0")
        self.add_header('X-Powered-By', 'Tornado/' + tornado.version)
        self.set_header('Content-Type', 'application/json; charset=' + self.application.CharSet);

        host_id = self.get_argument('id')
        host_pass = self.get_argument('pass')
        client_id = self.get_argument('client_id')

        if(self.application.check_host(host_id, host_pass) == False):
            self.write(json.dumps({'success' : False, 'error' : 'Invalid host id and password'}))
            return
        
        if client_id not in self.application.ClientTokens[host_id].keys():
            self.write(json.dumps({'success' : False, 'error' : 'ID doesn\'t exist.'}))
            return

        self.application.remove_client(host_id, client_id)

        self.write(json.dumps({'success' : True}))
