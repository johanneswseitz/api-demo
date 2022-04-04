# api-demo

## Requirements

* Python 3.10 (e.g. via brew)
* [pipenv](https://pipenv.pypa.io/)
* sqlite3

## Getting startet

1. Prepare environment: `pipenv shell`
1. Install dependencies: `pipenv install`
1. Create Admin user: `python manage.py createsuperuser`
1. Run server: `python manage.py runserver`
    * Fleet Management API: http://localhost:8000/swagger
    * Django Admin: http://localhost:8000/admin