import sys
sys.path.append("..")

import unittest
from kengine.handler import HandlerManager, FakeWS

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
		for i in xrange(8):
			ws = FakeWS()
			ws.uid = '1000{}'.format(i)
			HandlerManager.add_handler(ws)
		self.assertEqual(len(HandlerManager.uid_to_handler), 8)
		self.assertEqual(len(HandlerManager.room_to_uids[1]), 8)
		self.assertEqual(HandlerManager.room_uuid_index, 1)

		for i in xrange(8):
			ws = FakeWS()
			ws.uid = '2000{}'.format(i)
			HandlerManager.add_handler(ws)
		self.assertEqual(len(HandlerManager.uid_to_handler), 16)
		self.assertEqual(len(HandlerManager.room_to_uids[1]), 9)
		self.assertEqual(HandlerManager.room_uuid_index, 2)

		handler_for_uid_10001 = HandlerManager.uid_to_handler.get("10001")
		handler_for_uid_10002 = HandlerManager.uid_to_handler.get("10002")
		handler_for_uid_10003 = HandlerManager.uid_to_handler.get("10003")
		handler_for_uid_10004 = HandlerManager.uid_to_handler.get("10004")

		HandlerManager.del_handler(handler_for_uid_10001)
		HandlerManager.del_handler(handler_for_uid_10002)
		HandlerManager.del_handler(handler_for_uid_10003)
		HandlerManager.del_handler(handler_for_uid_10004)

		self.assertEqual(len(HandlerManager.uid_to_handler), 12)
		self.assertEqual(len(HandlerManager.room_to_uids[1]), 5)
		self.assertEqual(len(HandlerManager.room_to_uids[2]), 7)
		self.assertEqual(HandlerManager.room_uuid_index, 2)

		# now if i add new handler, should come in the room 2
		ws2 = FakeWS()
		ws2.uid = '30001'
		HandlerManager.add_handler(ws2)
		self.assertEqual(len(HandlerManager.uid_to_handler), 13)
		self.assertEqual(len(HandlerManager.room_to_uids[1]), 5)
		self.assertEqual(len(HandlerManager.room_to_uids[2]), 8)
		self.assertEqual(HandlerManager.room_uuid_index, 2)




if __name__ == '__main__':
	unittest.main()

