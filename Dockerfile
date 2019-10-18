FROM python:3.7-alpine3.10

WORKDIR /var/www/web/
COPY ./ /var/www/web/

RUN apk add --no-cache --virtual .build-deps \
      gcc \
      musl-dev \
      python3-dev \
      postgresql-dev \
 && pip install --upgrade pip \
 && pip install --no-cache-dir -r ./requirements.txt \
 && apk del --no-cache .build-deps

RUN apk add --no-cache \
      --repository 'http://dl-cdn.alpinelinux.org/alpine/edge/testing' \
      --repository 'http://dl-cdn.alpinelinux.org/alpine/edge/main' \
      postgresql-client \
      postgresql-libs \
      geos \
      gdal \
      libpq \
      proj

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
