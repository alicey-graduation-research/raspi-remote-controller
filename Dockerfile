FROM python:3.9.10

RUN apt-get update && apt-get install -y unzip wget make build-essential
# pigpio install
WORKDIR /tmp
RUN wget https://github.com/joan2937/pigpio/archive/master.zip
RUN unzip master.zip
WORKDIR /tmp/pigpio-master
RUN make
RUN make install
RUN ldconfig

RUN apt-get install -y python3-pigpio \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*
# gccとか消したほうが良い希ガス
# RUN /usr/local/bin/pigpiod

#app 
WORKDIR /opt/app
ENV PYTHONUNBUFFERED 1

ADD requirements.txt ./requirements.txt
ADD app/ .

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

ENTRYPOINT [ "python", "app.py" ] 

EXPOSE 80