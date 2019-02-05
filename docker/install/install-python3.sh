#!/bin/bash
yum install -y centos-release-scl
yum install -y rh-python36
cat /opt/rh/rh-python36/enable >> ~/.bashrc && \
    source ~/.bashrc