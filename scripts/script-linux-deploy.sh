# Service Linux Debug
# http://127.0.0.1:5000

# gunicorn 
gunicorn -w 4 -b 0.0.0.0:5000 "app:app"
