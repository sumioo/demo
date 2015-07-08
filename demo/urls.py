from django.conf.urls import patterns, include, url
from django.contrib import admin
from mysite.views import index,login,resume,job
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'demo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$',login.login),
    url(r'^accounts/logout/$',login.logout),
    url(r'^accounts/signup/$',login.signup),

    url(r'^$',index.index),

    url(r'^myresume/$',resume.myresume),
    url(r'^myresume/work-experience/$',resume.experience,{'form_name':'w_form','model_name':'w_model'}),
    url(r'^myresume/study-experience/$',resume.experience,{'form_name':'s_form','model_name':'s_model'}),
    url(r'^myresume/image/$',resume.image),
    url(r'^search/resume/',resume.search_resume),
    url(r'^resume/(\d{1,5})/$',resume.resume_display),

    url(r'^search/job/',job.search_job),
    url(r'^mycompany/$',job.mycompany),
    url(r'^mycompany/job/$',job.job),
    url(r'^mycompany/alter/company/$',job.alter_info,{'info_type':'company','offset':None}),
    url(r'^mycompany/alter/job/(\d{1,5})/$',job.alter_info,{'info_type':'job'}),
    url(r'^job/(\d{1,5})/$',job.job_display),
    url(r'^job/apply/(\d{1,5})/$',job.job_apply_or_favorite,{'action_type':'apply_job'}),
    url(r'^job/favorite/(\d{1,5})/$',job.job_apply_or_favorite,{'action_type':'favorite_job'}),
    url(r'^job/feedback/$',job.job_feedback),
    url(r'^myjob/$',job.job_apply_favorite_record),
    url(r'^apply/feedback/(\d{1,5})/$',job.read_feedback),
)
