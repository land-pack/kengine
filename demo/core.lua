

host_1 = {host='127.0.0.1:8101', num=3}
host_2 = {host='127.0.0.1:8102', num=9}
host_3 = {host='127.0.0.1:8103', num=4}

--host_list = {robin = host_1, jon=host_2, max=host_3}
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

print("target host is ", the_host)
