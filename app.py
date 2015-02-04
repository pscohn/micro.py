#!/usr/bin/env python3
import micro

def hello(name=None):
    name = name if name is not None else 'Asshole'
    return 'Hello, %s' % name 

def home():
    form = '<form name="firstform" method="post" action="/result">'
    form += '<input type="text" name="name" />'
    form += '<input type="submit" name="submit" value="Submit" />'
    form += '</form>'
    return form

def result(name):
    return name

def paul():
    return 'paul\'s homepage'

if __name__ == '__main__':
    micro.run_server()
