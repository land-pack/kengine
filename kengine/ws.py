import atexit
from handler import HandlerManager
from tornado.websocket import WebSocketHandler

register_flag = 0


class KWebSocketHandler(WebSocketHandler):
    r = None
    node = None

    def __init__(self, *args, **kwargs):
        global register_flag
        if register_flag == 0:
            atexit.register(self.remove_node_from_host_list)
            register_flag = 1
        super(KWebSocketHandler, self).__init__(*args, **kwargs)

    def prepare(self):
        [setattr(self, '{}'.format(k), v[0]) for k, v in self.request.arguments.iteritems()]

    def check_origin(self, origin):
        return True

    def open(self):
        print("open a connection >>%s | node=%s" % (self.r, self.node))
        self.r.incr(self.node)
        print("increase connection number")
        HandlerManager.add_handler(self)

    def on_message(self, msg):
        data = HandlerManager.route_message(self, msg)
        if data:
            self.write_message(data)
        else:
            self.write_message('response by {}:{}'.format(self.node, msg))

    def on_close(self):
        print("close ...")
        self.r.decr(self.node)
        HandlerManager.del_handler(self)

    def remove_node_from_host_list(self):
        self.r.delete(self.node)
        self.r.lrem("NODE_HOST_LIST", self.node)
        print("remove node data successful ~~")
