FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (none really needed for basic python, but good practice)
# RUN apt-get update && apt-get install -y --no-install-recommends ...

# Install python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Expose port
EXPOSE 8000

# Run
# Run
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}

