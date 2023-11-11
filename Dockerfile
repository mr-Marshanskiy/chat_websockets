# pull official base image
FROM python:3.11-alpine3.18

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .


RUN python -m pip install -r requirements.txt --no-cache-dir




# copy project
COPY . .
