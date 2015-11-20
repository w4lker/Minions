"""manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static  
from django.conf import settings  

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login$','webmanager.views.login',name='login'),
    url(r'^index_page','webmanager.views.index_page',name='page'),
    url(r'^index','webmanager.views.index',name='login'),
    url(r'^login/check','webmanager.views.login_check',name='login1'),
    url(r'^login/out','webmanager.views.login_out',name='login1'),
    url(r'^test','webmanager.views.test',name='login1'),
    url(r'^user/edit','webmanager.views.user_edit',name='login1'),
    url(r'^user/profile','webmanager.views.user_profile',name='login1'),
    url(r'^data/proxy','webmanager.views.data_proxy',name='login1'),
    url(r'^data/replay','webmanager.views.data_replay',name='login1'),
    url(r'^data/details/(\d+)/$','webmanager.views.data_details',name='login1'),
    url(r'^settings/menu/list$','webmanager.views.settings_menu_list',name='settings'),
    url(r'^settings/menu/edit/(\d*)','webmanager.views.settings_menu_edit',name='settings'),
    url(r'^settings/menu/add','webmanager.views.settings_menu_add',name='settings'),
    url(r'^settings/menu/del/(\d*)','webmanager.views.settings_menu_del',name='settings'),
    url(r'^settings/modules/list$','webmanager.views.settings_modules_list',name='settings'),
    url(r'^settings/modules/edit$','webmanager.views.settings_modules_edit',name='settings'),
    url(r'^vul/xss/list$','webmanager.views.vul_xss_list',name='vul'),
    url(r'^vul/xss/poc/(.{32})','webmanager.views.vul_xss_poc',name='vul'),
    url(r'^vul/xss/del/(.{32})','webmanager.views.vul_xss_del',name='vul'),
    url(r'^vul/sqli/list$','webmanager.views.vul_sqli_list',name='vul'),
    url(r'^vul/sqli/del/(.{16})','webmanager.views.vul_sqli_del',name='vul'),
    url(r'^ajax_test$','webmanager.views.ajax_test',name='login1'),
    url(r'^\s?\s?$','webmanager.views.index',name='login'),
]

urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)  