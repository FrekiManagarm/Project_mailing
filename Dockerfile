FROM ubuntu:14.04
ENV MONIT_VERSION 5.11
 
RUN apt-get update && apt-get install -y wget \
 tar \
 build-essential \
 ca-certificates \
 gcc \
 git \
 libpq-dev \
 make \
 python-pip \
 python2.7 \
 python2.7-dev \
 && apt-get autoremove \
 && apt-get clean
 
RUN wget -O /tmp/monit-$MONIT_VERSION-linux-x64.tar.gz http://mmonit.com/monit/dist/binary/$MONIT_VERSION/monit-$MONIT_VERSION-linux-x64.tar.gz
RUN cd /tmp && tar -xzf /tmp/monit-$MONIT_VERSION-linux-x64.tar.gz && cp /tmp/monit-$MONIT_VERSION/bin/monit /usr/bin/monit
COPY ./monitrc /etc/monitrc
RUN chmod 0700 /etc/monitrc
COPY ./conf.d /etc/monit/conf.d
 
RUN mkdir scripts
COPY scripts /scripts
COPY mqtt_publisher /etc/init.d/
 
RUN chmod +x /etc/init.d/mqtt_publisher
 
RUN pip install -r /scripts/requirements.txt
 
EXPOSE 2812
CMD monit -I