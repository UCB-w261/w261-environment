FROM cloudera/quickstart
MAINTAINER James Winegar

# Install linux development tools
RUN echo 'Install Development Tools'
RUN yum clean all
RUN rpm --rebuilddb; yum install -y yum-plugin-ovl
RUN yum clean all
RUN yum groupinstall -y 'Development Tools'
RUN yum install -y --quiet wget


# get Java 1.8 and use for hadoop
RUN wget --quiet -c --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u131-b11/d54c1d3a095b4ff2b6607d096fa80163/jdk-8u131-linux-x64.tar.gz
RUN mkdir /usr/java/jdk.1.8.0_131
RUN tar -xf jdk-8u131-linux-x64.tar.gz -C /usr/java/
ENV JAVA_HOME=/usr/java/jdk1.8.0_131

# upgrade CDH
RUN sudo rpm --import https://archive.cloudera.com/cdh5/redhat/5/x86_64/cdh/RPM-GPG-KEY-cloudera
RUN sudo yum clean all; sudo yum install -y --quiet hadoop-yarn-resourcemanager

# upgrade spark
RUN sudo yum install -y spark-core spark-master spark-worker spark-history-server spark-python
RUN wget https://d3kbcqa49mib13.cloudfront.net/spark-2.2.0-bin-hadoop2.7.tgz
RUN tar -xzf spark-2.2.0-bin-hadoop2.7.tgz
RUN mv spark-2.2.0-bin-hadoop2.7 /opt/spark-2.2.0
RUN ln -s /opt/spark-2.2.0 /opt/spark
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Install and update miniconda and other packages
RUN echo 'Install miniconda and more'
RUN mkdir -p /downloads && \
	mkdir -p /opt && \
	cd /downloads && \
	echo "Downloading Miniconda..." && \
	wget --quiet http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh && \
	/bin/bash /downloads/Miniconda-latest-Linux-x86_64.sh -b -p /opt/anaconda && \
	rm -rf /downloads
ENV PATH $PATH:/opt/anaconda/bin

# Disable token authentication for Jupyter Notebook
RUN mkdir -p /root/.jupyter
RUN touch /root/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.token = ''" >> /root/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.password = ''" >> /root/.jupyter/jupyter_notebook_config.py

RUN conda update conda
RUN conda install cython
RUN conda install ipython
RUN conda install ipython_genutils
RUN conda install ipython-qtconsole
RUN conda install ipython-notebook
RUN conda install libpng
RUN conda install notebook
RUN conda install numpy
RUN conda install pandas
RUN conda install scipy
RUN conda install jupyter
RUN conda install bokeh
RUN conda install nltk
RUN conda install pip
RUN conda install scikit-learn
RUN conda install scikit-image
RUN conda install setuptools
RUN conda install sympy
RUN conda install wheel
RUN conda install unicodecsv
RUN conda install ujson
RUN conda install zlib
RUN conda update --all
RUN conda install -c conda-forge -y jupyter_contrib_nbextensions
RUN conda clean -t
RUN conda clean -p

# Pip installs
RUN source /opt/anaconda/bin/activate
RUN pip install mrjob

# Jupyter settings
RUN jupyter nbextension enable toc2/main

# Download custom Docker startup file
RUN cd /root && \
	wget --quiet https://raw.githubusercontent.com/UCB-w261/w261-environment/master/start-notebook-pyspark.sh && \
	chmod 755 /root/start-notebook-pyspark.sh
	
RUN cd /root && \
	wget --quiet https://raw.githubusercontent.com/UCB-w261/w261-environment/master/start-notebook-python.sh && \
	chmod 755 /root/start-notebook-python.sh

RUN cd /root && \
	wget --quiet https://raw.githubusercontent.com/UCB-w261/w261-environment/master/docker-quickstart && \
	chmod 755 /root/docker-quickstart && \
	cat docker-quickstart > /usr/bin/docker-quickstart

ENV PYSPARK_PYTHON=/opt/anaconda/bin/python
ENV PYSPARK_DRIVER_PYTHON=jupyter
ENV PYSPARK_DRIVER_PYTHON_OPTS="notebook --port 8890 --notebook-dir='/media/notebooks' --ip='*' --no-browser --allow-root"