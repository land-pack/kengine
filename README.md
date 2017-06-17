# kengine

[![PyPI version](https://badge.fury.io/py/kengine.svg)](https://badge.fury.io/py/kengine)

MMORPG  WebSocket Connection Engine Based On Openresty + Lua + Tornado + Redis

Install
=====

You can easily install by `pip`

    pip install kengine


Beginner
======

	import redis
	from tornado import ioloop, web
	from tornado.options import options, define
	from kengine.ws import KWebSocketHandler
	from kengine.handler import HandlerManager
	from kengine.msg import MessageManager, BaseDispatcher


	r = redis.Redis("127.0.0.1")
	node = '127.0.0.1:8000'


	class MyDispatcher(BaseDispatcher):

	    def chat(self, handler, ws, message):
	        return 'hey, you said:{}'.format(message)

	message_manager = MessageManager(MyDispatcher())
	HandlerManager.message_manager = message_manager


	class MyWebSocketHandler(KWebSocketHandler):

	    def __init__(self, *args, **kwargs):
	        self.r = r
	        self.node = node
	        super(MyWebSocketHandler, self).__init__(*args, **kwargs)

	if __name__ == '__main__':
	    application = web.Application([
	        (r'/ws', MyWebSocketHandler),
	    ],
	        debug=True)
	    application.listen(8000)
	    r.lpush("NODE_HOST_LIST", node)
	    r.set(node, 0)
	    ioloop.IOLoop.instance().start()

The above snipet code has very easy to understand! Open you chrome (install chrome-extension://pfdhoblngboilpfeibdedpjgfnlcodoo/index.html) and then put the ws://127.0.0.1:8000/ws?uid=1001. you can play with your new toy!

Data Structure
=====

The kengine use `method` as default route tag! you can modify if you want ! for now
I just talking about the default situation!

	{
		"method":"chat",
		"message":{
			"greetting": "hello Frank AK",
			"context":"Where are you from ~~"
		}
	}

The response message is all update to you , you can see the code which i just `'hey, you said:{}'.format(message)` add some prefix :). Sometime if the networking
meet some trouble, we need a `heartbeat` to checking the connection if ok! by default you can use `p` as the tag! but you should declare your own checking solution , if you want to see how to do that see the document :)

Why use redis & Openresty
=====

What the game server has great press, we want to make easy extand~ so we use redis to register self with node id, and use lua + openresty to check which node has leisure time. if we find the target node , nginx we route the client to the node!
