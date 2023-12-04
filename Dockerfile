# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /orders-api
WORKDIR /orders-api

# Copy the requirements file into the container at /orders-api
COPY requirements.txt /orders-api/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /orders-api/requirements.txt

# Copy the app directory contents into the container at /orders-api
COPY ./app /orders-api/app
# Copy the .env file into the container at /orders-api
# COPY [".env", "/orders-api/.env"]
RUN --mount=type=secret, id=AWS_KEY cat /run/secrets/AWS_KEY > /orders-api/.env
RUN --mount=type=secret, id=AWS_SECRET cat /run/secrets/AWS_SECRET >> /orders-api/.env
RUN --mount=type=secret, id=AWS_REGION cat /run/secrets/AWS_REGION >> /orders-api/.env
RUN --mount=type=secret, id=AWS_BUCKET cat /run/secrets/AWS_BUCKET >> /orders-api/.env
RUN --mount=type=secret, id=DB_USER cat /run/secrets/DB_USER >> /orders-api/.env
RUN --mount=type=secret, id=DB_PASSWORD cat /run/secrets/DB_PASSWORD >> /orders-api/.env
RUN --mount=type=secret, id=DB_HOST cat /run/secrets/DB_HOST >> /orders-api/.env
RUN --mount=type=secret, id=DB_NAME cat /run/secrets/DB_NAME >> /orders-api/.env
RUN --mount=type=secret, id=JWT_ENCODING_KEY cat /run/secrets/JWT_ENCODING_KEY >> /orders-api/.env


# Make port 80 available to the world outside this container
EXPOSE 80

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]