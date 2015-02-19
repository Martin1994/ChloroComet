import os.path
import sys
import tornado.web

import AddClientHandler
import DebugHandler
import CDPortalHandler
import CometHandler
import RemoveClientHandler
import RemoveAllClientsHandler
import SendHandler
import WebSocketHandler

class KernelApplication(tornado.web.Application):
    
    # Stores { id : pass } pair for hosts
    Hosts = {}

    # Stores { id : { client_id : [ token ] } }
    ClientTokens = {}

    # Stores { token : client }
    ClientPool = {}

    # Timeout seconds
    ClientTimeout = 3600

    # Character Set of HTTP Respond
    CharSet = 'utf-8'
    
    def __init__(self, hosts):
        handlers = [(r"/api/addClient", AddClientHandler.AddClientHandler),
                    (r"/api/comet", CometHandler.CometHandler),
                    (r"/api/websocket", WebSocketHandler.WebSocketHandler),
                    (r"/api/send", SendHandler.SendHandler),
                    (r"/api/removeClient", RemoveClientHandler.RemoveClientHandler),
                    (r"/api/removeAllClients", RemoveAllClientsHandler.RemoveAllClientsHandler),
                  # (r"/api/debug", DebugHandler.DebugHandler),
                    (r"/CDPortal.(htm|html|php)", CDPortalHandler.CDPortalHandler),
                    (r"/(.*\.js)", tornado.web.StaticFileHandler, dict(path = os.path.join(sys.path[0], "static")))]
        
        self.Hosts = hosts
        for host_name in hosts:
            self.ClientTokens[host_name] = {}
        
        template_path = os.path.join(sys.path[0], "templates")
        static_path = os.path.join(sys.path[0], "static")

        tornado.web.Application.__init__(self, handlers = handlers, template_path = template_path, static_path = static_path)

    def add_client(self, host_id, client_id, token):
        self.ClientTokens[host_id][client_id] = token
        self.ClientPool[token] = []

    def remove_client(self, host_id, client_id):
        # Disconnect all running clients
        token = self.ClientTokens[host_id][client_id];
        for client in self.ClientPool[token]:
            client.unregister()

        # Delete token
        del self.ClientPool[token]
        del self.ClientTokens[host_id][client_id]

    def check_host(self, host_id, host_pass):
        return host_id in self.Hosts.keys() and self.Hosts[host_id] == host_pass
    