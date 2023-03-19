FROM python:3.8 as build-python

WORKDIR /project

COPY requirements.txt /project/
RUN apt-get update 
# Install Python dependencies
RUN apt-get clean
RUN pip install -r requirements.txt

COPY . /project

EXPOSE 80