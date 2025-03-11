FROM python:3.13.2

# Set working directory
WORKDIR /app

# Copy requirements file first to leverage Docker caching
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose the required port
EXPOSE 8080

# Define the command to run the application
CMD ["python", "main.py"]

