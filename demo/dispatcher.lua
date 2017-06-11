--[[ API disabled in the context of set_by_lua*? 
    https://github.com/openresty/lua-nginx-module/issues/275 ]] --

local var = ngx.var
local redis = require "resty.redis"

local red = redis:new()
red:set_timeout(1000)
local ok, err = red:connect("127.0.0.1", 6379)

-- [[ Node host list, you can put it all in your redis cache ]]--
origin_host_list = red:lrange("NODE_HOST_LIST",0, -1) or {}
ROOM_SIZE = tonumber(red:get("NODE_ROOM_SIZE") or '9')
host_list = {}

-- [[ Core dispatcher ]]--
for i, host in ipairs(origin_host_list)
do
    connect_num = tonumber(red:get(host))
    table.insert(host_list, {host=host, num=connect_num})
end

table.sort(host_list, function(a, b) return a.num < b.num end)
the_host = ''

for v in pairs(host_list) do
    if host_list[v].num % ROOM_SIZE ~= 0 then
        the_host = host_list[v].host
    end 
end

if the_host == '' then
    -- [[ Rand pick up a node , weight sort ~~]] --
    the_host = host_list[math.random(#host_list)].host
end

-- [[ Return the host to nginx for proxy pass ]]--
ngx.var.websocket_addr = the_host
