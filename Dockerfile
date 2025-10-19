# Base image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Run Gunicorn server
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]