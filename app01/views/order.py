import random
from datetime import datetime

from app01 import models
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app01.utils.forms import BootstrapModelForm
from app01.utils.pagination import Pagination


class OrderModelForm(BootstrapModelForm):
    class Meta:
        model = models.Order
        exclude = ['oid', 'admin']


def orderList(request):
    form = OrderModelForm
    queryset = models.Order.objects.all().order_by('-id')
    page_obj = Pagination(request, queryset)

    content = {
        'form': form,
        'queryset': page_obj.page_queryset,
        'page_string': page_obj.html()
    }

    return render(request, 'order_list.html', content)


@csrf_exempt
def orderAdd(request):
    """ 新建订单ajax """
    form = OrderModelForm(data=request.POST)
    # 生成oid
    form.instance.oid = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999))
    # 根据session生成admin_id
    form.instance.admin_id = request.session['info'].get('id')
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'errors': form.errors})


def orderDelete(request):
    uid = request.GET.get('uid')
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({'status': False, 'errors': '删除失败，该数据已经不存在！'})
    # 成功
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})


def orderDetails(request):
    uid = request.GET.get('uid')
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({'status': False, 'errors': '编辑失败，该数据已经不存在！'})

    row_dict = models.Order.objects.filter(id=uid).values('title', 'price', 'status').first()

    return JsonResponse({'status': True, 'data': row_dict})

@csrf_exempt
def orderEdit(request):
    uid = request.GET.get('uid')
    exists = models.Order.objects.filter(id=uid).exists()

    if not exists:
        return JsonResponse({'status': False, 'tips': '编辑失败，该数据已经不存在！'})
    row_obj = models.Order.objects.filter(id=uid).first()
    form = OrderModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'errors': form.errors})
