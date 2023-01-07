release: python manage.py migrate
web: gunicorn habit_tracker.wsgi
worker: celery -A habit_tracker worker