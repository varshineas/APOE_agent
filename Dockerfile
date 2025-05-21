FROM python:3.10-slim

# System deps
RUN apt-get update && apt-get install -y git gcc libsndfile1 ffmpeg

# Workdir
WORKDIR /app

# Python deps
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# App files
COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
