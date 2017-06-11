HighScore = { Robin = 8, Jon = 10, Max = 11 }

-- basic usage, just sort by the keys
table.sort(HighScore)
for v in pairs(HighScore) do
    print(v)
end
--> Jon     10
--> Max     11
--> Robin   8

-- this uses an custom sorting function ordering by score descending
table.sort(HighScore, function(t,a,b) return t[b] > t[a] end)

print(string.rep("=",20))

for v in pairs(HighScore) do
    print(v)
end
--> Max     11
--> Jon     10
--> Robin   8
