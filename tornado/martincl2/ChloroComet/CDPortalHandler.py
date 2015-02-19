import tornado.web

class CDPortalHandler(tornado.web.RequestHandler):

    def get(self, ext):
        self.set_header("Cache-control", "no-store, no-cache, must-revalidate, max-age=0")
        self.add_header('X-Powered-By', 'Tornado/' + tornado.version)
        self.set_header('Content-Type', 'text/html; charset=' + self.application.CharSet);

        token = self.get_argument('token')

        self.render('CDPortal.html', token = token)
