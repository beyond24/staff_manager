from app01 import models
from app01.utils.bootstrap import BootstrapModelForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms

class UseModelForm(BootstrapModelForm):
    name = forms.CharField(min_length=2,label='姓名')
    password = forms.CharField(min_length=3, label='密码') #单独定义form对象
    class Meta:
        model = models.Staff
        fields = ['name', 'password', 'age', 'acount', 'create_time', 'gender', 'depart']


class PrettyModelForm(BootstrapModelForm):
    # 第一种方式数据校验，重写form字段+正则
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )
    class Meta:
        model = models.PrettyNum
        # fields = ['mobile','price',]
        fields = '__all__'  # 意为所有字段
        # exclude = ['level'] # 排除某一字段
    # 第二种方式进行数据校验，钩子方法实现手机号重复的验证
    def clean_mobile(self):
        txt_moible = self.cleaned_data['mobile']
        exists =  models.PrettyNum.objects.filter(mobile=txt_moible).exists()
        if exists:
            raise ValidationError('该手机号已经存在')
        return txt_moible


class PrettyEditModelForm(BootstrapModelForm):
    """"单独定义editform方便限制修改"""
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )
    # mobile = forms.CharField(disabled=True, label='手机号')
    class Meta:
        model = models.PrettyNum
        fields = '__all__'
    # 钩子方法实现重复验证，但要排除自身
    def clean_mobile(self):
        txt_id = self.instance.pk # 当前id
        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.exclude(id=txt_id).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('该手机号已经存在')
        return txt_mobile

