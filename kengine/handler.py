import traceback
from collections import defaultdict
from concurrent import futures
import ujson

thread_executor = futures.ThreadPoolExecutor(max_workers=50)


class HandlerManager(object):
    uid_to_handler = {}
    room_to_uids = defaultdict(set)
    room_uuid_index = 0
    max_room_size = 9
    heart_beat = 'p'
    after_open_plugin_func = []
    after_close_plugin_func = []
    method_to_func = {}  # method hash to a function(handler, ws)
    when_ping_coming = {}

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
    def after_open(cls, func):
        cls.after_open_plugin_func.append(func)

    @classmethod
    def after_close(cls, func):
        cls.after_close_plugin_func.append(func)

    @classmethod
    def exec_after_open_plugin(cls, handler):
        for i in cls.after_open_plugin_func:
            i(cls, handler)

    @classmethod
    def exec_after_close_plugin(cls, handler):
        for i in cls.after_close_plugin_func:
            i(cls, handler)

    @classmethod
    def add_handler(cls, handler):
        target_room = cls._dispatcher_strategy()
        setattr(handler, 'room', target_room)
        cls.room_to_uids[target_room].add(handler.uid)
        cls.uid_to_handler[handler.uid] = handler
        cls.exec_after_open_plugin(handler)

    @classmethod
    def del_handler(cls, handler):
        cls.exec_after_close_plugin(handler)
        cls.room_to_uids[handler.room].remove(handler.uid)
        del cls.uid_to_handler[handler.uid]

    @classmethod
    def when_ping(cls, f):
        """
        Usage: the same to `fun_for`
        """
        cls.when_ping_coming[f.func_name] = f
        def wrapper(*args, **kwargs):
            return
        return wrapper

    @classmethod
    def run_for(cls, f):
        """
        @HandlerManager.run_for
        def chat(handler, ws):
            pass
        """
        cls.method_to_func[f.func_name] = f
        def wrapper(*args, **kwargs):
            return
        return wrapper

    @classmethod
    def exec_method_event(cls, request_method, ws):
        """
        call by MessageManager
        """
        f = cls.method_to_func[request_method]
        f(cls, ws)

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
                        "method": "chat",
                        "message":{
                        "uid": "1001",
                        "room": "1"
                    }
                }'
        """
        message = str(message)
        if message == cls.heart_beat:
            for f_name, f_obj in cls.when_ping_coming.items():
                f_obj(cls, handler)
            return 'q'
        else:
            try:
                data = ujson.loads(message)
                response = cls.message_manager.rpc(cls, handler, data) or {}
                data = ujson.dumps(response)
            except Exception as ex:
                print(traceback.format_exc())
                return
            return data

    @classmethod
    def send_message(cls, handler, message):
        try:
            thread_executor.submit(handler.write_message, ujson.dumps(message))
        except:
            print(".....error")

    @classmethod
    def broadcast_on_room(cls, room, message, ignore=[], care=[]):
        uids = cls.room_to_uids[room]
        care = care if care else uids
        uids = set(uids) - set(ignore) & set(care)
        for uid in uids:
            handler = cls.uid_to_handler[uid]
            cls.send_message(handler, message)

    @classmethod
    def broadcast_on_all(cls, message):
        for handler in cls.uid_to_handler.values():
            cls.send_message(handler, message)
