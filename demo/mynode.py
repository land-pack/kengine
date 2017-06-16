import sys

sys.path.append("..")

from kengine.ws import KWebSocketHandler
from kengine.handler import HandlerManager
from kengine.msg import MessageManager, BaseDispatcher
import redis
from tornado import ioloop
from tornado.options import options, define
from tornado import web

define("port", default=8000, help="Default port", type=int)
r = redis.Redis("127.0.0.1")

node = '127.0.0.1:8000'


class MyDispatcher(BaseDispatcher):

    def chat(self, handler, ws, message):
        print 'hello', message
        return 'chat ok'


@HandlerManager.run_for
def chat(handler, ws):
    print 'hello i catch a `chat` method, i gotta do something~'

@HandlerManager.when_ping
def pinging(handler, ws):
    print 'i am ping, update my hearbeat of ws'

message_manager = MessageManager(MyDispatcher())
HandlerManager.message_manager = message_manager


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
