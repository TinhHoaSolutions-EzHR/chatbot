# Use the official Python base image
FROM python:3.11.10-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port on which the application will run
EXPOSE 5000

# Run the application
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000" ]