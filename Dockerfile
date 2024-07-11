# Use an official Python runtime as a parent image
FROM python:3.11.4-slim-buster

# Install ODBC 17 driver dependencies
RUN apt-get update && apt-get install -y gnupg2 curl unixodbc-dev

# Add Microsoft ODBC 17 repository and install ODBC 17 driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Install npm packages
RUN npm install

# Run npm build scripts
RUN npm run build:css && npm run build:js

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
