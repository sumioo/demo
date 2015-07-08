#coding:utf-8
import datetime
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
def mycompany(request):
    user_id=request.session['_auth_user_id']
    if request.method=='GET':
        company=Company.objects.filter(user_id=user_id)
        if company:
            company=company[0]
            job=Job.objects.filter(company_id=company.id)
            for item in job:
                job_apply_info=Apply_job.objects.filter(job_id=item.id).order_by('-create_date')
                item.job_apply_info=job_apply_info
            t=template.loader.get_template('mycompany.html')
            c=template.RequestContext(request,locals())
            html=t.render(c)
            return HttpResponse(html)
        else:
            form=Company_form()
            t=template.loader.get_template('mycompany.html')
            c=template.RequestContext(request,locals())
            html=t.render(c)
            return HttpResponse(html)
    else:
        form=Company_form(request.POST)
        if form.is_valid():
            form_data=form.cleaned_data
            company=Company.objects.filter(user_id=user_id)
            if company:
                company.update(**form_data)
            else:
                Company(user_id=user_id,**form_data).save()
            return HttpResponseRedirect('/mycompany')
        else:
            t=template.loader.get_template('repost.html')
            c=template.RequestContext(request,locals())
            html=t.render(c)
            return HttpResponse(html)
@login_required
def job(request):
    if request.method=='POST':
        form=Job_form(request.POST)
        user_id=request.session['_auth_user_id']
        if form.is_valid():
            form_data=form.cleaned_data
            company=Company.objects.filter(user_id=user_id)
            if company:
                company_id=company[0].id
                key_id=form_data['key_id']
                if key_id:
                    del form_data['key_id']
                    job=Job.objects.filter(company_id=company_id,id=key_id)
                    if job:
                        create_date=datetime.date.today().isoformat()
                        job.update(create_date=create_date,**form_data)
                        return HttpResponseRedirect('/mycompany/')
                    else:
                        return render_to_response('message.html',{'msg_subject':u'提交错误'})
                else:
                    del form_data['key_id']
                    create_date=datetime.date.today().isoformat()
                    Job(create_date=create_date,user_id=user_id,company_id=company_id,**form_data).save()
                    return HttpResponseRedirect('/mycompany/')
            else:
                return render_to_response('message.html',{'msg_subject':u'请先填写公司信息'})
        else:
            form_action_path='/mycompany/job/'
            t=template.loader.get_template('repost.html')
            c=template.RequestContext(request,{'form_action_path':form_action_path,'form':form})
            html=t.render(c)
            return HttpResponse(html)

@login_required
def alter_info(request,offset,info_type):    #修改公司或职位信息
    user_id=request.session['_auth_user_id']
    if request.method=='GET':
        if info_type=='company':
            company=Company.objects.filter(user_id=user_id).values()[0]
            form=Company_form(company)
            form_action_path='/mycompany/'
            t=template.loader.get_template('alter_info.html')
            c=template.RequestContext(request,locals())
            html=t.render(c)
            return HttpResponse(html)
        else:
            company_id=Company.objects.get(user_id=user_id).id
            job=Job.objects.filter(id=offset,company_id=company_id).values()[0]
            if job:
                job['key_id']=job['id']
                del job['id']
                form=Job_form(job)
                form_action_path='/mycompany/job/'
                t=template.loader.get_template('alter_info.html')
                c=template.RequestContext(request,locals())
                assert 1
                html=t.render(c)
                return HttpResponse(html)
            else:
                return render_to_response('message.html',{'msg_subject':u'无此职位信息'})


def search_job(request):
    if request.method=='GET':
        keyword=request.GET.get('kw','')
        work_place=request.GET.get('place','')
        educational=request.GET.get('ed','')
        search_result=Job.objects.filter(name__contains=keyword,work_place__contains=work_place,educational__contains=educational)
        for item in search_result:
            company=Company.objects.get(id=item.company_id).name
            item.company=company
        if educational:
            ed='&ed='+educational
        if work_place:
            place='&place='+work_place
        link='/search/job/?kw='+keyword
        t=template.loader.get_template('job_search_display.html')
        c=template.RequestContext(request,locals())
        html=t.render(c)
        return HttpResponse(html)

def job_display(request,offest):
    if request.method=='GET':
        from_page=request.GET.get('from',None)
        job=Job.objects.filter(id=offest)
        if job:
            job=job[0]
            company=Company.objects.get(id=job.company_id)
            t=template.loader.get_template('job_display.html')
            c=template.RequestContext(request,locals())
            html=t.render(c)
            return HttpResponse(html)
        else:
            return render_to_response('message.html',{'msg_subject':u'暂无此职位信息'})
@login_required
def job_apply_or_favorite(request,offest,action_type):
    if request.method=='GET':
        user_id=request.session['_auth_user_id']
        model={'apply_job':Apply_job,'favorite_job':Favorite_job}
        try:
            job_id=Job.objects.get(id=offest).id
            resume_id=Resume.objects.get(user_id=user_id).id
        except (Job.DoesNotExist,Resume.DoesNotExist),e:
            if e.message[0]=='J':
                return render_to_response('message.html',{'msg_subject':u'暂时没有这样的职位，操作失败'})
            else:
                return render_to_response('message.html',{'msg_subject':u'请先填写简历'})
        if action_type=='apply_job':
            model[action_type](user_id=user_id,job_id=job_id,resume_id=resume_id,create_date=datetime.date.today()).save()
            return render_to_response('message.html',{'msg_subject':u'申请成功'})
        else:
            model[action_type](user_id=user_id,job_id=job_id,create_date=datetime.date.today()).save()
            return render_to_response('message.html',{'msg_subject':u'收藏成功'})

@login_required
def job_apply_favorite_record(request):
    user_id=request.session['_auth_user_id']
    if request.method=='GET':
        apply_job=Apply_job.objects.filter(user_id=user_id).order_by('-create_date') #从职位表查询
        favorite_job=Favorite_job.objects.filter(user_id=user_id).order_by('-create_date')
        for item in apply_job:
            job=Job.objects.get(id=item.job_id)
            company=Company.objects.get(id=job.company_id)
            if item.feedback_id:
                feedback=Feedback.objects.get(id=item.feedback_id)
                item.feedback_date=feedback.send_date
                item.feedback_is_read=feedback.is_read
            item.job_name,item.job_create_date=job.name,job.create_date
            item.company_id,item.company_name=company.id,company.name
        for item in favorite_job:
            job=Job.objects.get(id=item.job_id)
            company=Company.objects.get(id=job.company_id)
            item.job_name=job.name
            item.company_id,item.company_name=company.id,company.name
        t=template.loader.get_template('job_apply_favorite_record.html')
        c=template.RequestContext(request,locals())
        html=t.render(c)
        return HttpResponse(html)

@login_required
def job_feedback(request):
    user_id=request.session['_auth_user_id']
    if request.method=='GET':
        t=template.loader.get_template('feedback.html')
        c=template.RequestContext(request,locals())
        html=t.render(c)
        return HttpResponse(html)
    else:
        form=Feedback_form(request.POST)
        if form.is_valid():
            form_data=form.cleaned_data
            try:
                apply_job=Apply_job.objects.get(id=form_data['key_id'])
                assert form_data['user_id']==apply_job.user_id and form_data['job_id']==apply_job.job_id
            except Apply_job.DoesNotExist,AssertionError:
                return render_to_response('message.html',{'msg_subject':u'数据错误，提交失败'})
            del form_data['key_id']
            feedback=Feedback(send_date=datetime.date.today(),**form_data)
            feedback.save()
            apply_job.feedback_id=feedback.id
            apply_job.save()
            return render_to_response('message.html',{'msg_subject':u'提交成功'})
        else:
            form_action_path='/job/feedback/'
            t=template.loader.get_template('repost.html')
            c=template.RequestContext(request,{'form_action_path':form_action_path,'form':form})
            html=t.render(c)
            return HttpResponse(html)

@login_required
def read_feedback(request,offset):
    user_id=request.session['_auth_user_id']
    if request.method=='GET':
        try:
            feedback=Feedback.objects.get(id=offset,user_id=user_id)
        except Feedback.DoesNotExist:
            return render_to_response('message.html',{'msg_subject':u'无此回执信息'})
        feedback.is_read=True
        feedback.save()
        t=template.loader.get_template('message.html')
        c=template.RequestContext(request,{'msg_subject':u'回执信息:','msg_content':feedback.content})
        html=t.render(c)
        return HttpResponse(html)

















