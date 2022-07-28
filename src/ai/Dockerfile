FROM public.ecr.aws/lambda/python:3.9 AS base
WORKDIR /code

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0 \
  VIRTUAL_ENV=/.venv


FROM base as builder
RUN pip install poetry==$POETRY_VERSION
COPY poetry.lock pyproject.toml /code/
#create and activate virtual environment
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi
COPY . /code/
RUN poetry build --no-interaction

FROM base AS app
COPY --from=builder /code/dist/*.whl ./
COPY --from=builder /code/$VIRTUAL_ENV ./
# activate virtual environment
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install deepseasharcq
#run ai script through lambda
CMD ["deepseasharcq.main.lambda_handler"]