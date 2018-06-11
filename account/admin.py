from django.contrib import admin
from .models import UserProfile,UserInfo


# 管理新增的注册内容
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth', 'phone')
    list_filter = ('phone',)


admin.site.register(UserProfile, UserProfileAdmin)


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'company', 'profession', 'address', 'aboutme', 'photo')
    list_filter = ('school', 'company', 'profession')


admin.site.register(UserInfo, UserInfoAdmin)


# list_display:列出类表中的项目
# list_filter:规定网页右边FILTER的显示内容
