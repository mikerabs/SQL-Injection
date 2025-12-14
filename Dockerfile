FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY python/ /app/python/
COPY config/ /app/config/

CMD ["python", "/app/python/app.py"]
