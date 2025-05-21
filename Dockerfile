FROM python:3.10-slim

WORKDIR /app

# System packages if needed
RUN apt-get update && apt-get install -y git

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY ./app /app

# Set up FastAPI app entrypoint
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000"]
