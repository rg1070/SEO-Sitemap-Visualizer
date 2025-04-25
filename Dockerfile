# Dockerfile
FROM python:3.13.2

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY backend/ backend/
COPY frontend/ frontend/

# Set PYTHONPATH so "backend" becomes importable
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Start the app
CMD ["python", "backend/app.py"]
