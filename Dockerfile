FROM nvcr.io/nvidia/pytorch:24.06-py3

WORKDIR /app

COPY requirement.txt .

RUN sed -i '/pywin32/d' requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# PACKAGE INSTALATION
RUN apt-get update
RUN apt-get install -y tmux

ENV PYTHONDONTWRITEBYTECODE=1
