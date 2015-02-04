#!/usr/bin/env python3
from urls import URLS

import cgi

HTTP = {
    200: '200 OK',
    404: '404 NOT FOUND',
}


def wsgi_app(environ, start_response):
    print('--------------------')
    print('\n'.join(['%s: %s' % (k, v) for k, v in environ.items()]))

    query = environ.get('QUERY_STRING', None)
    query_list = query.split('&') if query != '' else None
    if query_list is not None:
        query_list = [q.split('=') for q in query_list]
        queries = {q[0]: q[1] for q in query_list}
    else:
        queries = {}

    request_method = environ.get('REQUEST_METHOD', None)
    path = environ.get('PATH_INFO', None)
    content_length = environ.get('CONTENT_LENGTH', '')
    content_length = int(content_length) if content_length != '' else 0
    print(type(content_length), content_length)
    print(environ.get('wsgi.input').read(content_length))
    print(request_method, path, queries)


    form = None
    if request_method == 'POST':
        form = cgi.FieldStorage(environ.get('wsgi.input').read(content_length))
        print(form) 

    if path in URLS:
        status = HTTP[200]
        response = URLS[path](**queries)
        response = [bytes(response, encoding='utf-8')]
    else:
        status = HTTP[404]
        response = [bytes(status, encoding='utf-8')]

    headers = [('Content-type', 'text/html; charset=utf-8')] 
    start_response(status, headers)
    return response

def run_server():
    from wsgiref.simple_server import make_server
    port = 8001
    httpd = make_server('', port, wsgi_app)
    print('serving on port %s' % port)
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()

