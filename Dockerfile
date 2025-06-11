FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r base.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8000"] 