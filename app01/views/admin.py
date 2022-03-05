
from django.shortcuts import render, redirect
from django import forms
from django.core.validators import ValidationError

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootstrapModelForm
from app01.utils.encrypt import md5

def adminList(request):
    data_dict = {}
    search_data = request.GET.get('q', '')  # 获取搜索框输入数据
    # 存入信息至dict
    if search_data:
        data_dict['username__contains'] = search_data

    queryset = models.Admin.objects.filter(**data_dict).all()
    # 分页组件
    page_obj = Pagination(request, queryset)

    content = {
        'queryset': page_obj.page_queryset,
        'page_string': page_obj.html(),
        'search_data': search_data,
    }

    return  render(request, 'admin_list.html', content)

class AdminModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.Admin

        fields = '__all__'
        widgets = {
            'password':forms.PasswordInput(render_value=True)
        }
    # md5加密
    def clean_password(self):
        password = self.cleaned_data['password']
        return md5(password)



    # 定义钩子方法实现密码确认的验证
    def clean_confirm_password(self):

        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data['confirm_password'])
        # print(password, confirm_password)

        if password != confirm_password:
            raise ValidationError('密码不一致')

        return confirm_password


def adminAdd(request):


    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'change.html', {'title': '添加管理员', 'form': form,})
    # post验证，存入
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {'title': '添加管理员', 'form': form,})

class AdminEditModelForm(BootstrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']

def adminEdit(request, nid):
    row_obj = models.Admin.objects.filter(id=nid).first()
    if request.method == 'GET':
        if not row_obj:
            return redirect('/admin/list/')
        form = AdminEditModelForm(instance=row_obj)
        return render(request, 'change.html',{'form':form, 'title':'编辑管理员'})

    form = AdminEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    return render(request, 'change.html', {'form':form, 'title':'编辑管理员'})


def adminDelete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


class AdminResetModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(render_value=True))
    class Meta:
        model = models.Admin
        fields = ['password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }
    # md5加密，并实现密码不能与上次密码相同
    def clean_password(self):
        password_md5 = md5(self.cleaned_data['password'])
        exists = models.Admin.objects.filter(id=self.instance.pk, password=password_md5).exists()
        if exists:
            raise ValidationError('不能和上次密码相同')
        return password_md5

    # 定义钩子方法实现密码确认的验证
    def clean_confirm_password(self):

        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data['confirm_password'])
        # print(password, confirm_password)

        if (password) and (password != confirm_password):
            raise ValidationError('密码不一致')

        return confirm_password

def adminPasswordReset(request, nid):
    """ 管理员密码重置 """
    row_obj = models.Admin.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'change.html',{'title':'管理员密码重置', 'form':form})
    form = AdminResetModelForm(data=request.POST,instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html',{'title':'管理员密码重置', 'form':form})