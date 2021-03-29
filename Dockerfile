# Nothing yet
FROM python3.9.2-alpine3.13

RUN apk add git gcc g++ make

RUN git clone https://github.com/Felaxus/nightscout_hue.git

RUN cd nightscout_hue

RUN rm Dockerfile docker-compose.yml

ENTRYPOINT ["python", "src/main.py"]