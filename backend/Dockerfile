FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app

EXPOSE 8081

CMD ["gunicorn", "run:app", "-b", "0.0.0.0:8081", "--worker-class", "gthread", "--workers", "2"]
