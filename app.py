#!/usr/bin/env python3
from micro import render, get, post, run_server
from models import User, Filter, FilterItem, Entry

def hello(name='Asshole'):
    return 'Hello, %s' % name 

@get
def home(request):
    return render('more-templates/form.html', {'name': 'name'})

@post
def home(request):
    return render(request[name])

def result():
    return 'result'

def paul(page=1):
    return 'paul\'s homepage number %s' % page


user = User()
user.id = 26
user.username = 'paul'
user.unread_only = False

class Paginator:
    def __init__(self, page, has_next):
        self.page = page
        self.previous_page_number = page - 1
        self.next_page_number = page + 1
        self.has_next = has_next

    @property
    def has_previous(self):
        return self.page > 1


def make_filter(queries, page):
    articles = []
    limit = 10
    offset = limit * page - limit

    filters = [Filter.get(user=user, name=query) for query in queries]
    articles += FilterItem.get_articles(filter_=filters, limit=limit, offset=offset)
    articles = filter(lambda x: x is not None, articles)
    next_articles = FilterItem.get_articles(filter_=filters, limit=1, offset=offset+limit)

    if len(next_articles) < 1:
        has_next = False
    else:
        has_next = True

    paginator = Paginator(page, has_next)
    #TODO problem with multiple queries, will get 30 articles for limit 10.
    #     should change sql to get all queries together
#    pager = Paginator()
    return render('templates/home.html', {'blots_all': articles, 'filter_keywords':', '.join(queries), 'paginator':paginator})

@get
def game():
    return make_filter(['vr','oculus', 'virtual reality'], int(page))

def elon(page=1):
    return make_filter(['elon musk'], int(page))


from micro import router

URLS = {
    '/': home,
    '/paul/': paul,
    '/paul/(?P<page>\d+?)/?$': paul,
    '/hello/?(?P<name>\w+)?/?': hello,
    '/result': result,
    '/vr/?$': game,
    '/vr/(?P<page>\d+?)/?$': game,
    '/elon/?': elon,
    '/elon/(?P<page>\d+)/?': elon,
}

router.add_routes(URLS)

if __name__ == '__main__':
    run_server()
