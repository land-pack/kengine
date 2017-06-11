--[[
    API disabled in the context of set_by_lua*? 
    https://github.com/openresty/lua-nginx-module/issues/275 
]] --

local var = ngx.var
--local devicedb = ngx.shared.devicedb

local redis = require "resty.redis"

local red = redis:new()
red:set_timeout(1000)
local ok, err = red:connect("127.0.0.1", 6379)

if not ok then
    ngx.log(ngx.ERR, "failed to connect redis: ", err)
else
    ngx.log(ngx.INFO, "connection ok:", ok) 
end

connections_number_list = {}

-- [[ Node host list, you can put it all in your redis cache ]]--
hosts_list = red:lrange("NODE_HOST_LIST",0, -1) or {}
ROOM_SIZE = red:get("NODE_ROOM_SIZE") or 9

-- [[ Core dispatcher ]]--
for i, host in ipairs(hosts_list)
do
    connect_num = tonumber(red:get(host))
    table.insert(connections_number_list, {host=host, num=connect_num})
end

table.sort(connections_number_list, function(a, b) return a.num < b.num end)
the_host = ''

for v in pairs(host_list) do
    if host_list[v].num % ROOM_SIZE ~= 0 then
        the_host = host_list[v].host
    end
end

if the_host == '' then
    for v in pairs(host_list)
    do
        -- reset the all node used mark to 0
        -- set redis on production 
        red:set(host_list[v].host, 0)
    end
    -- [[ Rand pick up a node ]] --
    the_host = host_list[math.random(#host_list)].host
end

-- [[ Return the host to nginx for proxy pass ]]--
ngx.var.websocket_addr = the_host
