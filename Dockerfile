FROM cloudera/quickstart
MAINTAINER James Winegar

# Install linux development tools and security updates
RUN yum clean all && \
    rpm --rebuilddb; yum install -y yum-plugin-ovl && \
    yum groupinstall -y 'Development Tools' && \
    yum install -y --quiet wget && \
    yum clean all

ENV SPARK_VERSION=2.2.0
ENV HADOOP_VERSION=2.7
ENV ANACONDA_VERSION=5.0.1
# Install Java and Spark and Anaconda
RUN mkdir -p /opt && \
    mkdir -p /downloads && \
    cd /downloads && \
    wget --quiet -c --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u131-b11/d54c1d3a095b4ff2b6607d096fa80163/jdk-8u131-linux-x64.tar.gz && \
    mkdir /usr/java/jdk.1.8.0_131 && \
    tar -xf jdk-8u131-linux-x64.tar.gz -C /usr/java/ && \
    wget --quiet http://mirrors.advancedhosters.com/apache/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark-${SPARK_VERSION} && \
    ln -s /opt/spark-${SPARK_VERSION} /opt/spark && \
    wget --quiet https://repo.continuum.io/archive/Anaconda2-${ANACONDA_VERSION}-Linux-x86_64.sh -O anaconda.sh && \
	/bin/bash /downloads/anaconda.sh -b -p /opt/anaconda && \
    rm -rf /downloads

# Update Python packages
ENV PATH=/opt/anaconda/bin:$PATH
RUN conda update conda && \
    conda update --all && \
    conda install -y pip setuptools wheel \
    cython numpy pandas scipy nltk scikit-learn scikit-image sympy \
    ipython ipython_genutils ipython-qtconsole ipython-notebook jupyter \
    libpng unicodecsv ujson zlib && \
    conda install -c conda-forge -y mrjob pyspark notebook jupyter_contrib_nbextensions && \
    jupyter nbextension enable toc2/main && \
    conda clean -tp -y

# Download custom Docker startup file
RUN mkdir -p /root/.jupyter
COPY jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py
COPY start-notebook.sh /root/start-notebook.sh
COPY docker-quickstart /usr/bin/docker-quickstart
COPY spark-defaults.conf /etc/spark/conf.dist/spark-defaults.conf
RUN chmod 755 /root/start-notebook.sh && \
    chmod 755 /usr/bin/docker-quickstart

ENV PYSPARK_PYTHON=/opt/anaconda/bin/python
ENV JAVA_HOME=/usr/java/jdk1.8.0_131
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.4-src.zip:$PATH