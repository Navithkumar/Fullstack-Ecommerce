FROM python:3.11-slim

# Install system dependencies for psycopg2 (Postgres)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Set Python path to include shared package
ENV PYTHONPATH=/shared:$PYTHONPATH

# Default command -> Production ready (Gunicorn)
CMD ["gunicorn", "user-backend.wsgi:application", "--bind", "0.0.0.0:8000"]
