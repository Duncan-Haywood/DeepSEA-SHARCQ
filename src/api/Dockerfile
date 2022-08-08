# for lambda use with poetry
FROM public.ecr.aws/lambda/python:3.9 AS base
ARG LAMBDA_TASK_ROOT=/var/task
WORKDIR ${LAMBDA_TASK_ROOT}
ARG PACKAGE_NAME

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.14 \
  PACKAGE_NAME=${PACKAGE_NAME}

FROM base as builder
RUN pip install poetry==$POETRY_VERSION
COPY poetry.lock pyproject.toml ./
# install dependencies
RUN poetry lock && \
poetry export -f requirements.txt --without-hashes > ./requirements.txt && \
pip install -r requirements.txt --target ./bundle
COPY $PACKAGE_NAME/ ./$PACKAGE_NAME

FROM base AS app
COPY --from=builder ${LAMBDA_TASK_ROOT}/$PACKAGE_NAME/ ./
COPY --from=builder ${LAMBDA_TASK_ROOT}/bundle/ ./
#run main script through lambda TODO change for other packages
CMD ["main.lambda_handler"]
