import json
import tornado.web

class SendHandler(tornado.web.RequestHandler):
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
        
        if(self.application.check_host(host_id, host_pass) == False):
            self.write(json.dumps({'success' : False, 'error' : 'Invalid host id and password'}))
            return
        
        message = self.get_argument('message')
        batch = self.get_argument('batch', 'false')
        client_id_string = self.get_argument('client_id')

        if batch.lower() == 'true':
            client_ids = json.loads(client_id_string)
        else:
            client_ids = [client_id_string]
        
        for client_id in client_ids:
            client_id = str(client_id)
            if client_id not in self.application.ClientTokens[host_id].keys():
                self.write(json.dumps({'success' : False, 'error' : 'Client ID ' + client_id + ' doen not have a token.'}))
                return
            token = self.application.ClientTokens[host_id][client_id]
        
            for client in self.application.ClientPool[token]:
                client.push(message)
        
        self.write(json.dumps({'success' : True}))