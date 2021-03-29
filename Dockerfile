# Nothing yet
FROM python3.9.2-alpine3.13

RUN apk add git gcc g++ make

RUN git clone https://github.com/Felaxus/nightscout_hue.git

RUN cd nightscout_hue

RUN pip install --no-cache-dir -r requirements.txt

RUN rm Dockerfile docker-compose.yml requirements.txt

ENTRYPOINT ["docker-entrypoiny.sh"]