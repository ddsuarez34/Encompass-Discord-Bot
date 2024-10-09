# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port if necessary (not needed for Discord bots, but useful for API services)
# EXPOSE 8000

# Set the command to run your application
CMD ["python", "main.py"]
