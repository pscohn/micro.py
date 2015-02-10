#!/usr/bin/env python3
import os
import re
import cgi

from jinja2 import Environment, PackageLoader, Markup
POST = {}
GET = {}

HTTP = {
    200: '200 OK',
    404: '404 NOT FOUND',
}



def get(view):
    GET[view.__name__] = view
    return view

def post(view):
    POST[view.__name__] = view
    return view

def static(filename):
    return Markup(loader.get_source(env, filename)[0])

packagedir = os.getcwd().split('/')[-1]
loader = PackageLoader('__init__', '')
env = Environment(loader=loader)
env.globals['static'] = static
def render(temp, context={}):
    if temp.endswith('.html'):
        template = env.get_template(temp)
        return template.render(**context)
    else:
        return temp

class Router:
    def __init__(self):
        self.urls = {}
    def add_routes(self, routes):
        self.urls.update(routes)

router = Router()
def wsgi_app(environ, start_response):
#    print('--------------------')
#    print('\n'.join(['%s: %s' % (k, v) for k, v in environ.items()]))

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

    status = HTTP[404]
    response = [bytes(status, encoding='utf-8')]

    if request_method == 'POST':
        current_views = POST
        data = post_data
    elif request_method == 'GET':
        current_views = GET
        data = queries
    print('current views:', current_views)

    if path in router.urls:
        status = HTTP[200]
        response = current_views[router.urls[path].__name__](data)
        print('calling %s' % current_views[router.urls[path].__name__])
        response = [bytes(response, encoding='utf-8')]
    else:
        #TODO improve this
        for k, v in router.urls.items():
            if '?' not in k:
                continue
            regex = re.compile(k)
            match = re.match(regex, path)
            if match:
                print('match at %s with regex %s' % (path, str(regex)))
                status = HTTP[200]
                arguments = {d: match.group(d) for d in match.groupdict() if match.group(d) is not None}
                print(arguments)
                print('calling %s' % current_views[router.urls[k].__name__])
                response = current_views[router.urls[k].__name__](data,**arguments)
                response = [bytes(response, encoding='utf-8')]
                break

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

