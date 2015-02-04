#!/usr/bin/env python3
from app import *

URLS = {
    '/': home,
    '/paul': paul,
    '/hello': hello,
    '/result': result,
}

if __name__ == '__main__':
    main()

