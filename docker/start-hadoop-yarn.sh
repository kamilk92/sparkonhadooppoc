#!/bin/bash
docker run --network=hadoop-network --name=hadoop-yarn -p 8032:8032 -p 8088:8088 -p 9870:9870 -it hadoop-yarn