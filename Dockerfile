# Use an official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Create app directory
WORKDIR /

# Copy project files
COPY ./ /

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
