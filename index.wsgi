#coding:utf-8
import sae

from demo import wsgi

application = sae.create_wsgi_app(wsgi.application)
