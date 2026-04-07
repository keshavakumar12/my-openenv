FROM python:3.11-slim

WORKDIR /app

COPY Requirements.txt .

RUN pip install --no-cache-dir -r Requirements.txt

COPY server/ ./server/

WORKDIR /app/server

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]