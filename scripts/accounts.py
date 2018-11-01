from web3 import Web3, HTTPProvider
import redis
provider = Web3.HTTPProvider('http://test.terrachain.network')
client = Web3(provider)



redis_host = "localhost"
redis_port = 6379
redis_password = ""
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

for i in range(1,10000):
    acct =client.eth.account.create()
    r.hmset("add",{acct.address+":"+acct.privateKey.hex():0})
    
#####
    
from web3 import Web3, HTTPProvider
import redis
provider = Web3.HTTPProvider('https://test.terrachain.network')
client = Web3(provider)


redis_host = "localhost"
redis_port = 6379
redis_password = ""
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
acs = r.hscan("add",cursor=0,count=200000)
accounts=list(acs[1].keys())
for i in accounts:
    x = client.eth.getBalance(i.split(":")[0])
    if x!=0:
        r.lpush('temp_add',i) 


####

from web3 import Web3, HTTPProvider
import redis
provider = Web3.HTTPProvider('https://test.terrachain.network')
client = Web3(provider)


redis_host = "localhost"
redis_port = 6379
redis_password = ""
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
acs = r.hscan("add",cursor=0,count=200000)
accounts=list(acs[1].keys())
count = 0
for i in accounts:
    #val = r.hget("add",i)
    #if val=="0:1":
    x = client.eth.getBalance(i.split(":")[0])
    if x>0:        
    
        count+=1
print(count)

####

import redis
import json
redis_host = "34.228.182.37"
redis_port = 6379
redis_password = ""
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
start=71150
end=start+7400
for i in reversed(range(start,end)):
            r.lpush('nonce',i) 


####
import redis
import json
redis_host = "localhost"
redis_port = 6379
redis_password = ""
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
start=74505
end=start+9100
for i in reversed(range(start,end)):
            r.lpush('nonce',i) 