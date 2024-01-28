# Using lightweight alpine image
FROM python:3.8-alpine

# Installing packages
RUN apk update

# Defining working directory and adding source code
WORKDIR /usr/src
COPY requirements.txt bootstrap.sh openapi.json ./
COPY src ./src

# Install API dependencies
RUN pip install -r requirements.txt

# Start app
EXPOSE 5000
ENTRYPOINT ["/usr/src/bootstrap.sh"]