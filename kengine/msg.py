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

    def rpc(self, handler, message):
        request_type = message.get("method")
        try:
            response = getattr(self.dispatcher, request_type, getattr(
                self.dispatcher, "default"))(handler, message)
        except Exception as ex:
            raise
        else:
            return response




if __name__ == '__main__':
	my_dispatcher = MyDispatcher()
	message_manager = MessageManager(my_dispatcher)
	d1 = {
		"method": "chat",
		"biz_content": "hello world"
	}
	message_manager.rpc(None, d1)

