# Use the official Python base image
FROM python:3.13.0

# Set the working directory inside the container
WORKDIR /code

# install dependencies
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get -y install libpq-dev

# Copy the requirements file to the working directory
COPY ./requirements.txt /code/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy the application code to the working directory
COPY ./app /code/app

# Expose the port on which the application will run
EXPOSE 8080

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
