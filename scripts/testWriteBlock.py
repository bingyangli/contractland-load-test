#!/usr/bin/env python

from functools import wraps
import random
from time import time,sleep
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
                    ac = r.lpop("temp_add")
                    #print(ac)
                    acc=ac.split(":")[0]  
                    key=ac.split(":")[1]
                    noncex=client.eth.getTransactionCount(acc)
                    #noncex=r.lpop("nonce")
                    #print(noncex)
                    #print(noncex[0])
                    #print(noncex[1])
                    
                    if noncex != None:
                        
                        signed_txn = client.eth.account.signTransaction(dict(
                                nonce=int(noncex),
                                gasPrice=234567897654321,
                                gas=21000,
                                to=conf_args['target'],
                                value=10,
                                data=b'',
                              ),
                              key,
                        )        
                 
                        
                        print(noncex)
                        bal=client.eth.sendRawTransaction(signed_txn.rawTransaction)
                        
                        
                        
                        res=client.eth.getTransaction(bal)
                        #print(res)
                        while res["blockHash"] ==None:
                            #sleep(1)
                            
                            res=client.eth.getTransaction(bal)                                  
                            #print(res["blockHash"] ==None)
                            print(noncex)
                        
                        
                        print("--------")                         
                    else:
                        exit()
            except Exception as e:
                print(e)
            return res    
