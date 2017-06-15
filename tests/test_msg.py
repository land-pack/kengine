import sys
sys.path.append("..")

import unittest
from kengine.msg import MessageManager, BaseDispatcher


class MyDispatcher(BaseDispatcher):

    def get_matches(self, handler, message):
        pass

    def chat(self, handler,  message):
        return 'chat_ok'

    def recovery(self, handler, message):
        pass


class TestMessageManager(unittest.TestCase):

    def setUp(self):
        pass

    def test_01_message_manage(self):
        my_dispatcher = MyDispatcher()
        message_manager = MessageManager(my_dispatcher)
        d1 = {
            "method": "chat",
            "biz_content": "hello world"
        }
        resp = message_manager.rpc(None, d1)
        self.assertEqual(resp, 'chat_ok')


if __name__ == '__main__':
    unittest.main()
