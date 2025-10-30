FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends build-essential             && pip install --no-cache-dir -r requirements.txt             && apt-get remove -y build-essential             && apt-get autoremove -y             && rm -rf /var/lib/apt/lists/*
COPY app.py .
COPY model.joblib .
COPY metrics.json .
EXPOSE 5000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4"]
