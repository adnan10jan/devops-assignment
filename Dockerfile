FROM python:3.11-slim

WORKDIR /app

# Install dependencies first for caching
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
