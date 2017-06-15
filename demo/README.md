# Demo

This demo is very simple, just make sure your all configure is correct ~~


How to make a env ?
==================

you need to install `openresty`, and then put the demo code on correct path ~
I am assume you openresty install as below path
    
    /usr/local/openresty

and then you should make a nginx config directory your self, my directory on
    
    /usr/local/openresty/nginx/conf.d

and then make a directory to save your lua script ~

    /usr/local/lua

if you haven't been installed virtualenv ,you should install it first

	sudo pip install virtualenv

to run a tornado websocket server as node , you need to install torado 

    virtualenv demo
    source demo/bin/active
    pip install tornado
    pip install redis

How to run it ?
===============

First at first , run your openresty ~

    /usr/local/openresty/nginx/sbin/nginx

and then run your redis (cause i don't know where are your redis ~~, so forget me
don't show the start way) and then run your tornado instance
        
    python knode.py --port=8101 # any port as you like ~~

# How to test it?

Try by chrome websocket extend, visiti `ws://127.0.0.1:9009/ws` . see the nginx log
should be at `/usr/local/openresty/nginx/logs/error.log` 
