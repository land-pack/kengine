from collections import defaultdict

class HandlerManager(object):

	uid_to_handler = {}
	room_to_uids = defaultdict(set)
	room_uuid_index = 0
	max_room_size = 9

	@classmethod
	def _dispatcher_strategy(cls):
		target_room = None
		sorted(cls.room_to_uids.items(), key=lambda x: len(x[1]), reverse=True)
		for room, uids in cls.room_to_uids.items():
			if len(uids) < cls.max_room_size:
				target_room = room
				break

		if not target_room:
			cls.room_uuid_index = cls.room_uuid_index + 1
			target_room = cls.room_uuid_index
		return target_room

	@classmethod
	def add_handler(cls, handler):
		target_room = cls._dispatcher_strategy()
		setattr(handler, 'room', target_room)
		cls.room_to_uids[target_room].add(handler.uid)
		cls.uid_to_handler[handler.uid] = handler
		print("target_room >>%s" % target_room)

	@classmethod
	def del_handler(cls, handelr):
		cls.room_to_uids[handelr.room].remove(handelr.uid)
		del cls.uid_to_handler[handelr.uid]

	@classmethod
	def dispatch_message(cls, handler, message):
		pass

	@classmethod
	def do_echo(cls, handler, message):
		pass

	@classmethod
	def do_broadcast(cls, message):
		pass

class WS(object):
	pass 

if __name__ == '__main__':

	# for i in xrange(100):
	# 	ws = WS()
	# 	ws.uid = '1000{}'.format(i)
	# 	HandlerManager.add_handler(ws)
	ws1 = WS()
	ws1.uid = 12345
	HandlerManager.add_handler(ws1)
	print(HandlerManager.room_to_uids)
	HandlerManager.del_handler(ws1)
	print(HandlerManager.room_to_uids)


