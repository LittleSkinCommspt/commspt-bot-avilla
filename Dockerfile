FROM python:3.12-slim

LABEL org.opencontainers.image.source=https://github.com/LittleSkinCommspt/commspt-bot-avilla.git
LABEL org.opencontainers.image.url=https://github.com/LittleSkinCommspt/commspt-bot-avilla

WORKDIR /app

COPY poetry.lock ./poetry.lock
COPY pyproject.toml ./pyproject.toml

ENV POETRY_HOME=/opt/poetry
    
RUN pip config set global.index-url https://mirror.sjtu.edu.cn/pypi/web/simple && \
    python3 -m venv $POETRY_HOME && \
    $POETRY_HOME/bin/pip install poetry==1.7.0

RUN $POETRY_HOME/bin/poetry install --no-interaction

CMD $POETRY_HOME/bin/poetry run start-bot