#!/bin/bash
python --version
$SPARK_HOME/bin/spark-submit \
    --master yarn \
    --deploy-mode client \
    naive_grep.py \
        --server hadoop-yarn \
        --port 9000 \
        --file user/root/datasets \
        --value post \
        --out hdfs://user/root/out