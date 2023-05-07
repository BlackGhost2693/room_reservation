# Installation

0. Create a virtual environment and install project dependency packages
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

1. Set a secret for django project in `.env` file just like `.env.example`

2. To test or overview the application you need to change project debuge mode to `True` in the `.env` file. Otherwise you should pass static files directory to a webserver like nginx to serve them. [Here](https://github.com/amirayat/Django-Production-Stack) is a production ready docker template with right nginx configuration to lunch django on debuge `False`.

3. Follow this commands:
```bash
# create database
python manage.py migrate

# create superuser
python manage.py createsuperuser

# collect static files for production mode
python manage.py collectstatic

# load sample data
python manage.py loaddata sample_data.json

# run tests
python manage.py test

# run project in development mode
python manage.py runserver
```

4. Take look on bellow links to find API documentaion:
- http://127.0.0.1:8000/swagger/
- http://127.0.0.1:8000/redoc/