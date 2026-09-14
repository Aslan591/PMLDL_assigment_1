FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/deployment/api/main.py ./src/deployment/api/main.py
COPY models/model.joblib ./models/model.joblib

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.deployment.api.main:app", "--host", "0.0.0.0", "--port", "8000"]