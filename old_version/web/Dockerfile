FROM alpine:3.18

RUN apk add --update --no-cache supervisor openssh python3 py3-pip zlib jpeg-dev zlib-dev gcc python3-dev vim nano
RUN apk add --no-cache --virtual .build-deps build-base linux-headers

RUN adduser -D -u 1000 -g 1000 -s /bin/sh www

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY config/supervisord.conf /etc/supervisord.conf
COPY --chown=www:www app/ /app

EXPOSE 5000

ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
