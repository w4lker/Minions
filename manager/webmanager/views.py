#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.db import connection,transaction
from webmanager.models import Users
from hashlib import md5

# Create your views here.
@csrf_protect

def login(request):
    return render(request, 'webmanager/template/login.html')

def index(request):
    return render(request, 'webmanager/template/index1.html')

def login_check(request):
    user = Users.objects.get(id=1)
    uname = request.POST['username']
    response = HttpResponse()
    pwd = md5(request.POST['password']).hexdigest()
    request.POST['password']
    try:
        user = Users.objects.get(username = uname)
    except:
        response.write('<html><script type="text/javascript">alert("用户名或密码错误"); window.location="/login"</script></html>')
        return response
    if user.password == pwd:
        return HttpResponseRedirect('/index')
    else:
        response.write('<html><script type="text/javascript">alert("用户名或密码错误"); window.location="/login"</script></html>')
        return response        

        
    
    
        