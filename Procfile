web: cd backend && gunicorn app:app --bind 0.0.0.0:$PORT
worker: cd frontend && serve -s build -l $PORT
