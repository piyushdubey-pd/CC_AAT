from alpine:latest

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

WORKDIR /app
COPY . /app


RUN set -e; \
   apk add --no-cache --virtual .build-deps \
      gcc \
      libc-dev \
      linux-headers \
   ; \
   pip3 --no-cache-dir install -r requirements.txt; \
   apk del .build-deps;
