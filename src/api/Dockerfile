FROM python:3.9-slim-bullseye AS base
ARG PROD=FALSE
ARG PACKAGE_NAME=deepseasharcqapi
WORKDIR /code
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0 \
  VIRTUAL_ENV=./venv \
  PROD=$PROD  \
  PACKAGE_NAME=$PACKAGE_NAME


FROM base as builder
RUN pip install poetry==$POETRY_VERSION
COPY poetry.lock pyproject.toml ./
#create virtual environment
RUN python3 -m venv $VIRTUAL_ENV
# install dependencies
RUN poetry install $(test ! $PROD && echo "--no-dev") --no-interaction --no-ansi
COPY ./$PACKAGE_NAME/ ./$PACKAGE_NAME/
RUN poetry build --no-interaction

FROM base AS app
# copy all dependencies and the package itself from build stage
COPY --from=builder ./code/$VIRTUAL_ENV/ $VIRTUAL_ENV/
COPY --from=builder ./code/dist/*.whl ./
# COPY --from=builder ./ ./

# activate virtual environment
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# install package into venv
RUN pip install ./*.whl

#run ai script
ENV S3_BUCKET=None
CMD python3 -m deepseasharcqapi.main_api