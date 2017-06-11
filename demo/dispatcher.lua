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

host_to_connections = {}
connections_to_host_list = {}

-- [[ Node host list, you can put it all in your redis cache ]]--
hosts_list = red:lrange("NODE_HOST_LIST",0, -1) or {}

-- [[ Core dispatcher ]]--
for i, host in ipairs(hosts_list)
do
    ngx.log(ngx.ERR, "the node address ==>>", host)
    host_to_connections[host] = tonumber(red:get(host))

end

-- [[ Rand pick up a node ]] --
host = hosts_list[math.random(#hosts_list)]

-- [[ Return the host to nginx for proxy pass ]]--
ngx.var.websocket_addr = host
