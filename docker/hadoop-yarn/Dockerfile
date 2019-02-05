FROM centos:7

ARG HADOOP_VERSION

# install hadoop required libraries
RUN yum update -y && \
    yum install -y java-1.8.0-openjdk-devel \
                   openssh-server \
                   openssh-clients \
                   rsync \
                   wget
ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk

# install python 3
ADD docker/install /tmp/install
RUN chmod +x /tmp/install/install-python3.sh && \
    tmp/install/install-python3.sh && \
    rm -rf tmp/install
ENV PATH="/opt/rh/rh-python36/root/bin:$PATH"
RUN python --version
RUN yum -y groupinstall 'Development Tools'

# configure ssh
RUN echo "/usr/sbin/sshd" >> ~/.bash_profile && \
    /usr/bin/ssh-keygen -A && \
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys


#install hadoop
ENV HADOOP_INSTALL_DIR /opt
RUN wget -P $HADOOP_INSTALL_DIR http://ftp.man.poznan.pl/apache/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xvzf $HADOOP_INSTALL_DIR/hadoop-$HADOOP_VERSION.tar.gz -C $HADOOP_INSTALL_DIR && \
    rm -rf $HADOOP_INSTALL_DIR/hadoop-$HADOOP_VERSION.tar.gz

ENV HADOOP_HOME $HADOOP_INSTALL_DIR/hadoop-$HADOOP_VERSION

ADD conf/single-node/core-site.xml $HADOOP_INSTALL_DIR/hadoop-$HADOOP_VERSION/etc/hadoop/core-site.xml
ADD conf/single-node/hdfs-site.xml $HADOOP_INSTALL_DIR/hadoop-$HADOOP_VERSION/etc/hadoop/hdfs-site.xml
ADD conf/single-node/hadoop-env.sh $HADOOP_HOME/etc/hadoop/hadoop-env.sh
ADD conf/single-node/mapred-site.xml $HADOOP_HOME/etc/hadoop/mapred-site.xml
ADD conf/single-node/yarn-site.xml $HADOOP_HOME/etc/hadoop/yarn-site.xml
ADD ./docker/start-scripts /start-scripts

RUN chmod +x /start-scripts/start.sh /start-scripts/start-grep-example.sh

# Add some datasets examples
ENV DATASETS_ROOT /datasets
RUN mkdir -p $DATASETS_ROOT
ADD dataset/epa-http $DATASETS_ROOT/epa-http

EXPOSE 8020 8032 8088 9870

VOLUME ["/start-scripts"]
WORKDIR /start-scripts

CMD ["./start.sh"]