--[[
    Author: Frank AK
    Date: June/23/2017 

    How does it work?
    When a client send a websockey request, the nginx
    will checking the redis `NODE_HOST_LIST` queue 
    if find some node are avaiable. And then this script
    will try to find the best match node as proxy ~
    so loop checking the node status by from redis with
    node id as key . for detail see the code below ~


    Q: Why don't use set_by_lua
    A: API disabled in the context of set_by_lua*?
    https://github.com/openresty/lua-nginx-module/issues/275 

    ]] --

local var = ngx.var
local redis = require "resty.redis"

local red = redis:new()
red:set_timeout(1000)
local ok, err = red:connect("127.0.0.1", 6379)
if not ok then
    ngx.log(ngx.ERR, "something about redis ", ok)
end

-- [[ Node host list, you can put it all in your redis cache ]]--
origin_host_list = red:lrange("NODE_HOST_LIST",0,  100) or {}
ROOM_SIZE = tonumber(red:get("NODE_ROOM_SIZE") or '9')
DISPATCHER_ALGO = tonumber(red:get("DISPATCHER_ALGO") or '1')  or 1
host_list = {}



-- [[ Core dispatcher ]]--
for i, host in ipairs(origin_host_list)
do
    connect_num = tonumber(red:get(host))
    table.insert(host_list, {host=host, num=connect_num})
end

table.sort(host_list, function(a, b) return a.num < b.num end)
the_host = ''

for i, v in ipairs(host_list) 
do
    the_room_player = host_list[i].num
    if the_room_player % ROOM_SIZE ~= 0 then
        the_host = host_list[i].host
        break
    end 
end
if the_host == '' then
    if DISPATCHER_ALGO == 1 then
        -- [[ Rand pick up a node , weight sort ~~]] --
        the_host = host_list[math.random(#host_list)].host
    else
        -- [[ Pick a node which has least connection ]] --
        table.sort(host_list, function(a, b) return a.num > b.num end)
        the_host = host_list[1].host
    end
end
if the_host == '' then
        ngx.log(ngx.ALERT, "Can 't no find any node | so use default node")
        the_host = '127.0.0.1:9011'
end
-- [[ Return the host to nginx for proxy pass ]]--
ngx.var.websocket_addr = the_host
