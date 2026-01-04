FROM python:3.11-slim

WORKDIR /app

# Força o log a aparecer em tempo real
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "consumer.py"]