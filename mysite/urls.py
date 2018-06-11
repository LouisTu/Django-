from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


# 配置URL讲请求转到相应的文件夹下的urls.py
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls', namespace='blog',app_name='blog')),
    url(r'^account/', include('account.urls', namespace='account', app_name='account')),
    url(r'^article/', include('article.urls', namespace='article', app_name='article')),
    url(r'^home/', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^course/', include('course.urls', namespace='course', app_name='course')),
    url(r'^image/', include('image.urls', namespace='image', app_name='image')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)