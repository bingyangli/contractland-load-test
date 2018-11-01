#!/usr/bin/env python3

# step 1: import the redis-py client package
import redis
from web3 import Web3, HTTPProvider
import json
# step 2: define our connection information for Redis
# Replaces with your configuration information
redis_host = "127.0.0.1"
redis_port = 6379
redis_password = ""

def parse(args: list = None) -> dict:
    """ """
    with open('locust.config.json') as f:        
        configs: dict = json.load(f)
    return configs

conf_args=parse()
provider = Web3.HTTPProvider(conf_args['target']) 
client = Web3(provider)

def hello_redis():
    """Example Hello Redis Program"""
   
    # step 3: create the Redis Connection object
    try:
   
        # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
        # using the default encoding utf-8.  This is client specific.
        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        #start=44570
        start=client.eth.getTransactionCount(conf_args['address'])
        end=start+1000
            
        
        # step 4: Set the hello message in Redis
        for i in reversed(range(start,end)):
            r.lpush('nonce',i)     
        print(r.lrange("nonce",0,-1))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    hello_redis()
