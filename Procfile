web: gunicorn vAPI.wsgi
worker: ./manage.py createsuperuser --email admin@g.com --username admin
worker: ./manage.py makemigrations; ./manage.py migrate
