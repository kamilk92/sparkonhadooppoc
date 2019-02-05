#!/bin/bash
$HADOOP_HOME/bin/hdfs namenode -format
$HADOOP_HOME/sbin/start-dfs.sh

$HADOOP_HOME/bin/hdfs dfs -mkdir /user
$HADOOP_HOME/bin/hdfs dfs -mkdir /user/root

$HADOOP_HOME/bin/hdfs dfs -mkdir datasets
$HADOOP_HOME/bin/hdfs dfs -put $DATASETS_ROOT/epa-http/epa-http.txt datasets
$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.1.1 jar grep datasets output 'Access'