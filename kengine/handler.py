from collections import defaultdict
from concurrent import futures
from ttl import TTLManager
from msg import MessageManager

thread_executor = futures.ThreadPoolExecutor(max_workers=50)
ttl_hb = TTLManager(timeout=150, ttl_type='ping', detail=True)
ttl_hb.start()

message_manager = MessageManager(None)


class HandlerManager(object):

    uid_to_handler = {}
    room_to_uids = defaultdict(set)
    room_uuid_index = 0
    max_room_size = 9
    heart_beat = 'p'

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
    def reset(cls, max_room_size=9, heart_beat='p'):
        cls.room_uuid_index = 0
        del cls.room_to_uids
        cls.room_to_uids = defaultdict(set)
        del cls.uid_to_handler
        cls.uid_to_handler = {}
        cls.max_room_size = max_room_size
        cls.heart_beat = heart_beat

    @classmethod
    def route_message(cls, handler, message):
        """
        client mssage can be two structure !
        example 1 (heart beat)
                'p'
        example 2 (stanard message)
                '{
	                "method": "recovery",
	                "platform": "fedora",
	                "version": "v1.1.1",
	                "channel": "websocket",
                    "biz_content":{
                        "uid": "1002922",
                        "roomid": "101"
                    }
                }'
        """
        if message == cls.heart_beat:
            return 'q'
        else:
            try:
                data = ujson.loads(message)
                response = message_manager.rpc(cls, data)
                data = ujson.dumps(response)
            except:
                # print log
                return
            return data

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
