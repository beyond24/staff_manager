from django.shortcuts import render, redirect

from app01 import models
from app01.utils.forms import PrettyModelForm, PrettyEditModelForm
from app01.utils.pagination import Pagination


def prettyList(request):
    """ 靓号列表 """

    data_dict = {}
    search_data = request.GET.get('q', '')  # 获取搜索框输入数据

    # 存入信息至dict
    if search_data:
        data_dict['mobile__contains'] = search_data

    # select * from [tableName] by level desc;
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by('-level')

    # 实例化分页组件
    page_obj = Pagination(request, queryset)

    context = {
        'queryset': page_obj.page_queryset,
        'page_string': page_obj.html(), #生成的HTML string
        'search_data': search_data, # 搜索框的数据
    }
    return render(request, 'pretty_list.html', context)



def prettyAdd(request):
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form':form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_add.html', {'form': form})


def prettyEdit(request, nid):
    row_obj = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = PrettyEditModelForm(instance=row_obj)
        return render(request, 'pretty_edit.html', {'form':form})
    form = PrettyEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_edit.html', {'form': form})

def prettyDelete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')