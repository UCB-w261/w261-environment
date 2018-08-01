FROM cloudera/quickstart
MAINTAINER James Winegar

# Install linux development tools and security updates
COPY docker/cloudera-kafka.repo /etc/yum.repos.d/cloudera-kafka.repo
RUN yum clean all && \
    rpm --rebuilddb; yum install -y yum-plugin-ovl && \
    yum update -y && \
    yum groupinstall -y 'Development Tools' && \
    yum install -y --quiet \
      wget \
      htop \
      hadoop-yarn-nodemanager \
      hadoop-hdfs-datanode \
      hadoop-mapreduce \
      hadoop-hdfs-namenode \
      hadoop-yarn-resourcemanager \
      hadoop-client \
      kafka \
      kafka-server && \
    yum clean all

ENV SPARK_VERSION=2.3.1
ENV HADOOP_VERSION=2.7
ENV ANACONDA_VERSION=5.2.0
ENV SPARK_HOME=/opt/spark
# Install Java and Spark and Anaconda
RUN mkdir -p /opt && \
    mkdir -p /downloads && \
    cd /downloads && \
    wget --quiet -c --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u131-b11/d54c1d3a095b4ff2b6607d096fa80163/jdk-8u131-linux-x64.tar.gz && \
    mkdir /usr/java/jdk.1.8.0_131 && \
    tar -xf jdk-8u131-linux-x64.tar.gz -C /usr/java/ && \
    wget --quiet http://mirrors.advancedhosters.com/apache/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} ${SPARK_HOME}-${SPARK_VERSION} && \
    ln -s ${SPARK_HOME}-${SPARK_VERSION} ${SPARK_HOME} && \
    wget --quiet https://repo.continuum.io/archive/Anaconda3-${ANACONDA_VERSION}-Linux-x86_64.sh -O anaconda.sh && \
    /bin/bash /downloads/anaconda.sh -b -p /opt/anaconda && \
    rm -rf /downloads

# Update Python packages
ENV PATH=/opt/anaconda/bin:$PATH
RUN conda update -y conda && \
    conda update -y --all && \
    conda install -y pip setuptools wheel \
    cython numpy pandas scipy nltk scikit-learn scikit-image sympy && \
    conda install -c conda-forge -y jupyterlab kafka-python && \
    conda clean -tp -y && \
    pip install --no-cache-dir bash_kernel && \
    python -m bash_kernel.install


RUN cd $SPARK_HOME/python &&\
      python setup.py install

# Download custom Docker startup file
RUN mkdir -p /root/.jupyter
COPY docker/jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py
COPY docker/themes.jupyterlab-settings /root/.jupyter/lab/user-settings/\@jupyterlab/apputils-extension/
COPY docker/ipython_config.py /root/.ipython/profile_default/ipython_config.py
COPY docker/start-notebook.sh /root/start-notebook.sh
COPY docker/docker-quickstart /usr/bin/docker-quickstart
COPY docker/spark-defaults.conf /etc/spark/conf.dist/spark-defaults.conf
RUN chmod 755 /root/start-notebook.sh && \
    chmod 755 /usr/bin/docker-quickstart

ENV PYSPARK_PYTHON=/opt/anaconda/bin/python
ENV SHELL=bash
ENV JAVA_HOME=/usr/java/jdk1.8.0_131
ENV PATH=$SPARK_HOME/bin:$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.4-src.zip:$PATH
