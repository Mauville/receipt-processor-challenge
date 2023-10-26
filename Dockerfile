FROM python:latest
LABEL authors="Oscar Vargas"

EXPOSE 5000

# Use the latest official Python image from DockerHub
FROM python:latest

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the local project files into the container
COPY . .

# Install flask
RUN pip install --no-cache-dir flask

# The command to run when the container starts
CMD ["python", "main.py"]
