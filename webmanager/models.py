from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=12)
    password = models.CharField(max_length=32)
    
    def __unicode__(self):
        return self.username