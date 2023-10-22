FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y git

RUN git config --global url."https://$GIT_USERNAME:$GIT_TOKEN@github.com/".insteadOf "https://github.com/"

COPY ./requirements.txt requirements.txt
COPY ./api.py api.py
COPY utils/ utils/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]