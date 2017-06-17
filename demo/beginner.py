import redis
from tornado import ioloop, web
from tornado.options import options, define
from kengine.ws import KWebSocketHandler
from kengine.handler import HandlerManager
from kengine.msg import MessageManager, BaseDispatcher


r = redis.Redis("127.0.0.1")
node = '127.0.0.1:8000'


class MyDispatcher(BaseDispatcher):

    def chat(self, handler, ws, message):
        return 'hey, you said:{}'.format(message)

message_manager = MessageManager(MyDispatcher())
HandlerManager.message_manager = message_manager


class MyWebSocketHandler(KWebSocketHandler):

    def __init__(self, *args, **kwargs):
        self.r = r
        self.node = node
        super(MyWebSocketHandler, self).__init__(*args, **kwargs)

if __name__ == '__main__':
    application = web.Application([
        (r'/ws', MyWebSocketHandler),
    ],
        debug=True)
    application.listen(8000)
    r.lpush("NODE_HOST_LIST", node)
    r.set(node, 0)
    ioloop.IOLoop.instance().start()
