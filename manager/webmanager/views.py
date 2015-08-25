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
    if request.session.get('username') != None:
        return render(request, 'webmanager/template/index2.html',{'page_title':'主页'})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎!"); window.location="/login"</script></html>')
        return response        

def login_check(request):
    user = Users.objects.get(id=1)
    uname = request.POST['username']
    response = HttpResponse()
    pwd = md5(request.POST['password']).hexdigest()
    request.POST['password']
    try:
        user = Users.objects.get(username = uname)
    except:
        response.write('<html><script type="text/javascript">alert("暗号都记不住，你丫还搞啥革命呀！"); window.location="/login"</script></html>')
        return response
    if user.password == pwd:
        request.session['username'] = uname
        return HttpResponseRedirect('/index')
    else:
        response.write('<html><script type="text/javascript">alert("暗号都记不住，你丫还搞啥革命呀！"); window.location="/login"</script></html>')
        return response  

def login_out(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return HttpResponseRedirect('/login')

def test(request):
    request.breadcrumbs([(("homepage"),'/'),  
                         (("activity"),'/activity/')  
                         ])  
    return render(request,'webmanager/template/test.html', {'page_title':'just4test'})      
        
    
    
        