FROM python:3.12-slim

LABEL org.opencontainers.image.source=https://github.com/LittleSkinCommspt/commspt-bot-avilla.git
LABEL org.opencontainers.image.url=https://github.com/LittleSkinCommspt/commspt-bot-avilla

WORKDIR /app

COPY pdm.lock ./pdm.lock
COPY pyproject.toml ./pyproject.toml
COPY README.md ./README.md

ENV PDM_HOME=/opt/pdm

RUN pip config set global.index-url https://mirror.sjtu.edu.cn/pypi/web/simple && \
    python3 -m venv $PDM_HOME && \
    $PDM_HOME/bin/pip install pdm

RUN $PDM_HOME/bin/pdm install --check --prod --no-editable

CMD $PDM_HOME/bin/pdm run start-bot