from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm,  RegistrationForm, UserProfileForm, UserInfoForm, UserForm
from .models import User, UserInfo, UserProfile
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


# 登入
def user_login(request):
    # 处理前端提交方法为'POST'的数据，并支持前端的显示请求
    if request.method == 'POST':
        # 提交表单内容
        login_form = LoginForm(request.POST)
	# 验证传入的数据是否合法
        if login_form.is_valid():
            # 以键值对的形式记录用户名和密码
            cd = login_form.cleaned_data
            # 用authenticate()函数，检验此用户是否为本网站项目的用户以及密码是否正确
            user = authenticate(username=cd['username'], password=cd['password'])

            if user:
                # 用login()函数，并将所得到的user实例对象作为参数，实现用户登入
                login(request, user)
                return HttpResponse('Welcome you.You have been authenticated successfully')
            else:
                return HttpResponse('Sorry.Your username or password is not right.')
        else:
            return HttpResponse('Invalid login')

    if request.method == 'GET':
        login_form = LoginForm()
        return render(request,'account/login.html',{'form':login_form})


# 注册
def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid():
	    # 在参数中添加一个"commit=False"，使数据结果暂时不被写入到数据库，仅生成一个数据对象， 作用是为了防止数据写入到数据库后，在设置密码就需要重新写入
            new_user = user_form.save(commit=False)
	    # 设置该数据对象的密码，此密码是已经被经过效验的
            new_user.set_password(user_form.cleaned_data['password'])
            # 把数据对象和数据对象的密码写入到数据库中
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            UserInfo.objects.create(user=new_user)
            return HttpResponseRedirect(reverse('account:register_success'))
        else:
            return HttpResponseRedirect(reverse('account:register_fail'))
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, 'account/register.html', {'form':user_form,'profile':userprofile_form})


def register_success(request):
    return render(request, 'account/register_success.html')


def register_fail(request):
    return render(request, 'account/register_fail.html')


@login_required(login_url='/account/login/')
def myself(request):
    user=User.objects.get(username=request.user.username)
    userprofile=UserProfile.objects.get(user=user)
    userinfo=UserInfo.objects.get(user=user)
    return render(request,'account/myself.html',{'user':user,'userprofile':userprofile,'userinfo':userinfo})


# 编辑个人信息
@login_required(login_url='/account/login/')
def myself_edit(request):
    user=User.objects.get(username=request.user.username)
    userprofile=UserProfile.objects.get(user=request.user)
    userinfo=UserInfo.objects.get(user=request.user)

    if request.method=='POST':
        user_form=UserForm(request.POST)
        userprofile_form=UserProfileForm(request.POST)
        userinfo_form=UserInfoForm(request.POST)
        if user_form.is_valid() and  userprofile_form.is_valid() and userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            print(user_cd['email'])
            user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            user.save()
            userprofile.save()
            userinfo.save()
        # 执行语句，页面跳转到"http://localhost:8000/account/my-information" ，用户可以看到自己修改的结果
        return HttpResponseRedirect('/account/my-information/')
    else:
        user_form=UserForm(instance=request.user)
        userprofile_form=UserProfileForm(initial={'birth':userprofile.birth,'phone':userprofile.phone})
        userinfo_form= UserInfoForm(initial={'school':userinfo.school,'company':userinfo.company,'profession':userinfo.profession,'address':userinfo.address,'aboutme':userinfo.aboutme})
        return render(request,'account/myself_edit.html',{'user_form':user_form,'userprofile_form':userprofile_form,'userinfo_form':userinfo_form})


# 编辑视图
@login_required(login_url='/account/login/')
def my_image(request):
    if request.method=='POST':
        # 得到前端以POST提交的图片信息
        img=request.POST['img']
        userinfo=UserInfo.objects.get(user=request.user.id)
        userinfo.photo=img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request,'account/imagecrop.html',)

