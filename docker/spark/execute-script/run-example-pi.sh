#!/bin/bash
$SPARK_HOME/bin/spark-submit \
    --class org.apache.spark.examples.SparkPi \
    --master yarn \
    --deploy-mode client \
    --conf spark.network.timeout=3602 \
    --conf spark.executor.heartbeatInterval=3601 \
    $SPARK_HOME/examples/jars/spark-examples_2.11-2.3.1.jar