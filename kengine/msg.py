class BaseDispatcher(object):
    def _to_dict(self, messageid, messagetype, message):
        d = {
            "messageid": messageid,
            "messagetype": messagetype,
            "body": message
        }
        return d

    def render(self, messageid, messagetype, message):
        pass

    def default(self, handler, message):
        response = self._to_dict(4004, 'no found', {})
        return response


class MessageManager(object):
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def rpc(self, handler, ws, message):
        request_type = message.get("method")
        try:
            response = getattr(self.dispatcher, request_type, getattr(
                self.dispatcher, "default"))(handler, ws, message)
        except Exception as ex:
            raise
        else:
            return response
