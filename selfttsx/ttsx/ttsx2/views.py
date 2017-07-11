#coding:utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    goods_list = []
    type_list = TypeInfo.objects.all()
    for t1 in type_list:
        nlist = t1.goodsinfo_set.order_by('-id')[0:4]
        clist = t1.goodsinfo_set.order_by('-gclick')[0:4]
        goods_list.append({'t1':t1,'nlist':nlist,'clist':clist})
    #查询分类对象
    #查询每个分类最新的4个商品
    #查询每个分类最火的4个商品
    context = {'title':'首页','glist':goods_list,'cart_show':'1',}
    return render(request,'ttsx2/index.html',context)

def goods_list(request,tid,pindex):
    try:
        t1 = TypeInfo.objects.get(pk = int(tid))
        new_list = t1.goodsinfo_set.order_by('-id')[0:2]
        glist = t1.goodsinfo_set.order_by('-id')
        paginator = Paginator(glist,15)
        pindex1 = int(pindex)
        if pindex1<1:
            pindex1 = 1
        elif pindex1>paginator.num_pages:
            pindex1 = paginator.num_pages
        page = paginator.page(pindex1)
        context = {'title':'商品列表','cart_show':'1','t1':t1,'new_list':new_list,'page':page}
        return render(request,'ttsx2/list.html',context)
    except:
        return render(request,'404.html')

def detail(request,tid,id):
    try:
        t1 = TypeInfo.objects.get(pk = int(tid))
        new_list = t1.goodsinfo_set.order_by('-id')[0:2]
        goods = t1.goodsinfo_set.get(pk=int(id))
        btitle = goods.gsubtitle
        gcontent = goods.gcontent
        context = {'title':'商品列表','cart_show':'1','new_list':new_list,'btitle':btitle,"gcontent":gcontent,'goods':goods}
        return render(request,'ttsx2/detail.html',context)
    except:
        return render(request, '404.html')

