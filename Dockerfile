# Use the official Python image
FROM python:3.8

# Set environment variables
ENV FLASK_APP=core/server.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Set the working directory
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the application code to the container
COPY . .

# Uncomment the following lines if you need to run database migrations during container build
# RUN flask db init -d core/migrations/
# RUN flask db migrate -m "Initial migration." -d core/migrations/
# RUN flask db upgrade -d core/migrations/

# Expose the port your app runs on
EXPOSE 5000

# Run Gunicorn when the container launches
CMD ["gunicorn", "-c", "gunicorn_config.py", "core.server:app"]
