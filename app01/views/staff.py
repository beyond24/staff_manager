from django.shortcuts import render, redirect

from app01 import models
from app01.utils.forms import UseModelForm
from app01.utils.pagination import Pagination


def staffList(request):
    """ 用户列表 """
    queryset = models.Staff.objects.all()
    # for obj in queryset:
    #     # datetime转化为str
    #     print(obj.create_time.strftime('%Y-%m-%d'))
    #     # 直接使用choices中的value
    #     print(obj.get_gender_display())
    #     # 直接使用外键关联 obj.depart为关联的对象
    #     print(obj.depart.title)

    page_obj = Pagination(request, queryset, 3)
    content = {
        'queryset': page_obj.page_queryset,
        'page_string': page_obj.html()
    }
    return render(request, 'staff_list.html', content)

def staffAdd(request):
    """ 添加用户 """
    if request.method == 'GET':
        content = {
        'gender_choices': models.Staff.gender_choices,
        'depart_list': models.Department.objects.all(), # queryset类型

    }
        # print(models.Department.objects.all())
        return render(request, 'staff_add.html', content)
    # 若为post获取数据
    name = request.POST.get('name')
    password = request.POST.get('password')
    age = request.POST.get('age')
    acount =  request.POST.get('acount')
    create_time  = request.POST.get('create_time')
    gender_id = request.POST.get('gender')
    depart_id = request.POST.get('depart')

    # 存入数据库
    models.Staff.objects.create(name=name, password=password, age=age, acount=acount, create_time=create_time, gender=gender_id, depart_id=depart_id)
    return redirect('/staff/list')




def staffModelFormAdd(request):
    """ 基于modelform的添加用户 """
    if request.method == 'GET':
        # 实例化对象
        form = UseModelForm()
        return render(request, 'staff_modelform_add.html', {'form': form})
    # post提交数据,数据校验
    form = UseModelForm(data=request.POST)
    # 数据合法，存入数据库
    if form.is_valid():
        form.save()
        return redirect('/staff/list/')
    # 校验失败在页面显示错误信息
    return render(request, 'staff_modelform_add.html', {'form': form})

def staffEdit(request, nid):
    """ 编辑员工 """
    row_obj = models.Staff.objects.filter(id=nid).first()

    if request.method == 'GET':
        # 根据ID去数据库获得需要的一行数据
        form = UseModelForm(instance=row_obj)
        return render(request, 'staff_edit.html', {'form':form})
    # post修改
    form = UseModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/staff/list/')
    return render(request, 'staff_edit.html', {'form':form})

def staffDelete(request, nid):
    models.Staff.objects.filter(id=nid).delete()
    return redirect('/staff/list/')
