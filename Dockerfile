FROM cloudera/quickstart
MAINTAINER Ankit Tharwani

# Install linux development tools
RUN echo 'Install Development Tools'
RUN yum clean all
RUN rpm --rebuilddb; yum install -y yum-plugin-ovl
RUN yum clean all
RUN yum groupinstall -y 'Development Tools'

# Install and update miniconda and other packages
RUN echo 'Install miniconda and more'
RUN yum install -y --quiet wget && \
	mkdir -p /downloads && \
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
RUN conda clean -t
RUN conda clean -p

# Set Environment Variable to use ipython with PySpark
RUN echo 'Set environment variables'
ENV PYSPARK_PYTHON /opt/anaconda/bin/python
ENV IPYTHON 1
ENV IPYTHON_OPTS "notebook --port 8889 --notebook-dir='/media/notebooks' --ip='*' --no-browser"

# Download custom Docker startup file
RUN cd /root && \
	wget --quiet https://raw.githubusercontent.com/ankittharwani/mids-cloudera-hadoop/master/startup.sh && \
	chmod 755 /root/startup.sh && \
	wget --quiet https://raw.githubusercontent.com/ankittharwani/mids-cloudera-hadoop/master/docker-quickstart && \
	chmod 755 /root/docker-quickstart && \
	cat docker-quickstart > /usr/bin/docker-quickstart

RUN source /opt/anaconda/bin/activate
RUN pip install mrjob

# Add Tini
# ENV TINI_VERSION v0.13.2
# ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
# RUN chmod +x /tini
# ENTRYPOINT ["/tini", "--"]

# Run jupyter under Tini
# CMD ["jupyter", "notebook", "--port=8889", "--notebook-dir='/media/notebooks'", "--no-browser", "--ip='*'", "&"]
