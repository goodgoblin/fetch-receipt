FROM --platform=linux/amd64 python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose API port
EXPOSE 8000

# runs the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
