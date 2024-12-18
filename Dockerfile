FROM nvcr.io/nvidia/pytorch:24.06-py3

# PACKAGE INSTALATION
RUN apt-get update
RUN apt-get install -y tmux

ENV PYTHONDONTWRITEBYTECODE=1

# PIP example
# RUN pip install pilkit plotly