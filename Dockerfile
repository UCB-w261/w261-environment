FROM cloudera/quickstart
MAINTAINER James Winegar

# Install linux development tools, Java, and Spark
RUN yum clean all && \
    rpm --rebuilddb; yum install -y yum-plugin-ovl && \
    yum clean all && \
    yum groupinstall -y 'Development Tools' && \
    yum install -y --quiet wget && \
    mkdir -p /downloads && \
    mkdir -p /opt && \
    cd /downloads && \
    wget --quiet -c --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u131-b11/d54c1d3a095b4ff2b6607d096fa80163/jdk-8u131-linux-x64.tar.gz && \
    mkdir /usr/java/jdk.1.8.0_131 && \
    tar -xf jdk-8u131-linux-x64.tar.gz -C /usr/java/ && \
    sudo rpm --import https://archive.cloudera.com/cdh5/redhat/5/x86_64/cdh/RPM-GPG-KEY-cloudera && \
    sudo yum clean all; sudo yum install -y --quiet hadoop-yarn-resourcemanager && \
    sudo yum install -y spark-core spark-master spark-worker spark-history-server spark-python && \
    sudo wget --quiet https://d3kbcqa49mib13.cloudfront.net/spark-2.2.0-bin-hadoop2.7.tgz && \
    tar -xzf spark-2.2.0-bin-hadoop2.7.tgz && \
    mv spark-2.2.0-bin-hadoop2.7 /opt/spark-2.2.0 && \
    ln -s /opt/spark-2.2.0 /opt/spark && \
	rm -rf /downloads
	
RUN mkdir -p /downloads && \
    cd /downloads && \
    wget --quiet https://repo.continuum.io/archive/Anaconda2-5.0.0-Linux-x86_64.sh -O anaconda.sh && \
	/bin/bash /downloads/anaconda.sh -b -p /opt/anaconda && \
    rm -rf /downloads && \
	mkdir -p /root/.jupyter && \
    touch /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.token = ''" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.password = ''" >> /root/.jupyter/jupyter_notebook_config.py 

ENV PATH=/opt/anaconda/bin:$PATH

RUN conda update conda && \
    conda install -y cython && \
    conda install -y ipython && \
    conda install -y ipython_genutils && \ 
    conda install -y ipython-qtconsole && \ 
    conda install -y ipython-notebook && \ 
    conda install -y libpng && \ 
    conda install -y numpy && \ 
    conda install -y pandas && \ 
    conda install -y scipy && \ 
    conda install -y jupyter && \ 
    conda install -y bokeh && \ 
    conda install -y nltk && \ 
    conda install -y pip && \ 
    conda install -y scikit-learn && \ 
    conda install -y scikit-image && \ 
    conda install -y setuptools && \ 
    conda install -y sympy && \ 
    conda install -y wheel && \ 
    conda install -y unicodecsv && \ 
    conda install -y ujson && \ 
    conda install -y zlib && \ 
    conda update --all && \ 
    conda install -c conda-forge -y mrjob && \ 
    conda install -c conda-forge -y notebook jupyter_contrib_nbextensions && \
    conda clean -t && \ 
    conda clean -p && \
    jupyter nbextension enable toc2/main


# Download custom Docker startup file
RUN cd /root && \
    wget --quiet https://raw.githubusercontent.com/UCB-w261/w261-environment/master/start-notebook-pyspark.sh && \
    wget --quiet https://raw.githubusercontent.com/UCB-w261/w261-environment/master/docker-quickstart && \
    chmod 755 /root/start-notebook-pyspark.sh && \
    chmod 755 /root/docker-quickstart && \
    cat docker-quickstart > /usr/bin/docker-quickstart

ENV JAVA_HOME=/usr/java/jdk1.8.0_131
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH
ENV PYSPARK_PYTHON=/opt/anaconda/bin/python
ENV PYSPARK_DRIVER_PYTHON=jupyter
ENV PYSPARK_DRIVER_PYTHON_OPTS="notebook --port 8889 --notebook-dir='/media/notebooks' --ip='*' --no-browser --allow-root"