# Gunakan image Python
FROM python:3.10-slim

ENV PYTHONPATH=/app

WORKDIR /app

RUN pip install redis

COPY . /app/

# Install dependency Python
RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["python","run.py"]