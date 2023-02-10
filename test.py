
li=[]
hq.heappush(li,(5,['a']))
hq.heappush(li,(7,['b']))
hq.heappush(li,(3,['c']))

print(hq.heappop(li)[1])
print(hq.heappop(li))
print(hq.heappop(li))