# JCHAT

## Setup

Make sure you are having virtualenv (`virtualenv` or `virtualenvwrapper`)

Create a virtualenv and activate then run in terminal

```
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata sites
./manage.py runserver
```

Channels change django in multiprocess model. We don't run everything in a wsgi server.
Runserver will work as worker server where django runs actual logic and asgi server will work as interface server that's capapble of serving websockets.

Install asgi server 
```
pip install asgi_redis

```
Run asgi-server and django runserver 
```
asgi-server
python manage.py runserver
```
Browse on 127.0.0.1:8000
