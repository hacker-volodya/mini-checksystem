FROM python:3 as builder
RUN pip3 install jinja2 pyyaml
WORKDIR /services
COPY services /services
COPY build.py /build.py
RUN python3 /build.py /services /cs.services.conf /checkers /app/checkers

FROM node:12 as scoreboard

RUN git clone https://github.com/HackerDom/ctf-scoreboard-client.git /repo
WORKDIR /repo/scoreboard

RUN npm install
RUN npm run build

FROM ghcr.io/hackerdom/checksystem:master

COPY --from=scoreboard /repo/scoreboard/build /scoreboard
ENV CS_STATIC=/scoreboard

ENV MOJO_CONFIG=/app/cs.conf
ENV MOJO_MODE=production

RUN apt-get update
RUN apt-get install -y python3-pip postgresql-client

# Copy checkers to /app/checkers catalog
COPY --from=builder /checkers /app/checkers
RUN cd /app/checkers && ./setup.sh

# Copy config
COPY --from=builder /cs.services.conf /app/cs.production.conf
COPY cs.conf /app/cs.conf

EXPOSE 8080
