#coding:utf-8
from django.shortcuts import render_to_response
from django import template
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.contrib.auth.models import User
from models import *
from forms import *
from utils import *
# Create your views here.
def login(request):
    if request.method == 'GET':
        t=template.loader.get_template('login.html')
        f=Login_form()
        c=template.RequestContext(request,{'form':f})
        html=t.render(c)
        return HttpResponse(html)
    else:
        f=Login_form(request.POST)
        if f.is_valid():
            login_info=f.cleaned_data
            user=auth.authenticate(username=login_info['username'],password=login_info['password'])
            if user is not None and user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect('/')
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

def index(request):
    if request.user.is_authenticated():
        login=1
    t=template.loader.get_template('index.html')
    c=template.Context(locals())
    html=t.render(c)
    return HttpResponse(html)


def myresume(request):
    user_id=is_login(request)
    if request.method=='GET':
        resume=Resume.objects.filter(user_id=user_id)
        print user_id,'****'
        if resume:
            import glob
            a=resume.values()
            resume=resume[0]
            work_experience=Work_experience.objects.filter(resume_id=resume.id)
            study_experience=Study_experience.objects.filter(resume_id=resume.id)
            resume_image=glob.glob(('D:/SVN/demo/lagou/static/%s.*' %resume.user_id))[0].split
        else:
            resume=None
        t=template.loader.get_template('myresume.html')
        c=template.RequestContext(request,locals())
        html=t.render(c)

        assert 1
        return HttpResponse(html)
    else:
        form_id=request.POST.get('form_id','1')
        print request.POST,'\n'
        select_form={'1':Resume_form,'2':Work_experience_form,'3':Study_experience_form}
        select_model={'1':Resume,'2':Work_experience,'3':Study_experience}
        form=select_form[form_id](request.POST)
        print form.errors
        if form.is_valid():
            form_clean=form.cleaned_data
            print form_clean,'\n'
            del form_clean['form_id']
            if form_clean['key_id']:                    #key_id为表主键id，避免与内建名相同
                form_clean['id']=form_clean['key_id']   #表行已存在，更新操作
                del form_clean['key_id']
            else:
                del form_clean['key_id']                #表行不存在，插入操作
                form_clean['id']=None
            assert 1
            model=select_model[form_id]()
            for k,v in form_clean.items():
                setattr(model,k,v)
            model.save()
            return HttpResponse('done')
        else:
            return HttpResponse('false')


def image(request):
    if request.method=='POST':
        user_id=request.session.get('_auth_user_id')
        form=Image_form(request.POST,request.FILES)
        if form.is_valid():
            if request.FILES['upfile'].size > 100000:
                form.errors['upfile']="file's size is over 100000bytes"
                return HttpResponseRedirect('/myresume/')
            else:
                file_name=upload_file_handle(request.FILES['upfile'],user_id)
                resume=Resume.objects.filter(user_id=user_id)

                return HttpResponse('done')



    else:
        pass
    return HttpResponse('vvv')



def search_resume(request):
    if request.method=='GET':
        link=request.get_full_path()
        keyword=request.GET.get('kw','')
        city=request.GET.get('city','')
        education=request.GET.get('ed','')
        search_result=Resume.objects.filter(tag__contains=keyword,city__contains=city,education__contains=education)
        t=template.loader.get_template('search_display.html')
        c=template.Context({'search_result':search_result,'keyword':keyword,'link':link})
        html=t.render(c)
        return HttpResponse(html)


def resume_display(request,offset):
    if request.method=='GET':
        resume=Resume.objects.filter(id=offset)
        if resume:
            import glob
            resume=resume[0]
            work_experience=Work_experience.objects.filter(resume_id=offset)
            study_experience=Study_experience.objects.filter(resume_id=offset)
            resume_image=glob.glob(('D:/SVN/demo/lagou/static/%s.*' %resume.user_id))[0]
        else:
            resume=None
        t=template.loader.get_template('resume_display.html')
        c=template.Context(locals())
        html=t.render(c)
        return HttpResponse(html)

