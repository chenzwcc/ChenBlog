# coding=utf8

from django import forms
from users.models import UserProfile

from captcha.fields import CaptchaField


class RegisterForm(forms.Form):
    # 自定义表单验证
    username = forms.CharField(required=True,max_length=30)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=5,max_length=20)
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误'})

class LoginForm(forms.Form):
    # 自定义登陆表单验证
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ModifyPwdForm(forms.Form):
    Password1 = forms.CharField(required=True, min_length=6, max_length=20)
    Password2 = forms.CharField(required=True, min_length=6, max_length=20)



class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['img']


class UserInfoForm(forms.Form):
    class Meta:
        model=UserProfile
        fields=['username', ]