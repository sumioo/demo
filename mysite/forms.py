#coding:utf-8
from django import forms
from django.contrib.auth.models import User


error_messages = {
    'username':{
                'required': u'必须填写用户名',
                'max_length': u'用户名长度过长（3-12个字符）'
                },
    'email':{
            'required': u'必须填写E-mail',
            'max_length': u'Email长度有误',
            'invalid':u'请填写正确的邮箱地址'
            },
    'password': {
                'required': u'密码不能为空',
                'max_length': u'密码长度过长',
                'min_length':u'密码少于6个字符'
                },
    'date':{
            'invalid':u'日期格式不正确，正确格式：2015-1-1'

            },
    'text':{
            'max_length':u'文本长度超过最大值',
            'required':u'必须填写'
            },
    'image':{
            'empty':u'上传不能为空',
            'required':u'未选择任何照片'
            },
    'company_intfield':{
           'max_value':u'超过最大值100000',
           'min_value':u'人数不能小于0',
    },
    'job_intfield':{
           'max_value':u'超过最大值1000',
           'min_value':u'人数不能小于1',
    },
}

class Signup_form(forms.Form):
    username=forms.CharField(max_length=20,label=u"用户名",
        error_messages=error_messages.get('username'))
    password=forms.CharField(min_length=6,max_length=20,label=u'密码',widget=forms.PasswordInput,required=True,error_messages=error_messages.get('password'))
    repassword=forms.CharField(min_length=6,max_length=20,label=u'再次输入密码',widget=forms.PasswordInput,required=True,
        error_messages=error_messages.get('password'))
    email=forms.EmailField(max_length=20,label=u'邮箱',
        error_messages=error_messages.get('email'))
    identity=forms.BooleanField(label=u'注册为 HR?',initial=False,required=False)

    def clean_repassword(self):
        password=self.cleaned_data['password']
        repassword=self.cleaned_data['repassword']
        if  password != repassword:
            raise forms.ValidationError(u'密码不一致')
        return repassword
    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError(u'用户名已被注册')
        return username

class Login_form(forms.Form):
    #required_css_class='form-control'
    username=forms.CharField(max_length=20,label=u"用户名",
        error_messages=error_messages.get('username'))
    password=forms.CharField(max_length=20,label=u'密码',widget=forms.PasswordInput,error_messages=error_messages.get('password'))

class Resume_form(forms.Form):
    name=forms.CharField(max_length=255,label=u'姓名')
    city=forms.CharField(max_length=255,required=False,label=u'现居城市')
    mobilephone=forms.CharField(max_length=11,required=False,label=u'手机号码')
    email=forms.EmailField(max_length=75,required=False,label=u'邮箱地址',error_messages=error_messages.get('email'))
    hope_work=forms.CharField(max_length=255,required=False,label=u'期望工作')
    hope_type=forms.CharField(max_length=255,required=False,label=u'工作类型：全职/实习')
    hope_city=forms.CharField(max_length=255,required=False,label=u'期望工作城市')
    hope_salary=forms.CharField(max_length=255,required=False,label=u'期望薪资')
    education=forms.CharField(max_length=255,required=False,label=u'学历')
    description=forms.CharField(max_length=255,required=False,label=u'自我描述',widget=forms.Textarea)
    self_evaluate=forms.CharField(max_length=255,required=False,label=u'自我评价',widget=forms.Textarea)
    tag=forms.CharField(max_length=255,required=False,label=u'个人亮点')

class Work_experience_form(forms.Form):
    key_id=forms.CharField(max_length=10,label=u'id',widget=forms.HiddenInput,required=False)
    company_name=forms.CharField(max_length=255,required=False,label=u'公司名称')
    start_date=forms.DateField(required=False,widget=forms.DateInput,label=u'起始日期',error_messages=error_messages.get('date'))
    end_date=forms.DateField(required=False,widget=forms.DateInput,label=u'结束日期',error_messages=error_messages.get('date'))
    job=forms.CharField(max_length=255,required=False,label=u'工作岗位')
    description=forms.CharField(required=False,label=u'工作内容',widget=forms.Textarea)

class Study_experience_form(forms.Form):
    key_id=forms.CharField(max_length=10,label=u'id',widget=forms.HiddenInput,required=False)
    school_name=forms.CharField(max_length=255,required=False,label=u'学校名称')
    start_date=forms.DateField(required=False,label=u'起始日期')
    end_date=forms.DateField(required=False,label=u'结束日期')
    educational=forms.CharField(max_length=255,required=False,label=u'学历')
    subject=forms.CharField(max_length=255,required=False,label=u'专业')

class Company_form(forms.Form):
    name=forms.CharField(max_length=255,label=u'公司名字',error_messages=error_messages.get('text'))
    city=forms.CharField(max_length=255,required=False,label=u'所在城市')
    stage=forms.CharField(max_length=255,required=False,label=u'阶段')
    tag=forms.CharField(max_length=255,required=False,label=u'标签')
    people_num=forms.IntegerField(max_value=100000,min_value=0,required=False,label=u'人数',error_messages=error_messages.get('company_intfield'))
    home_url=forms.CharField(max_length=255,required=False,label=u'公司网址')
    description=forms.CharField(required=False,label=u'公司简介',widget=forms.Textarea)

class Job_form(forms.Form):
    key_id=forms.CharField(max_length=10,required=False,label=u'id',widget=forms.HiddenInput)
    name=forms.CharField(max_length=255,required=False,label=u'职位名称')
    work_place=forms.CharField(max_length=255,required=False,label=u'工作地点')
    num=forms.IntegerField(min_value=1,max_value=1000,required=False,label=u'招聘人数',error_messages=error_messages.get('job_intfield'))
    scal=forms.CharField(max_length=255,required=False,label=u'薪资')
    experience=forms.CharField(max_length=255,required=False,label=u'工作经验')
    educational=forms.CharField(max_length=255,required=False,label=u'学历')
    job_type=forms.CharField(max_length=255,required=False,label=u'工作类型：全职/实习')
    tag=forms.CharField(max_length=255,required=False,label=u'标签')
    description=forms.CharField(required=False,label=u'工作描述',widget=forms.Textarea)
    end_date=forms.DateField(required=False,label=u'过期时间',error_messages=error_messages.get('date'))

class Image_form(forms.Form):
    upimage=forms.ImageField(label=u'上传照片',error_messages=error_messages.get('image'))

    def clean_upimage(self):
        upimage=self.cleaned_data.get('upimage',False)
        if upimage:
            if upimage.size>2*1024*1024:
                raise ValidationError(u'上传照片超过2mb限制，请重新上传')
            else:
                return upimage
        else:
            raise ValidationError(u'上传失败')

class Feedback_form(forms.Form):
    key_id=forms.IntegerField(widget=forms.HiddenInput)
    user_id=forms.IntegerField(widget=forms.HiddenInput)
    job_id=forms.IntegerField(widget=forms.HiddenInput)
    content=forms.CharField(error_messages=error_messages.get('text'),widget=forms.Textarea,label=u'发送回执')


