web: gunicorn goldenland.wsgi --timeout 15 --keep-alive 5 --log-file -
worker: celery -A goldenland worker --loglevel=info 
