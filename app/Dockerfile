FROM python:3.8.5
MAINTAINER "renatobanzai@gmail.com"
COPY ./ /app
WORKDIR /app
RUN apt-get update && apt-get install -y default-jre-headless && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]