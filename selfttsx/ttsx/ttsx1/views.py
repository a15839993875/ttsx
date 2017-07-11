#coding:utf-8
from django.shortcuts import render,redirect
from models import *
from hashlib import sha1
from django.http import JsonResponse
import datetime
from middleware import *
from user_decorators import *
# Create your views here.

def register(request):
    context = {'title':'注册','top':'0'}
    return render(request,'ttsx/register.html',context)

def register_handle(request):
    #接收数据
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('user_pwd')
    umail=post.get('user_email')
    #加密
    s1=sha1()
    s1.update(upwd)
    upwd_sha1=s1.hexdigest()
    #创建对象
    user=UserInfo()
    user.uname=uname
    user.upwd=upwd_sha1
    user.umail=umail
    user.save()
    #完成后转向
    return redirect('/user/login/')

def register_valid(request):
    uname=request.GET.get('uname')
    result=UserInfo.objects.filter(uname = uname).count()
    context={'valid':result}
    return JsonResponse(context)

def login(request):
    uname=request.COOKIES.get('uname','')
    context={'title':'登录','uname':uname,'top':'0'}
    return render(request,'ttsx/login.html',context)

def login_handle(request):
    uname = request.POST.get('username')
    upwd = request.POST.get('pwd')
    name_jz = request.POST.get('name_jz','1')
    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()
    context = {'title': '登录', 'uname': uname, 'upwd': upwd, 'top': '0'}
    result = UserInfo.objects.filter(uname = uname)
    if len(result) == 1:
        if result[0].upwd == upwd_sha1:
            request.session['uid'] = result[0].id
            request.session['uname'] = uname
            path =  request.session.get('url_path','/')
            response = redirect(path)
            if name_jz == '2':
                response.set_cookie('uname',uname,expires=datetime.datetime.now() + datetime.timedelta(days = 7))
            else:
                response.set_cookie('uname','',max_age=-1)
            return response
        else:#密码错误
            context['pwd_error'] = '1'
            return render(request, 'ttsx/login.html',context)
    else:#账号错误
        context['name_error'] = '1'
        return render(request,'ttsx/login.html',context)

def logout(request):
    request.session.flush()
    return redirect('/user/login/')
@user_login
def center(request):
    user= UserInfo.objects.get(pk = request.session['uid'])
    context = {'title':'用户中心','user':user}
    return render(request,'ttsx/center.html',context)
@user_login
def order(request):
    user = UserInfo.objects.get(pk=request.session['uid'])
    context = {'title':'用户订单','user':user}
    return render(request,'ttsx/order.html',context)
@user_login
def site(request):
    user=UserInfo.objects.get(pk=request.session['uid'])
    if request.method=='POST':
        post=request.POST
        user.ushou=post.get('ushou')
        user.uaddress=post.get('uaddress')
        user.ucode=post.get('ucode')
        user.uphone=post.get('uphone')
        user.save()
    context={'title':'收货地址','user':user}
    return render(request,'ttsx/site.html',context)














