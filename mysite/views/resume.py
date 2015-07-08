#coding:utf-8
from django.shortcuts import render_to_response
from django import template
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from mysite.models import *
from mysite.forms import *
from mysite.utils import *

# Create your views here.

@login_required
def myresume(request):
    if request.method=='GET':
        user_id=request.session['_auth_user_id']
        resume=Resume.objects.filter(user_id=user_id)
        if resume:
            resume=resume[0]
            work_experience=Work_experience.objects.filter(resume_id=resume.id)
            study_experience=Study_experience.objects.filter(resume_id=resume.id)
        else:
            resume=None
        t=template.loader.get_template('myresume.html')
        c=template.RequestContext(request,locals())
        html=t.render(c)
        return HttpResponse(html)
    else:
        user_id=request.session['_auth_user_id']
        form=Resume_form(request.POST)
        if form.is_valid():
            form_data=form.cleaned_data
            resume=Resume.objects.filter(user_id=user_id)
            if resume:
                resume.update(**form_data)
            else:
                Resume(user_id=user_id,**form_data).save()
            return HttpResponseRedirect('/myresume/')
        else:
            t=template.loader.get_template('repost.html')
            c=template.RequestContext(request,{'form_action_path':'/myresume/','form':form})
            html=t.render(c)
            return HttpResponse(html)

@login_required
def experience(request,form_name,model_name):
    if request.method=='POST':
        experience_type={   'w_form':Work_experience_form,
                            'w_model':Work_experience,
                            's_form':Study_experience_form,
                            's_model':Study_experience
                        }
        form=experience_type[form_name](request.POST)
        model=experience_type[model_name]
        user_id=request.session['_auth_user_id']
        if form.is_valid():
            form_data=form.cleaned_data
            resume=Resume.objects.filter(user_id=user_id)
            if resume:
                resume_id=resume[0].id
                key_id=form_data['key_id']
                if key_id:
                    experience=model.objects.filter(resume_id=resume_id,id=key_id)
                    if experience:
                        del form_data['key_id']
                        experience.update(**form_data)
                        return HttpResponseRedirect('/myresume/')
                    else:
                        return render_to_response('message.html',{'msg_subject':u'提交错误'})
                else:
                    del form_data['key_id']
                    model(resume_id=resume_id,**form_data).save()
                    return HttpResponseRedirect('/myresume/')
            else:
                return render_to_response('message.html',{'msg_subject':u'请先填写基本简历信息'})
        else:
            form_action_path='/myresume'+request.path
            t=template.loader.get_template('repost.html')
            c=template.RequestContext(request,{'form_action_path':form_action_path,'form':form})
            html=t.render(c)
            return HttpResponse(html)




def image(request):
    if request.method=='POST':
        user_id=request.session.get('_auth_user_id')
        form=Image_form(request.POST,request.FILES)
        if form.is_valid():
            image_path=upload_file_handle(request.FILES['upimage'],user_id)
            resume=Resume.objects.filter(user_id=user_id).update(image_path=image_path)
            return HttpResponseRedirect('/myresume/')
        else:
            form_action_path='/myresume'+request.path
            t=template.loader.get_template('repost.html')
            c=template.RequestContext(request,{'form_action_path':form_action_path,'form':form,
                                                'enctype':'multipart/form-data'})
            html=t.render(c)
            return HttpResponse(html)



def search_resume(request):
    if request.method=='GET':
        keyword=request.GET.get('kw','')
        hope_city=request.GET.get('city','')
        education=request.GET.get('ed','')
        search_result=Resume.objects.filter(hope_work__contains=keyword,hope_city__contains=hope_city,education__contains=education)
        if education:
            ed='&ed='+education
        if hope_city:
            city='&city='+hope_city
        link='/search/resume/?kw='+keyword
        t=template.loader.get_template('resume_search_display.html')
        c=template.RequestContext(request,locals())
        html=t.render(c)
        return HttpResponse(html)


def resume_display(request,offset):
    if request.method=='GET':
        resume=Resume.objects.filter(id=offset)
        if resume:
            resume=resume[0]
            work_experience=Work_experience.objects.filter(resume_id=offset)
            study_experience=Study_experience.objects.filter(resume_id=offset)
            form=Feedback_form()
        else:
            resume=None
        t=template.loader.get_template('resume_display.html')
        c=template.RequestContext(request,locals())
        html=t.render(c)
        return HttpResponse(html)
