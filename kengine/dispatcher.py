from collections import defaultdict
from concurrent import futures

thread_executor = futures.ThreadPoolExecutor(max_workers=50)


class HandlerManager(object):

    uid_to_handler = {}
    room_to_uids = defaultdict(set)
    room_uuid_index = 0
    max_room_size = 9

    @classmethod
    def _dispatcher_strategy(cls):
        target_room = None
        room_uids_list = sorted(
            cls.room_to_uids.items(), key=lambda x: len(x[1]), reverse=True)
        for room, uids in room_uids_list:
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

    @classmethod
    def del_handler(cls, handelr):
        cls.room_to_uids[handelr.room].remove(handelr.uid)
        del cls.uid_to_handler[handelr.uid]

    @classmethod
    def reset(cls, max_room_size=9):
        cls.room_uuid_index = 0
        del cls.room_to_uids
        cls.room_to_uids = defaultdict(set)
        del cls.uid_to_handler
        cls.uid_to_handler = {}
        cls.max_room_size = max_room_size

    @classmethod
    def dispatch_message(cls, handler, message):
        pass

    @classmethod
    def send_message(cls, handler, message):
        try:
            thread_executor.submit(handler.write_message, ujson.dumps(message))
        except:
            print(".....error")

    @classmethod
    def broadcast_on_room(cls, room, message, ignore=[]):
        uids = cls.room_to_uids[room]
        for uid in uids:
            if uid in ignore:
                continue
            handler = cls.uid_to_handler[uid]
            cls.send_message(handler, message)

    @classmethod
    def broadcast_on_all(cls, message):
        for handler in cls.uid_to_handler.values():
            cls.send_message(handler, message)


class FakeWS(object):
    pass
