release: python manage.py migrate --noinput
web: gunicorn django_chat.wsgi --log-file -
web2: daphne chat.routing:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channel_layer -v2