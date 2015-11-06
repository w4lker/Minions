#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.db import connection,transaction
from django.core import serializers
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
        rsp = {'code':0,'hint':''}
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
                        rsp['code'] = 1
                        rsp['hint'] = '修改成功'
                        #return response                         
                            
                    else:
                        rsp['hint'] = '原密码错误'
                        #return response    
            else:
                rsp['hint'] = '请将表单填写完整！'
                #return response            
            
        else:
            rsp['hint'] = '接头暗号：天王盖地虎,小鸡炖蘑菇!'
            response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
            #return response
        return JsonResponse(rsp)

def data_proxy(request):
    if request.session.get('username') != None:
        data = Proxydata.objects.all()
        return render(request, 'webmanager/template/data_proxy.html',{'page_title':'主页','proxydata':data})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response 

def data_details(request,param):
    if request.session.get('username') != None:
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
        mlist = Menu.objects.all()
        return render(request, 'webmanager/template/menu_list.html',{'page_title':'菜单列表','mlist':mlist})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response     

def menu_edit(request,param):
    if request.session.get('username') != None:
        if request.method == 'GET':
            menu = Menu.objects.get(id=param)
            fathermenu = Menu.objects.filter(fatherid=0)
            return render(request, 'webmanager/template/menu_edit.html',{"menu":menu,"action":"菜单编辑","fathermenu":fathermenu})
        elif request.method == 'POST':
            rsp = {'code':0,'hint':''}
            menu = Menu.objects.get(id=request.POST['id'])
            #titles = Menu.objects.exclude(id=request.POST['id']).values('title')
            menu.title=request.POST['title']
            menu.href=request.POST['href']
            menu.fatherid = request.POST['fatherid']
            print type(request.POST['fatherid'])
            if request.POST['fatherid'] == '0':
                fathername = '/'
            else:
                fathername = Menu.objects.get(id=request.POST['fatherid']).values('fathername')['fathername']
            menu.fathername= fathername
            print fathername
            menu.pri=request.POST['pri']
            menu.save()
            rsp['hint'] = '修改成功!'
            rsp['code'] = 1
            return JsonResponse(rsp)          
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response 

def menu_reload(request):
    if request.session.get('username') != None:
        mlist = {"1":"test","2":"test2"}
        
        data = serializers.serialize('json', Menu.objects.all())
        return JsonResponse(data,safe=False)
        #return render(request, 'webmanager/template/menu_list.html',{'page_title':'菜单列表','mlist':mlist})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response  
    
def menu_add(request):
    if request.session.get('username') != None:
        if request.method == 'GET':
            fathermenu = Menu.objects.filter(fatherid=0)
            return render(request, 'webmanager/template/menu_add.html',{"action":"菜单添加","fathermenu":fathermenu})
        elif request.method == 'POST':
            print request.POST['fatherid']
            rsp = {'code':0,'hint':''}
            if request.POST['fatherid'] == '0':
                fname = '/'
                h= '/'
            else:
                fname = Menu.objects.get(id=request.POST['fatherid']).title
                h = request.POST['href']
            try:
                menu = Menu(title=request.POST['title'],href=h,fatherid=request.POST['fatherid'],fathername=fname,pri=request.POST['pri'])
                menu.save()
            except Exception as e:
                rsp['hint'] = e.message
            else:
                rsp['code'] = 1
                rsp['hint'] = "添加成功！"
            finally:
                return JsonResponse(rsp)        
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response

def menu_del(request,param):
    if request.session.get('username') != None:
        menu = Menu.objects.get(id=param)
        if menu.fatherid == 0:
            submenu = Menu.objects.filter(fatherid=param)
            submenu.delete()
        menu.delete()
        rsp = {'code':1,'hint':"删除成功"}
        return JsonResponse(rsp)       
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response 

def vul_xss(request):
    if request.session.get('username') != None:
        xss = Xsscan.objects.raw('select * from webmanager_xsscan group by taskid')
        return render(request, 'webmanager/template/vul_xss.html',{'page_title':'XSS 扫描结果','xss':xss})
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response

def xss_poc(request,param):
    if request.session.get('username') != None:
        xss = Xsscan.objects.filter(taskid=param)
        return render(request, 'webmanager/template/xss_poc.html',{'page_title':'XSS PoC','xss':xss})     
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response 

def xss_del(request,param):
    if request.session.get('username') != None:
        xss = Xsscan.objects.filter(taskid=param)
        xss.delete()
        rsp = {'code':1,'hint':"删除成功"}
        return JsonResponse(rsp)       
    else:
        response = HttpResponse()
        response.write('<html><script type="text/javascript">alert("接头暗号：天王盖地虎,小鸡炖蘑菇!"); window.location="/login"</script></html>')
        return response 
    
    
    
    
        