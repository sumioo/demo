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

# Create your views here.
def login(request):
    if request.method == 'GET':
        t=template.loader.get_template('login.html')
        f=Login_form()
        c=template.RequestContext(request,{'form':f})
        html=t.render(c)
        return HttpResponse(html)
    else:
        query_str=request.META['QUERY_STRING']
        query_str=query_str if query_str !='' else 'next=/'
        next_path=extract_path_arg(query_str)['next']
        f=Login_form(request.POST)
        if f.is_valid():
            login_info=f.cleaned_data
            user=auth.authenticate(username=login_info['username'],password=login_info['password'])
            if user is not None and user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect(next_path)
            else:
                t=template.loader.get_template('login.html')
                c=template.RequestContext(request,{'form':f,'login_error':1})
                html=t.render(c)
                return HttpResponse(html)
        else:
            t=template.loader.get_template('login.html')
            c=template.RequestContext(request,{'form':f})
            html=t.render(c)
            return HttpResponse(html)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
def signup(request):
    if request.method == 'GET':
        t=template.loader.get_template('signup.html')
        f=Signup_form()
        print f['username'].label_tag
        c=template.RequestContext(request,{'form':f})
        html=t.render(c)
        return HttpResponse(html)
    else:
        f=Signup_form(request.POST)
        if f.is_valid():
            sign_info=f.cleaned_data
            user=User.objects.create_user(username=sign_info['username'],password=sign_info['password'],email=sign_info['email'])
            is_hr=Is_HR(user_id=user.id,is_hr=sign_info['identity'])
            is_hr.save()
            return HttpResponse('signup success')
        else:
            t=template.loader.get_template('signup.html')
            c=template.RequestContext(request,{'form':f})
            html=t.render(c)
            return HttpResponse(html)
