from django.shortcuts import render, redirect

from app01 import models
from app01.utils.pagination import Pagination


def departList(request):
    """ 部门列表 """
    # queryset = [对象， 对象， 对象]
    queryset = models.Department.objects.all()
    page_obj = Pagination(request, queryset, 2)
    content = {
        'queryset': page_obj.page_queryset,
        'page_string': page_obj.html()
    }
    return render(request, 'depart_list.html', content)

def departAdd(request):
    if request.method == 'GET':
        return render(request, 'depart_add.html')
    # 若为post，获取用户输入数据
    title = request.POST.get('title')
    # 保存到数据库
    models.Department.objects.create(title=title)
    # 重定向到list页面
    return redirect('/depart/list/')

def departDelete(request):
    """ 删除部门 """
    #get删除 127.0.0.1:8000/depart/delete/#?nid=1
    nid = request.GET.get('nid')
    # 从数据库删除
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart/list/')

def departEdit(request, nid):
    """ 编辑部门 """
    if request.method =='GET':
        row_obj = models.Department.objects.filter(id=nid).first()
        obj_title = models
        return render(request, 'depart_edit.html', {'row_obj':row_obj})
    # 若为form post的提交
    title = request.POST.get('title')
    # 根据id找到数据并update
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")
