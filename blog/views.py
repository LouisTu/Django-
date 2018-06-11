from django.shortcuts import render, get_object_or_404
from .models import BlogArticles


# 读取文章标题
# 用request函数响应所接收到的请求。 注：不能缺少
def blog_title(request):
    # 获取BlogArticles对象实例
    blogs = BlogArticles.objects.all()
    # 结束函数，并返回结果， 并用render()将数据传到指定的模板上
    return render(request, 'blog/titles.html', {'blogs':blogs})


# 查看文章详情请求
def blog_article(request, article_id):
    # 通过article_id创建BlogArticles类的实例，读取id的值是article_id的记录
    # article = BlogArticles.objects.get(id=article_id)
    # 改写上面代码，引入get_object_or_404()方法，这个方法能够简化对请求网页不存在时的异常处理
    article = get_object_or_404(BlogArticles, id=article_id)
    pub = article.publish
    return render(request, 'blog/content.html', {'article':article,'publish':pub})
