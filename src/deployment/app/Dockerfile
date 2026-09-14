FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/deployment/app/streamlit_app.py ./src/deployment/app/streamlit_app.py

EXPOSE 8501

CMD ["streamlit", "run", "src/deployment/app/streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]