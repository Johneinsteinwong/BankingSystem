FROM python:3.11-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

RUN mkdir data
COPY src/*.py .
COPY tests/ ./tests
COPY pytest.ini .

CMD ["python", "main.py"]