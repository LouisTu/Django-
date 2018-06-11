from django import forms
from django.core.files.base import ContentFile
from slugify import slugify
from urllib import request

from .models import Image


class ImageForm(forms.ModelForm):

    class Meta:
        models = Image
        fields = ('title', 'url', 'description')

    # 创建一个除self外，不传入其他值的函数，也不直接得到提交表单的内容
    def clean_url(self):
        # 获得相应字段的值，透过cleaned_data
        url = self.cleaned_data['url']
        # 规定图片的扩展名
        valid_extensions = ['jpg', 'jpeg', 'png']
        # 从得到的图片的网址中分解出其扩展名，
        extension = url.rsplit('.', 1)[1].lower()
        # 判断扩展名是否合法
        if extension not in valid_extensions:
            raise forms.ValidationError("The given Url does not match valid image extension")
        # 返回验证后的字段
        return url

    # 讲表单提交的数据保存到数据库
    def save(self, force_insert=False, force_update=False, commit=True):
        # 执行父类的ModelForm的save()方法，先建立实例但是先不保存数据
        image = super(ImageForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{0).{1}'.format(slugify(image.title), image_url.rsplit('., 1')[1].lower())
        # 以GET方式访问图片地址
        response = request.urlopen(image_url)
        # 将访问的图片地址中返回的结果保存到本地，以约定的名称给图片文件命名
        image.image.save(image_name, ContentFile(response.read()), save=True)
        if commit:
            image.save()
        return image
