micro.py
========

A work-in-progress WSGI microframework for Python. Don't use this
or anything.

Usage
-----

To start the local server, run

    python app.py


How to use
----------

## urls.py

Here you define a dictionary called URLS that contains a simple
path url as the key and a function in your app.py file as the
value. Regex is not yet supported, so only simple strings will
be matched.

Example:

    from app import *

    URLS = {
        # will call app.hello() when you visit localhost:8001/hello
        '/hello': hello, 
    }

## app.py

This file can be called anything as long as you import it in
urls.py. Here you can import micro, define your views and
start the server upon execution.

    import micro
    def hello(name=None):
        name if name is not none else 'Person'
        return 'Hello, %s' % name

    if __name__ == '__main__':
        micro.run_server()

Current Features
----------------

- Get requests and query parsing
- Simple pattern matching
- URL dict for routes

To Do
-----

- Post requests
- Regular expression matching
- Templating support for Jinja2
- Better http support

