FROM centos:7

ARG SPARK_VERSION

RUN yum update -y && \
    yum install -y java-1.8.0-openjdk-devel wget

# install python 3
ADD docker/install /tmp/install
RUN chmod +x /tmp/install/install-python3.sh && \
    tmp/install/install-python3.sh && \
    rm -rf tmp/install
ENV PATH="/opt/rh/rh-python36/root/bin:$PATH"
RUN python --version
RUN yum -y groupinstall "Development Tools"
ENV PYSPARK_PYTHON=/opt/rh/rh-python36/root/bin/python

ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk

ENV SPARK_HOME /etc/spark
RUN wget -P $SPARK_HOME http://ftp.man.poznan.pl/apache/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop2.7.tgz
RUN tar -xvzf $SPARK_HOME/spark-$SPARK_VERSION-bin-hadoop2.7.tgz --strip 1 -C $SPARK_HOME && \
    rm -rf $SPARK_HOME/spark-$SPARK_VERSION-bin-hadoop2.7.tgz

ENV HADOOP_CONF_DIR /etc/hadoop
RUN mkdir -p $HADOOP_CONF_DIR
ADD conf/single-node/core-site.xml $HADOOP_CONF_DIR/core-site.xml
ADD conf/single-node/yarn-site.xml $HADOOP_CONF_DIR/yarn-site.xml
ADD conf/single-node/hdfs-site.xml $HADOOP_CONF_DIR/hdfs-site.xml

VOLUME ["/execute-script"]

WORKDIR /execute-script

CMD ["./run-naive-grep.sh"]