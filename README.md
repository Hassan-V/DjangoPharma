# Pharmacy Management System

Welcome to a simple pharmacy management system. Currently, it utilizes Django's default admin portal.

## Installation

### Requirements

- Python > 3.10
- Node.js

### Clone Repository

Clone the Pre-Production branch of the repository:

bash

    git clone -b Pre-Production https://github.com/Shooooooter/DjangoPharma.git


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

### Run Django migrations and collect static files:

    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py collectstatic

### Run JS bundling and Tailwind CSS compilation scripts:

    npm run build:css
    npm run build:js

### Start the Django development server:

    python3 manage.py runserver
