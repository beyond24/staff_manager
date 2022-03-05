from django.shortcuts import render, redirect, HttpResponse
from django import forms
from io import BytesIO

from app01.utils.bootstrap import BootstrapForm, BootstrapModelForm
from app01.utils.encrypt import md5
from app01.utils.code import check_code
from app01 import models

class LoginForm(BootstrapForm):
    username = forms.CharField(
        label = '用户名',
        widget = forms.TextInput,
    )
    password = forms.CharField(
        label = '密码',
        widget = forms.PasswordInput(render_value=True),
    )
    code = forms.CharField(
        label = '验证码',
        widget = forms.TextInput(),
    )
    # 钩子方法将输入框所得密码md5方便与数据库对照
    def clean_password(self):
        password_md5 = md5(self.cleaned_data['password'])
        return password_md5

def login(request):
    if request.method == 'GET':
        form  = LoginForm()
        return render(request, 'login.html',{'form':form})
    # post验证，存入数据库
    form = LoginForm(data=request.POST)
    if form.is_valid():
        #1.验证验证码是否正确
        input_code = form.cleaned_data.pop('code')
        correct_code = request.session.get('code') # 超时获得空字符串返回None
        if not correct_code:
            form.add_error('code', '验证码已超时')
            return render(request, 'login.html', {'form': form})
        if input_code.upper() != correct_code.upper():
            form.add_error('code', '验证码输入有误')
            return render(request, 'login.html', {'form': form})

        # 2.去数据库查找用户
        admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_obj:
            # 若没有找到用户
            form.add_error('password', '用户名或密码错误') # 为form.password追加错误
            return render(request, 'login.html', {'form': form})
        # 用户名和密码正确，写入session
        request.session['info'] = {
            'id': admin_obj.id,
            'username': admin_obj.username
        }
        # 设置用户的session时间
        request.session.set_expiry(60*60*24*7)


        return redirect('/staff/list/')
    # 数据校验失败重新输入
    return render(request, 'login.html',{'form':form})

def logout(request):
    """ 用户注销 """
    # 清除用户session并重定向
    request.session.clear()
    return redirect('/login/')

def imageCode(request):
    """ 生成图片验证码"""
    img, code_string = check_code()
    print(code_string)
    # 将正确的验证码存到session中，并设置30s有效时间
    request.session['code'] = code_string
    request.session.set_expiry(30)

    # 将验证码写如内存，并返还
    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())