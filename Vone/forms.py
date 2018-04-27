from django import forms
from django.forms import widgets
from .models import UserInfo
from django.core.exceptions import ValidationError


# 注册表单
class RegForm(forms.Form):
    user = forms.CharField(label="用户名：", min_length=4,
                           widget=widgets.TextInput(attrs={"class": "form-control"})
                           )
    pwd = forms.CharField(label="密码：", min_length=4,
                          widget=widgets.PasswordInput(attrs={"class": "form-control"})
                          )
    repeat_pwd = forms.CharField(label="重复密码：", min_length=4,
                                 widget=widgets.PasswordInput(attrs={"class": "form-control"})
                                 )
    email = forms.EmailField(label="邮箱",
                             widget=widgets.EmailInput(attrs={"class": "form-control"})
                             )
    """
        下面是对注册页面字段的一些校验
        django的局部钩子，源码定义过clean_%s 这样一个函数，这里相当于重写
        格式是固定的，一次只能校验一个字段
    """

    def clean_user(self):
        val = self.cleaned_data.get("user")
        print(val)
        ret = UserInfo.objects.filter(username=val)
        if not ret:
            return val
        else:
            raise ValidationError("该用户已经存在")

    # 这是一个全局钩子，可以获取cleaned_data 的数据
    def clean(self):
        if self.cleaned_data.get("pwd") == self.cleaned_data.get("repeat_pwd"):
            return self.cleaned_data
        else:
            raise ValidationError("两次密码不一致！")

