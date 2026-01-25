FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get install -y gcc postgresql-client\
    && apt-get clean

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]