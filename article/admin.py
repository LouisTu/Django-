from django.contrib import admin
from .models import ArticleColumn

# Register your models here.
class ArticleColumnAdmin(admin.ModelAdmin):
    list_filter = ('column',)
    list_display = ('column','created','user')

admin.site.register(ArticleColumn,ArticleColumnAdmin)