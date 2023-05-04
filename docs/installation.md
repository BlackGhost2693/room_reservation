# Installation

Follow this commands:
```bash
# create database
python manage.py migrate

# create superuser
python manage.py createsuperuser

# load sample data
python manage.py loaddata sample_data.json

# run tests
python manage.py test

# run project in development mode
python manage.py runserver
```