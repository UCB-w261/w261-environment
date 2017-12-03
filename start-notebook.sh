#! /usr/bin/env bash

echo "###################### Starting Jupyter Notebook ######################"
jupyter notebook --port 8889 --notebook-dir='/media/notebooks' --ip='*' --no-browser --allow-root &