# Gunakan image Python
FROM python:3.10-slim

ENV PYTHONPATH=/app

WORKDIR /app

# Install netcat dan clean up cache
RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /app/

# Install dependency Python
RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["python","run.py"]