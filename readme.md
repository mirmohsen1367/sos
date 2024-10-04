
## Django Central API Service Integration Guide

## PYTHON VERSION
    Python 3.10 or higher versions.

### Installation of the Django App Locally

To get started with the Django application locally, follow these steps:

#### a) Requirements

- Ensure you have Python installed (preferably Python 3.10 or above).
- Install pip and virtualenv if you haven't already.

#### b) Setting Up the Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

#### c) Set environment variables from .env.sample.
    SECRET_KEY=
    ALLOWED_HOSTS=127.0.0.1
    SETTINGS=
    DEBUG=
    DB=
    DB_HOST=
    DB_PORT=
    DB_NAME=
    DB_USER=
    DB_PASSWORD=


#### d) Run in development mode.

    Please set SETTINGS=sos_test.settings.local in the .env file.

    Please create a logs folder in the root directory and set up separate logging for debug, warning, and query messages.


#### e) Run Migrations

```bash
python manage.py migrate
```

#### f) Run Test

```bash
pytest
```
#### g) Create new user and login and test api

```bash
python manage.py createsuperuser
```

#### h) For run on docker

    docker compose up
