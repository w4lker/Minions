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
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
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

def user_profile(request):
    if request.session.get('username') != None:
        return render(request, 'webmanager/template/user_profile.html',{'username':request.session.get('username'),'page_title':'Userprofile'})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response

def user_edit(request):
    response = HttpResponse()
    if request.method == 'GET':
        if request.session.get('username') != None:
            return render(request,'webmanager/template/user_edit.html',{'page_title':'UserProfile',"username":request.session.get('username')})
        else:
            response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
            return response 
        
    elif request.method == 'POST':
        if request.session.get('username') != None:
            if request.POST['pass'] != '' and request.POST['new_pass'] != '' and request.POST['re_pass'] !='':
                if request.POST['new_pass'] != request.POST['re_pass']:
                    response.write('<html><script type="text/javascript">alert("请确定两次新密码一致!");</script></html>')
                    return response
                else:
                    uname = request.session.get('username')
                    user = Users.objects.get(username = uname)
                    if user.password == md5(request.POST['pass']).hexdigest():
                        user.password = md5(request.POST['new_pass']).hexdigest()
                        user.save()
                        response.write('<html><script type="text/javascript">alert("修改成功");window.location="/user_profile"</script></html>')
                        return response                         
                            
                    else:
                        response.write('<html><script type="text/javascript">alert("原密码错误!");window.location="/edit_profile"</script></html>')
                        return response    
            else:
                response.write('<html><script type="text/javascript">alert("请将表单填写完整!");window.location="/edit_profile"</script></html>')
                return response            
            
        else:
            response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
            return response                     
     
        
        
    
    
        