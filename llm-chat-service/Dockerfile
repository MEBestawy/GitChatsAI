FROM python:3.11-slim AS llm-chat-api-prod

WORKDIR /app/src

RUN apt-get update &&\
    apt-get install -y git curl

COPY ./requirements.txt ../requirements.txt
COPY src/ .

RUN pip install --no-cache-dir --upgrade -r ../requirements.txt

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]

FROM llm-chat-api-prod AS llm-chat-api-dev

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]