#!/usr/bin/env python

from functools import wraps
import random
from time import time
from locust import Locust, TaskSet, events, task
from web3 import Web3, HTTPProvider
import json
import redis



def parse(args: list = None) -> dict:
    """ """
    with open('scripts/locust.config.json') as f:        
        configs: dict = json.load(f)
    return configs

conf_args=parse()
provider = Web3.HTTPProvider(conf_args['target']) 
client = Web3(provider)

#nonce=client.eth.getTransactionCount(conf_args['address'])
#noncex=nonce
redis_host = conf_args['redis_host']
redis_port = conf_args['redis_port']
redis_password = conf_args["redis_password"]
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)





def geth_locust_task(f):
    '''
    Simple timing wrapper which fires off the necessary
    success and failure events for locust.
    '''
    @wraps(f)
    def wrapped(*args, **kwargs):
        start_time = time()
        try:
            result = f(*args, **kwargs)
            print(result)
        except Exception as e:
            print('Exception in {}'.format(f.__name__))
            total_time = int((time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="jsonrpc",
                name=f.__name__,
                response_time=total_time,
                exception=e)
            return False
        else:
            total_time = int((time() - start_time) * 1000)
            events.request_success.fire(
                request_type="jsonrpc",
                name=f.__name__,
                response_time=total_time,
                response_length=0)
        return result
    return wrapped

    

        


class EthUser(Locust):

    conf_args=parse()
    host=conf_args['target']
    min_wait = conf_args['min_wait']
    max_wait = conf_args['min_wait']

            
    class task_set(TaskSet):
        
       
            
        
        @geth_locust_task
        @task
        def load_test_send_transaction(self):
            
            
            try:    
                    
                    
                    noncex=r.lpop("nonce")
                    #print(noncex)
                    #print(noncex[0])
                    #print(noncex[1])
                    
                    if noncex != None:
                        
                        signed_txn = client.eth.account.signTransaction(dict(
                                nonce=int(noncex),
                                gasPrice=234567897654321,
                                gas=100000,
                                to='0x61cE02F8Cc5a6D79864c159d8655dD4957508ED6',
                                value=12345,
                                data=b'',
                              ),
                              conf_args['privatekey'],
                        )        
                 
                        
                        print(noncex)
                        bal=client.eth.sendRawTransaction(signed_txn.rawTransaction)
                        
                                                
                        #r.zrem("nonce",noncex)      
                        #r.zadd("nonce",str(self.id_),int(noncex))
                        #r.zadd("nonce","-1",int(noncex)+1)  
                        
                        
                        print("--------")                         
                    else:
                        exit()
            except Exception as e:
                print(e)
            return bal    
