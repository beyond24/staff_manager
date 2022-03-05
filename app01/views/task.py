import json
from django import forms
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app01.utils.pagination import Pagination

from app01 import models
from app01.utils.bootstrap import BootstrapModelForm


class TaskModelForm(BootstrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            # "detail": forms.Textarea,
            "detail": forms.TextInput
        }



def taskList(request):
    """ 任务列表 """
    queryset = models.Task.objects.all().order_by('-id')
    form = TaskModelForm()
    page_obj = Pagination(request, queryset)
    content = {
        'queryset': page_obj.page_queryset,
        'form': form,
        'page_string': page_obj.html()
    }
    return render(request, "task_list.html", content)

@csrf_exempt
def taskAdd(request):

    # print(request.POST)

    # 1.用户发送过来的数据进行校验（ModelForm进行校验）
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status": False, 'error': form.errors}
    # print(json.dumps(data_dict, ensure_ascii=False))
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))