from django import forms
from .models import ArticleColumn, ArticlePost
from .models import Comment
from .models import ArticleTag


# 栏目数据模型
class ArticleColumnForm(forms.ModelForm):

    class Meta:
        model = ArticleColumn
        fields = ('column',)


class ArticlePostForm(forms.ModelForm):

    class Meta:
        model = ArticlePost
        fields = ('title','body')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("commentator", "body",)


class ArticleTagForm(forms.ModelForm):
    
    class Meta:
        model = ArticleTag
        fields = ("tag",)


class fanyiForm(forms.Form):  
    ''''' 
    翻译功能表单 
    '''  
    fanyi_content = forms.CharField(label='翻译', error_messages={  
        'required': '请填写需要翻译的内容',  
        'max_length': '填写的内容太长'  
    }, widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'exampleInputContent', 'placeholder': '请输入要翻译的文字', 'rows': '1'}))  
