#coding:utf-8
from django.shortcuts import render_to_response
from django import template
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.contrib.auth.models import User
from mysite.models import *
from mysite.forms import *
from mysite.utils import *

def index(request):
    if request.user.is_authenticated():
        login=1
    resume=Resume.objects.all()
    company=Company.objects.all()
    job=Job.objects.all()
    user=User.objects.all()
    username=request.user.username
    t=template.loader.get_template('index.html')
    c=template.Context(locals())
    html=t.render(c)
    return HttpResponse(html)
