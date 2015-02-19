import datetime
import tornado.websocket

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    Token = ""
    TimeoutEvent = None
    Connected = False
    
    def check_origin(self, origin):
        return True

    def wsinit(self):
        self.Connected = True
        
        self.application.ClientPool[self.Token].append(self)
        
        def timeout():
            self.unregister()
        self.TimeoutEvent = tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds = self.application.ClientTimeout), timeout)
    
    # If Tornado version < 4.x, we have to initialize in open()
    def open(self):
        if(tornado.version_info[0] < 4):
            self.Token = self.get_argument('token')
        
            self.add_header('X-Powered-By', 'Tornado/' + tornado.version)

            if self.Token not in self.application.ClientPool.keys():
                self.close()
                return

            self.wsinit()

    # After tornado 4.x, hand shaking will handled by get().
    # We can return status code before hand shaking. After that set_status() will be disabled.
    # NOTE: Before tornado 4.x, get() will never be called.
    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        if(tornado.version_info[0] >= 4):
            self.Token = self.get_argument('token')
        
            self.add_header('X-Powered-By', 'Tornado/' + tornado.version)

            if self.Token not in self.application.ClientPool.keys():
                self.set_status(401)
                self.finish()
                return

            tornado.websocket.WebSocketHandler.get(self, *args, **kwargs)

            self.wsinit()
        else:
            tornado.websocket.WebSocketHandler.get(self, *args, **kwargs)

    def push(self, message):
        self.write_message(message)

    def on_message(self, message):
        pass

    def on_close(self):
        self.unregister()

    def unregister(self):
        if self.Connected:
            self.application.ClientPool[self.Token].remove(self)
            tornado.ioloop.IOLoop.instance().remove_timeout(self.TimeoutEvent)