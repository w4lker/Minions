#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.db import connection,transaction
from webmanager.models import *
from hashlib import md5
import sys
import re
import urllib2
import gzip
import StringIO
import string
import base64
# Create your views here.
@csrf_protect

def login(request):
    return render(request, 'webmanager/template/login.html')

def index(request):
    if request.session.get('username') != None:
        menus = Menu.objects.order_by('pri').all()
        for menu in menus:
            print menu.title
        return render(request, 'webmanager/template/indexa.html',{'page_title':'主页','menus':menus})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response  

def index_page(request):
    if request.session.get('username') != None:
        return render(request, 'webmanager/template/index_page.html',{'page_title':'主页'})
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
        res = {'code':0,'hint':''}
        if request.session.get('username') != None:
            if request.POST['pass'] != '' and request.POST['new_pass'] != '' and request.POST['re_pass'] !='':
                if request.POST['new_pass'] != request.POST['re_pass']:
                    res['hint'] = '请确定两次新密码一致!'
                    response.write('<html><script type="text/javascript">alert("请确定两次新密码一致!");</script></html>')
                    #return response
                else:
                    uname = request.session.get('username')
                    user = Users.objects.get(username = uname)
                    if user.password == md5(request.POST['pass']).hexdigest():
                        user.password = md5(request.POST['new_pass']).hexdigest()
                        user.save()
                        res['code'] = 1
                        res['hint'] = '修改成功'
                        response.write('<html><script type="text/javascript">alert("修改成功");window.location="/user_profile"</script></html>')
                        #return response                         
                            
                    else:
                        res['hint'] = '原密码错误'
                        response.write('<html><script type="text/javascript">alert("原密码错误!");window.location="/edit_profile"</script></html>')
                        #return response    
            else:
                res['hint'] = '请将表单填写完整！'
                response.write('<html><script type="text/javascript">alert("请将表单填写完整!");window.location="/edit_profile"</script></html>')
                #return response            
            
        else:
            res['hint'] = '接头暗号：天王盖地虎,小鸡炖蘑菇!'
            response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
            #return response
        return JsonResponse(res)

def data_proxy(request):
    if request.session.get('username') != None:
        #return render(request, 'webmanager/template/data_proxy.html',{'page_title':'主页'})
        data = Proxydata.objects.all()
        return render(request, 'webmanager/template/data_proxy.html',{'page_title':'主页','proxydata':data})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response 

def data_details(request,param):
    if request.session.get('username') != None:
        #return render(request, 'webmanager/template/data_proxy.html',{'page_title':'主页'})
        data = Proxydata.objects.get(id=param)
        return render(request, 'webmanager/template/data_detail.html',{'page_title':'主页','request':data.request,'response':data.response})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response     
    
def data_replay(request):
    print request.POST['request']
    response = http_request(request.POST['request'])
    data = {'response':''}
    data['response'] = response
    return JsonResponse(data)    

def data_split(data):
    r_content=re.compile(r'\n\n(.*)')
    r_url=re.compile(r'\s(.*)\sHTTP/1')
    r_headers=re.compile(r'(.+):\s(.+)')
    url = re.findall(r_url,data)
    header = {}
    headers = re.findall(r_headers,data)
    for h in headers:
        header[h[0]] = h[1]
    content = re.findall(r_content,data)
    if content == []:
        content = ['']   
    
    request = {}
    request['url'] = url[0]    #正则匹配返回的是list，取出其中字符串的值
    request['header'] = header
    request['content'] = content[0]
    return request

def http_request(data):
    request = data_split(data)
    try:
        req = urllib2.Request(url= request['url'],headers=request['header'],data=request['content'])
        rsp = urllib2.urlopen(req)
        code = rsp.code
        msg = rsp.msg
        headers = rsp.headers
        if rsp.info().get('Content-Encoding') == 'gzip':
            data = StringIO.StringIO(rsp.read())
            gzip.GzipFile()
            content = gzip.GzipFile(fileobj=data).read()
        else:
            content = rsp.read()
    except urllib2.HTTPError,e:
        code = e.code
        msg = e.msg
        headers = e.headers
        content = e.read()
    except urllib2.URLError,e:
        response = e.reason
        return response
    response = '''HTTP/1.1 %d %s\n%s\n\n%s''' % (code,msg,headers,content)
    return response

def ajax_test(request):
    print request
    response = {'test':'123'}
    return JsonResponse(response)


def menu_list(request):
    if request.session.get('username') != None:
        #return render(request, 'webmanager/template/data_proxy.html',{'page_title':'主页'})
        mlist = Menu.objects.all()
        return render(request, 'webmanager/template/menu_list.html',{'page_title':'菜单列表','mlist':mlist})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response     

def menu_edit(request,param):
    if request.session.get('username') != None:
        Menu = Menu.objects.get(id=param)
        return render(request, 'webmanager/template/data_detail.html',{'page_title':'主页','request':data.request,'response':data.response})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response     
    
    
        