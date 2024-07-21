# Pharmacy Management System

Welcome to a simple pharmacy management system. Currently, it utilizes Django's default admin portal.

## Installation

### Requirements

- Python > 3.10
- Node.js

### Clone Repository

Clone the Pre-Production branch of the repository:

bash

    git clone https://github.com/Hassan-V/DjangoPharma.git


### Set up a Python virtual environment (Recommended):
  For Windows:
    
    python3 -m venv any-env-name-you-want
    ./any-env-name-you-want/scripts/activate
  
  For Linux

    python3 -m venv any-env-name-you-want
    source ./any-env-name-you-want/bin/activate

### Install Python packages:
    
    pip install -r requirements.txt

### Install Node packages:

    npm install

### Setup Envirnment Variables for Database:

Create a file named .env in the project root and add the following lines. Remove the angle brackets (<>) when configuring the variables.

For MS SQL Server (set as default):

    DATABASE_NAME=<Name of the Database>
    DATABASE_USER=<Username of the database user>
    DATABASE_PASSWORD=<Password for the aforementioned user>
    DATABASE_HOST=<IP / Domain / URL of Database Host>
    DATABASE_PORT=<Port of the Database Server>

for any other db you must change the ENGINE variable in the settings. py accordingly and configure the envirnment variables accordingly
refer to the official documentation for more information
    
    https://docs.djangoproject.com/en/5.0/ref/databases/

### Run Django migrations and collect static files:

    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py collectstatic

### Run JS bundling and Tailwind CSS compilation scripts:

    npm run build:css
    npm run build:js

### Start the Django development server:

    python3 manage.py runserver


### To Do
Check out system

Auxiliary User Models
