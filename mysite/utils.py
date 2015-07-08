import os,datetime
from django.http import HttpResponse,HttpResponseRedirect

def upload_file_handle(f,user_id):
    from sae.storage import Bucket
    bucket=Bucket('image')
    bucket.put()
    file_postfix=f.name.split('.')[-1]
    file_name=str(user_id)+'.'+file_postfix
    bucket.put_object(file_name, f.read())
    return 'http://sumioo-image.stor.sinaapp.com/'+file_name

def is_login(request):
    if request.session.get('_auth_user_id',''):
        return True
    return False

def extract_path_arg(query_str):
    arg=query_str.split('&')
    key,value=[],[]
    for i in arg:
        n,m=i.split('=')
        key.append(n)
        value.append(m)
    return dict(zip(key,value))

def is_overdue(date):
    if isinstance(date,datetime.date):
        if date<datetime.date.today():
            return True
        else:
            return False
    else:
        raise TypeError,'agr must be a datetime.date instance'
