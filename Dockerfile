# Use the official Python image as the base image for the container
FROM python:3.12

# Set the working directory to /app in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /

# Install the required packages from the requirements file and remove the cache to reduce the image size
RUN pip3 install --no-cache-dir -r /requirements.txt


# Copy the application code to the container at /app
COPY ./predikit/ /app/predikit/
COPY ./backend/ /app/backend/

# Set the environment variable PYTHONOPTIMIZE=2 to remove the assert statements and __debug__-dependent statements
# ENV PYTHONOPTIMIZE=2

# Set the environment variable PYTHONOPTIMIZE=1 to remove the assert statements
ENV PYTHONOPTIMIZE=1

# Set the environment variable PYTHONUNBUFFERED=1 to avoid buffering of the standard output
ENV PYTHONUNBUFFERED=1

# Enter the backend directory
WORKDIR /app/backend

# Expose the port 5001 to the host machine
EXPOSE 5001

# Run the application when the container launches
ENTRYPOINT ["python", "-O","server.py"]

