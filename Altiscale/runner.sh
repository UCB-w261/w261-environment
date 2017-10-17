#!/bin/bash

# init variables
RUN=0
SETUP=0
PORT="BAD"

# help defintion
usage () {
   echo "How to use:";
   echo "    Initial setup: ./runner.sh -s -p <port>";
   echo "    Initial setup and run: ./runner.sh -sr -p <port>";
   echo "    Run Notebook environment after setup: ./runner.sh -r";
}

# option handler
TEMP=`getopt -o hrsp: --long help,run,start,port: -- "$@"`
eval set -- "$TEMP"

while true ; do
    case "$1" in
        -s|--start)
            SETUP=1 ;
            shift
            ;;
        -p|--port)
            case "$2" in
                "") shift 2 ;;
                *) PORT=$2 ; shift 2 ;;
            esac ;;
        -r|--run)
            RUN=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --) shift ; break ;;
        *) echo 'Invalid option.' 1>&2
            usage 1>&2
            exit 1
            ;;
    esac
done

# do the business
if [ "$SETUP" -eq "1" ]; then
    re='^[0-9]+$'
    if ! [[ $PORT =~ $re ]] ; then
       echo "error: PORT is not a number" >&2; exit 1
    fi
    echo "Cleaning up existing setup"
    rm -rf ~/.conda
    rm -rf ~/.ipython
    rm -rf ~/.jupyter
    rm -rf ~/.local
    echo "Rebuilding .bashrc"
    echo "# .bashrc" > ~/.bashrc
    echo "" >> ~/.bashrc
    echo "# Source global definitions" >> ~/.bashrc
    echo "if [ -f /etc/bashrc ]; then" >> ~/.bashrc
    echo "        . /etc/bashrc" >> ~/.bashrc
    echo "fi" >> ~/.bashrc
    echo "" >> ~/.bashrc
    echo "# User specific aliases and functions" >> ~/.bashrc
    echo 'export PATH=/opt/anaconda2/bin:$PATH' >> ~/.bashrc
    PATH=/opt/anaconda2/bin:$PATH
    echo "Creating Conda environment"
    ENV_NAME=py27
    conda create --name $ENV_NAME python=2.7 -y
    echo "Creating Altiscale Jupyter kernels"
    /mnt/ephemeral1/jupyter/new_alti-jupyter.sh -s
    source activate $ENV_NAME
    echo "Installing python packages"
    conda install -c conda-forge mrjob -y
    conda install nb_conda -y
    conda install numpy -y
    conda install matplotlib -y
    conda install nltk -y
    conda install -c conda-forge -y notebook jupyter_contrib_nbextensions
    jupyter nbextension enable toc2/main
    echo "Configuring Jupyter Notebook environment"
    echo "c.NotebookApp.ip = '*'" > ~/.jupyter/jupyter_notebook_config.py
    echo "c.NotebookApp.port = $PORT" >> ~/.jupyter/jupyter_notebook_config.py
    echo "c.NotebookApp.token = ''" >>  ~/.jupyter/jupyter_notebook_config.py
    echo "Moving Python environment to HDFS for use"
    cd ~/.conda/envs/$ENV_NAME/
    zip -r ~/$ENV_NAME.zip *
    cd ~
    USERNAME="$(id -u -n)"
    hdfs dfs -mkdir /user/$USERNAME/virtualenv/
    hdfs dfs -put -f ~/$ENV_NAME.zip /user/$USERNAME/virtualenv/
    wget --quiet https://raw.githubusercontent.com/UCB-w261/w261-environment/master/Altiscale/AltiscaleExample.ipynb -O AltiscaleExample.ipynb
    echo "Setting up MRJob Configuration"
    echo "runners:" > ~/.mrjob.conf
    echo "  hadoop:" >> ~/.mrjob.conf
    echo "    py_files: hdfs:///user/$USERNAME/virtualenv/$ENV_NAME.zip" >> ~/.mrjob.conf
    echo "    python_bin: python_bin: /opt/rh/python27/root/usr/bin/python2.7" >> ~/.mrjob.conf
    echo "    cmdenv:" >> ~/.mrjob.conf
    echo "      LD_LIBRARY_PATH: /opt/rh/python27/root/usr/lib64" >> ~/.mrjob.conf
    echo "    cleanup_on_failure: ALL" >> ~/.mrjob.conf
    echo "  local:" >> ~/.mrjob.conf
    echo "    cleanup_on_failure: ALL" >> ~/.mrjob.conf
fi

if [ "$RUN" -eq "1" ]; then
    /mnt/ephemeral1/jupyter/new_alti-jupyter.sh -r
fi

