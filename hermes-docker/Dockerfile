FROM node:20-bookworm-slim

RUN apt-get update && apt-get install -y \
    iputils-ping \
    traceroute \
    net-tools \
    snmp \
    netcat-openbsd \
    iproute2 \
    python3 \
    python3-pip \
    curl \
    nano \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://hermes-agent.nousresearch.com/install.sh | bash

ENV PATH="/usr/local/lib/hermes-agent/venv/bin:/usr/local/bin:${PATH}"

RUN curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py && \
    /usr/local/lib/hermes-agent/venv/bin/python3 /tmp/get-pip.py && \
    /usr/local/lib/hermes-agent/venv/bin/python3 -m pip install "packaging==26.0" && \
    /usr/local/lib/hermes-agent/venv/bin/python3 -m pip install python-telegram-bot && \
    rm /tmp/get-pip.py

WORKDIR /root

EXPOSE 8080

CMD ["hermes", "gateway"]
