FROM ubuntu:18.04

WORKDIR /usr/src/app
RUN apt-get update
RUN apt-get install python-pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

