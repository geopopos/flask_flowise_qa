# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port 5001 for the Flask app
EXPOSE 5001

# Set the environment variables for Flask and the API URL
ENV FLASK_APP=app.py

# Run the command to start the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]