worker: python worker.py
web: gunicorn app:app --log-file=-
heroku ps:scale web=1
heroker ps:scale worker=1
