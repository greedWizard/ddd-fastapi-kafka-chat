FROM python:3.12.1-slim-bullseye as builder

RUN python -m pip install poetry==1.8.2

COPY poetry.lock pyproject.toml ./

RUN poetry export -o requirements.txt --without-hashes

FROM python:3.12.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev

WORKDIR /app

EXPOSE 8000

COPY --from=builder requirements.txt ./

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY /app/ /app/**

CMD ["uvicorn", "--factory", "application.api.main:create_app", "--timeout-graceful-shutdown", "2", "--host", "0.0.0.0", "--port", "8000"]
