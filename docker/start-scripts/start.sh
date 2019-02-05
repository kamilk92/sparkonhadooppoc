#!/bin/bash
$HADOOP_HOME/bin/hdfs namenode -format
$HADOOP_HOME/sbin/start-dfs.sh

$HADOOP_HOME/bin/hdfs dfs -mkdir /user
$HADOOP_HOME/bin/hdfs dfs -mkdir /user/root

# put some example files
$HADOOP_HOME/bin/hdfs dfs -mkdir datasets
$HADOOP_HOME/bin/hdfs dfs -put $DATASETS_ROOT/epa-http/epa-http.txt datasets
$HADOOP_HOME/bin/hdfs dfs -put $DATASETS_ROOT/epa-http/epa-http-1.txt datasets

$HADOOP_HOME/sbin/start-yarn.sh

sleep infinity & wait