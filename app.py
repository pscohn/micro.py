#!/usr/bin/env python3
import micro

def hello(name=None):
    name = name if name is not None else 'Asshole'
    return 'Hello, %s' % name 

def home():
    return micro.render('templates/form.html', {'name': 'name'})


def result():
    return 'result'

def paul():
    return 'paul\'s homepage'

if __name__ == '__main__':
    micro.run_server()
