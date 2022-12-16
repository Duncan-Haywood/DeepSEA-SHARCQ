FROM python:3.9
RUN pip install poetry
COPY poetry.lock pyproject.toml ./
# install dependencies
RUN poetry install
COPY deepseasharcq /deepseasharcq
CMD ["poetry", "run","uvicorn", "deepseasharcq.api:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]

