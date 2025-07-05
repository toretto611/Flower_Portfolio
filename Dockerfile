# Use a lightweight Python image
FROM python:3.11

# Install PostgreSQL development libraries (needed for psycopg2-binary)
RUN apt-get update && apt-get install -y libpq-dev

# Expose Flask port (Flask's default is 5000)
EXPOSE 5000

# Prevent Python from writing .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turn off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies listed in requirements.txt
RUN python -m pip install -r requirements.txt

# Set the working directory inside the container
WORKDIR /app

# Copy the rest of the project files into the container
COPY . /app

# Run the Flask app (this will start the server inside the container)
CMD ["python", "app.py"]
