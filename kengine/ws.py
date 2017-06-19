import atexit
from handler import HandlerManager
from tornado.websocket import WebSocketHandler

_clean_node_information_callback_register_flag = 0


class KWebSocketHandler(WebSocketHandler):
    r = None
    node = None

    def __init__(self, *args, **kwargs):
        global _clean_node_information_callback_register_flag
        if _clean_node_information_callback_register_flag == 0:
            atexit.register(self.remove_node_from_host_list)
            _clean_node_information_callback_register_flag = 1
        super(KWebSocketHandler, self).__init__(*args, **kwargs)

    def prepare(self):
        [setattr(self, '{}'.format(k), v[0])
         for k, v in self.request.arguments.iteritems()]

    def check_origin(self, origin):
        return True

    def open(self):
        self.r.incr(self.node)
        HandlerManager.add_handler(self)

    def on_message(self, msg):
        data = HandlerManager.route_message(self, msg)
        if data != '{}':
            self.write_message(data)

    def on_close(self):
        self.r.decr(self.node)
        HandlerManager.del_handler(self)

    def remove_node_from_host_list(self):
        self.r.delete(self.node)
        self.r.lrem("NODE_HOST_LIST", self.node)

    def pre_close(self, code, reason='connection expire ~'):
        """
        You should override this! if you want to have some tips before shutdown
        the websocket connection ~
        """
        self.close(1000, reason)
