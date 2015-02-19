import datetime
import tornado.web

class CometHandler(tornado.web.RequestHandler):
    Token = ""
    TimeoutEvent = None
    Connected = True
    
    @tornado.web.asynchronous
    def get(self):
        self.handle()
        
    @tornado.web.asynchronous
    def post(self):
        self.handle()

    def handle(self):
        self.Connected = True

        self.set_header('Content-Type', 'text/html; charset=' + self.application.CharSet);
        self.add_header('X-Powered-By', 'Tornado/' + tornado.version)

        self.Token = self.get_argument('token')
        if self.Token not in self.application.ClientPool.keys():
            self.set_status(401)
            self.finish()
            return

        self.set_header('Transfer-Encoding', 'chunked');
        
        self.application.ClientPool[self.Token].append(self)
        
        def timeout():
            self.unregister()
        self.TimeoutEvent = tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds = self.application.ClientTimeout), timeout)

    def push(self, message):
        # Calculate data length
        length = len(message)
        self.write(format(length, 'X') + "\r\n" + message + "\r\n") 
        self.flush()

    def on_connection_close(self):
        self.Connected = False
        self.unregister()

    def unregister(self):
        if(self.Connected):
            self.write("0\r\n\r\n")
            self.finish()
        self.application.ClientPool[self.Token].remove(self)
        tornado.ioloop.IOLoop.instance().remove_timeout(self.TimeoutEvent)