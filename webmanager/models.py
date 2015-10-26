from django.db import models
from django.utils import datetime_safe
# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=12)
    password = models.CharField(max_length=32)
    
    def __unicode__(self):
        return self.username

class Proxydata(models.Model):
    id = models.IntegerField(primary_key=True)
    status_code = models.IntegerField(null=True,blank=True)
    method = models.CharField(max_length=5)
    host = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    request = models.TextField()
    response = models.TextField(null=True)
    timestamp = models.FloatField()

class Setting(models.Model):
    id = models.IntegerField(primary_key=True)
    negative_type = models.CharField(max_length=100)
    sqlmap_srv = models.CharField(max_length = 30)
    
class Sqliscan(models.Model):
    id = models.IntegerField(primary_key=True)
    taskid = models.CharField(max_length=16)
    url = models.CharField(max_length=100)
    request = models.TextField()
    starttime = models.TimeField(auto_now_add=True)
    total = models.FloatField()
    status = models.CharField(max_length=15)
    
class Xsscan(models.Model):
    id = models.IntegerField(primary_key=True)
    taskid = models.CharField(max_length=16)
    target = models.CharField(max_length=100)
    heuristic = models.CharField(max_length=100)
    poc = models.CharField(max_length=50)
    browsers = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
class Menu(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20)
    href = models.CharField(max_length=50,blank=True,null=True)
    fatherid = models.IntegerField()
    fathername = models.CharField(max_length=20,blank=True,null=True)
    pri = models.IntegerField()
    
    
    

    
    

