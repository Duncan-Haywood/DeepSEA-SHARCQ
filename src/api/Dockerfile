FROM python:3.9-slim-bullseye AS base
ARG PROD
WORKDIR /code

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0 \
  VIRTUAL_ENV=/venv


FROM base as builder
RUN pip install poetry==$POETRY_VERSION
COPY poetry.lock pyproject.toml /code/
#create and activate virtual environment
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# install dependencies
RUN poetry install $(test ! $PROD && echo "--no-dev") --no-interaction --no-ansi
COPY . /code
RUN poetry build --no-interaction

FROM base AS app
COPY ./dist/*.whl ./ FROM builder
COPY ./venv ./ FROM builder
# activate virtual environment
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# install package
RUN pip install ./dist/*.whl

#run ai script
ENV S3_BUCKET=None
CMD python3 -m deepseasharcqapi.main_api