release: python manage.py migrate
web: gunicore habit_tracker.wsgi
worker: celery -A habit_tracker worker