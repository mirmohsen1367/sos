
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



#### e) Run Migrations

```bash
python manage.py migrate
```

#### d) Run Test

```bash
pytest
```
#### e) Create new user and login and test api

```bash
python manage.py createsuperuser
```

#### f) For run on docker

    docker compose up
