from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    username = forms.CharField(label='用户名')
    email = forms.EmailField(label='邮件地址')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='密码')
    username.widget.attrs['class'] = 'form-control'
    email.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
