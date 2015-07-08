from django.db import models
from django.contrib.auth.models import User
import utils
# Create your models here.


class Resume(models.Model):
    user_id=models.PositiveIntegerField()
    name=models.CharField(max_length=255,null=True)
    description=models.CharField(max_length=255,null=True)
    tag=models.CharField(max_length=255,null=True)
    education=models.CharField(max_length=255,null=True)
    city=models.CharField(max_length=255,null=True)
    mobilephone=models.CharField(max_length=11,null=True)
    email=models.EmailField(max_length=75,null=True)
    self_evaluate=models.CharField(max_length=255,null=True)
    hope_work=models.CharField(max_length=255,null=True)
    hope_type=models.CharField(max_length=255,null=True)
    hope_city=models.CharField(max_length=255,null=True)
    hope_salary=models.CharField(max_length=255,null=True)
    image_path=models.CharField(max_length=255,null=True)

class Study_experience(models.Model):
    id=models.AutoField(primary_key=True)
    resume_id=models.PositiveIntegerField()
    school_name=models.CharField(max_length=255,null=True)
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)
    educational=models.CharField(max_length=255,null=True)
    subject=models.CharField(max_length=255,null=True)

class Work_experience(models.Model):
    id=models.AutoField(primary_key=True)
    resume_id=models.PositiveIntegerField()
    company_name=models.CharField(max_length=255,null=True)
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)
    job=models.CharField(max_length=255,null=True)
    description=models.TextField(null=True)

class Company(models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.PositiveIntegerField()
    name=models.CharField(max_length=255,null=True)
    city=models.CharField(max_length=255,null=True)
    stage=models.CharField(max_length=255,null=True)
    tag=models.CharField(max_length=255,null=True)
    people_num=models.PositiveIntegerField(null=True)
    home_url=models.URLField(max_length=200,null=True)
    description=models.TextField(null=True)

class Job(models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.PositiveIntegerField()
    company_id=models.PositiveIntegerField()
    category_path=models.CharField(max_length=255,null=True)
    name=models.CharField(max_length=255,null=True)
    work_place=models.CharField(max_length=255,null=True)
    num=models.PositiveIntegerField(null=True)
    scal=models.CharField(max_length=255,null=True)
    experience=models.CharField(max_length=255,null=True)
    educational=models.CharField(max_length=255,null=True)
    job_type=models.CharField(max_length=255,null=True)
    tag=models.CharField(max_length=255,null=True)
    description=models.TextField(null=True)
    create_date=models.DateField(null=True)
    end_date=models.DateField(null=True)

    def is_overdue(self):
        return utils.is_overdue(self.end_date)


class Feedback(models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.PositiveIntegerField()
    job_id=models.PositiveIntegerField()
    content=models.TextField(null=True)
    is_read=models.BooleanField(default=False)
    send_date=models.DateField(null=True)

class Apply_job(models.Model):
    id=models.AutoField(primary_key=True)
    job_id=models.PositiveIntegerField()
    user_id=models.PositiveIntegerField()
    feedback_id=models.PositiveIntegerField(null=True)
    resume_id=models.PositiveIntegerField()
    is_read=models.BooleanField(default=False)
    create_date=models.DateField(null=True)

class Favorite_job(models.Model):
    id=models.AutoField(primary_key=True)
    job_id=models.PositiveIntegerField()
    user_id=models.PositiveIntegerField()
    create_date=models.DateField(null=True)

class Is_HR(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(User)
    is_hr=models.BooleanField(default=False)
































