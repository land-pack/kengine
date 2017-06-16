import sys

sys.path.append("..")

from kengine.ws import KWebSocketHandler
import redis
from tornado import ioloop
from tornado.options import options, define
from tornado import web


r = redis.Redis("192.168.41.76", 6379)
define("port", default=8109, help="Default port", type=int)
node_id = "127.0.0.1:{}".format(options.port)



r = redis.Redis("127.0.0.1")

node = '127.0.0.1:8000'


class MyWebSocketHandler(KWebSocketHandler):
    def __init__(self, *args, **kwargs):
        self.r = r
        self.node = node
        super(MyWebSocketHandler, self).__init__(*args, **kwargs)

if __name__ == '__main__':
    options.parse_command_line()
    application = web.Application([
        (r'/ws', MyWebSocketHandler),
    ],
        debug=True)
    application.listen(options.port)
    print 'Listen on ', options.port
    r.lpush("NODE_HOST_LIST", "127.0.0.1:{}".format(options.port))
    node_id = "127.0.0.1:{}".format(options.port)
    r.set(node_id, 0)
    ioloop.IOLoop.instance().start()
