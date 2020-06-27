from django import forms

from captcha.fields import CaptchaField


class UserLoginForm(forms.Form):
    Username = forms.CharField(required=True)
    Password = forms.CharField(required=True, min_length=6)


class UserRegisterForm(forms.Form):
    Username = forms.CharField(required=True)
    Password = forms.CharField(required=True, min_length=6)
    rPassword = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={"Invalid": u'验证码错误'})


class UserPasswordForgetForm(forms.Form):
    Username = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={"Invalid": u'验证码错误'})


class UserPasswordResetForm(forms.Form):
    Username = forms.CharField(required=True)
    Password = forms.CharField(required=True)
    rPassword = forms.CharField(required=True,min_length=6)