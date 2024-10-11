# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ..

# Install the required packages
RUN pip install --no-cache-dir .

# Make the script executable
RUN chmod +x /app/devaralan

# Command to run the application
ENTRYPOINT ["devaralan"]

CMD ["-h"]
