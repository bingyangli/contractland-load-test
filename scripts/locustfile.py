#!/usr/bin/env python

from functools import wraps
import random
from time import time
from locust import Locust, TaskSet, events, task
from web3 import Web3, HTTPProvider
import json

def parse(args: list = None) -> dict:
    """ """

    with open('scripts/locust.config.json') as f:
    #with open('/home/bing/Softwares/load-test/scripts/locust.config.json') as f:
        
        configs: dict = json.load(f)


    return configs

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


class EthLocust(Locust):
    '''
    This is the abstract Locust class which should be subclassed.
    It provides an Ethereum JSON-RPC client that can be used for
    requests that will be tracked in Locust's statistics.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        conf_args=parse()
        provider = Web3.HTTPProvider(conf_args['target']) 
        self.client = Web3(provider)
        

class EthUser(EthLocust):
    
    conf_args=parse()
    host=conf_args['target']
    min_wait = conf_args['min_wait']
    max_wait = conf_args['min_wait']
    
    def __init__(self):
        super(EthUser, self).__init__()  


    class task_set(TaskSet):
        
        
        @geth_locust_task
        @task
        def load_test_get_block(self):

            
            
            bal = self.client.eth.getBlock("latest")
            
            print(bal)

           
                
            return bal
