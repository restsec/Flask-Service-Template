FROM python:3

#COPY requirements.txt /app/requirements.txt
COPY ./ /app/

WORKDIR /app

RUN pip3 install --proxy='https://10.30.0.10:3128' --no-cache-dir -r requirements.txt

ADD . /app

#ADD ./devssl ./devssl

COPY conf.json conf.json

EXPOSE 8080

ENTRYPOINT ["/bin/bash", "run.sh"]
