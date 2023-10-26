FROM python:3.11-slim AS repo-manager-api-prod

WORKDIR /app/src

RUN apt-get update && \
    apt-get install -y git

RUN git config --global url."https://$GIT_USERNAME:$GIT_TOKEN@github.com/".insteadOf "https://github.com/"

COPY ./requirements.txt ../requirements.txt
COPY src/ .

RUN pip install --no-cache-dir --upgrade -r ../requirements.txt

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]

FROM repo-manager-api-prod AS repo-manager-api-dev

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]