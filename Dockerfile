FROM python:3.12-slim

WORKDIR /code-repair-with-llms

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["bash"]