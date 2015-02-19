import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

import martincl2.ChloroComet

if __name__ == "__main__":
    define("hostid", default="chlorocomet", help="Your host identifier")
    define("hostpass", default="chlorocomet", help="Your host password")
    define("port", default="85", help="Port to listen")

    tornado.options.parse_command_line()

    app = martincl2.ChloroComet.KernelApplication(hosts = {options.hostid : options.hostpass});
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(int(float(options.port)))
    tornado.ioloop.IOLoop.instance().start()