import hashlib
import datetime
import json
import time
import tornado.web

class AddClientHandler(tornado.web.RequestHandler):

    def get(self):
        self.handle()
    
    def post(self):
        self.handle()

    def handle(self):
        self.set_header("Cache-control", "no-store, no-cache, must-revalidate, max-age=0")
        self.set_header('Content-Type', 'application/json; charset=' + self.application.CharSet);

        host_id = self.get_argument('id')
        host_pass = self.get_argument('pass')
        client_id = self.get_argument('client_id')
        
        if(self.application.check_host(host_id, host_pass) == False):
            self.write(json.dumps({'success' : False, 'error' : 'Invalid host id and password'}))
            return
        
        if client_id in self.application.ClientTokens[host_id].keys():
            self.write(json.dumps({'success' : False, 'error' : 'ID exists.'}))
            return
        
        m = hashlib.sha1()
        m.update(host_id)
        m.update("|")
        m.update(client_id)
        m.update("|")
        m.update(str(time.time()))
        token = m.hexdigest()
        
        # TODO: may have a collision
        self.application.add_client(host_id, client_id, token)
        
        self.write(json.dumps({'success' : True, 'token' : token}))
