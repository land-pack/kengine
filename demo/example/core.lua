host_1 = {host='127.0.0.1:8101', num=9}
host_2 = {host='127.0.0.1:8102', num=9}
host_3 = {host='127.0.0.1:8103', num=9}

host_list = {}

table.insert(host_list, host_1)
table.insert(host_list, host_2)
table.insert(host_list, host_3)

table.sort(host_list, function(a, b) return a.num < b.num end)

the_host = ''

for v in pairs(host_list) do
    print(v, host_list[v], host_list[v].num, host_list[v].host)
    if host_list[v].num % 9 ~= 0 then
        the_host = host_list[v].host
    end
end
if the_host == '' then
    for v in pairs(host_list)
    do
        -- reset the all node used mark to 0
        -- set redis on production 
        host_list[v].num = 0
    end
    the_host = host_list[math.random(#host_list)].host
end


for v in pairs(host_list) 
do
    print(host_list[v].num)
end

print("target host is ", the_host)
