import sys
sys.path.append("..")

import unittest
from kengine.dispatcher import HandlerManager, FakeWS

class DispatcherTest(unittest.TestCase):

	def setUp(self):
		pass

	def test_01_add_handler(self):
		ws = FakeWS()
		ws.uid = '10001'
		HandlerManager.add_handler(ws)
		self.assertEqual(len(HandlerManager.uid_to_handler), 1)

	def test_02_del_handler(self):
		ws1 = FakeWS()
		ws1.uid = '10002'
		HandlerManager.add_handler(ws1)
		self.assertEqual(len(HandlerManager.uid_to_handler), 2),
		HandlerManager.del_handler(ws1)
		self.assertEqual(len(HandlerManager.uid_to_handler), 1)

	def test_03_reset(self):
		self.assertEqual(len(HandlerManager.uid_to_handler), 1)
		self.assertEqual(len(HandlerManager.room_to_uids[1]), 1)
		self.assertEqual(HandlerManager.room_uuid_index, 1)
		HandlerManager.reset()
		self.assertEqual(len(HandlerManager.uid_to_handler), 0)
		self.assertEqual(len(HandlerManager.room_to_uids), 0)
		self.assertEqual(HandlerManager.room_uuid_index, 0)

	def test_04_dispatcher_strategy(self):
		HandlerManager.reset()


if __name__ == '__main__':
	unittest.main()

