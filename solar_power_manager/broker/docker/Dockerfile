FROM resin/rpi-raspbian:stretch

LABEL maintainer="lukasz.towarek@gmail.com"

RUN apt-get update && apt-get install -y wget && \
    wget -O - http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key | apt-key add - && \
    wget -O /etc/apt/sources.list.d/mosquitto-stretch.list http://repo.mosquitto.org/debian/mosquitto-stretch.list && \
    apt-get update && apt-get install -y mosquitto mosquitto-clients

EXPOSE 1883 9001

COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

