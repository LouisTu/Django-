from django import forms
from django.contrib.auth.models import User
from .models import UserProfile,UserInfo


# 登入表单
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# 注册表单
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

    # 是一个内部类，声明表单的内容会写入到User的数据库表中的指定记录里
    class Meta:
        model = User
        fields = ('username','email')

    # 检查用户所输入的两个密码是否一致，以"clean_属性名称"的命名方式所创建的方法，都有类似的功能
    def clean_password2(self):
        formdata = self.cleaned_data
        if formdata['password'] != formdata['password2']:
            raise forms.ValidationError("passwords don't match.")
        return formdata['password2']


# 增加注册项目表单
class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('phone', 'birth')


# 用户信息表单
class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ('school', 'company', 'address', 'aboutme', 'profession', 'photo')


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email',)
