#!/usr/bin/env python3
import os
import cgi

from jinja2 import Environment, PackageLoader

from urls import URLS


HTTP = {
    200: '200 OK',
    404: '404 NOT FOUND',
}



def get(func):
    pass

def post(func):
    pass

packagedir = os.getcwd().split('/')[-1]
env = Environment(loader=PackageLoader('urls', ''))
def render(temp, context={}):
    template = env.get_template(temp)
    return template.render(**context)

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
#    post_content = environ.get('wsgi.input').read(content_length) if content_length != 0 else None
    print(type(content_length), content_length)
#    print(post_content)
    print(request_method, path, queries)

    form = None
    if request_method == 'POST' and content_length != 0:
        form = cgi.FieldStorage(fp=environ.get('wsgi.input'), environ=environ)
        post_data = {k: form.getvalue(k) for k in form.keys()}
        print(post_data)

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

