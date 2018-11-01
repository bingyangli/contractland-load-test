# Introduction
This tool is used to do the load test for ContractLand's Terra Chain (contractland.io). I will walk you through the environment set up from the scratch. 

# How to Use This Tool

## Install Docker

Get Docker: https://docs.docker.com/install/linux/docker-ce/ubuntu/

Get Docker Compose: https://docs.docker.com/compose/install/

## Download this repository

```bash
git clone https://github.com/bingyangli/load-test.git
```

## Locusts Docker Image

The locusts docker image is designed for easily composing multi-container 
[locust.io](http://http://locust.io/) 
load testing swarms using Python 3.6. The locusts image functions can function
as either a master or worker depending on whether or not the `--master-host` 
flag is specified in a container's run execution call.

cd to the directory where your Dockerfiles located then build your docker conatainer:

```bash
sudo docker build -t "bingyang:test" .
```

## Start the load test cluster

1.Manual Start

The optional `--master-host` argument is used to specify that the container 
should be a worker and communicate with the master with the specified host.
For example:

1.1 Start the master node
```bash
$ docker run -it --rm \
    -v [the absolute path to the "scripts" folder]/scripts:/scripts \
    bingyang:test \
```
1.2 Start the woker nodes
```bash
$ docker run -it --rm \
    -v [the absolute path to the "scripts" folder]/scripts:/scripts \
    bingyang:test \
    --master-host=127.0.0.1
```
Note: You can start multiple worker nodes by the above command. would specify a worker container where the master resides at the local
`127.0.0.1` host location.

1.3 Script Volume

A locusts container requires that a volume be mounted to the container's 
`/scripts` directory. It expects to find the *locustfile.py* to run in that 
directory.


2.Auto Start: Docker Compose

The multi-container environment is easily specified using docker compose. You 
can see an example in this repository of how that would look:
[docker-compose.yml](docker-compose.yml)

```bash
$ docker-compose up
$ docker-compose scale locust-worker=5
```

## Config File
The config file is under scripts/locust.config.jason. "f" is the customized testing program path. You can specify whatever you want by changing this parameter. "target" is the target url for the load test. "min_wait" and "max_wait" is the mimic user waiting time.


