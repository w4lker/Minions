from django.db import models

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

class Proxysetting(models.Model):
    id = models.IntegerField(primary_key=True)
    negative_type = models.CharField(max_length=100)
    

