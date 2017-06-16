import sys
sys.path.append("..")

import unittest
from kengine.msg import MessageManager, BaseDispatcher


class MyDispatcher(BaseDispatcher):

    def get_matches(self, handler, ws,  message):
        pass

    def chat(self, handler, ws, message):
        return 'chat_ok'

    def recovery(self, handler, ws, message):
        pass


class FakeHandlerManager(object):
    pass


class FakeWebsocketHandler(object):
    pass


class TestMessageManager(unittest.TestCase):

    def setUp(self):
        pass

    def test_01_message_manage(self):
        fake_handler_manager = FakeHandlerManager()
        fake_websocket_handler = FakeWebsocketHandler()
        my_dispatcher = MyDispatcher()
        message_manager = MessageManager(my_dispatcher)
        d1 = {
            "method": "chat",
            "biz_content": "hello world"
        }
        resp = message_manager.rpc(
            fake_handler_manager, fake_websocket_handler, d1)
        self.assertEqual(resp, 'chat_ok')


if __name__ == '__main__':
    unittest.main()
