#!/usr/bin/env python3
from app import *
from micro import router

URLS = {
    '/': home,
    '/paul/?$': paul,
    '/paul/(?P<page>\d+?)/?$': paul,
    '/hello': hello,
    '/result': result,
    '/vr/?$': game,
    '/vr/(?P<page>\d+?)/?$': game,
    '/elon/?': elon,
    '/elon/(?P<page>\d+)/?': elon,
}

router.add_routes(URLS)

if __name__ == '__main__':
    main()

