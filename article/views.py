import json
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ArticleColumn, ArticlePost
from .forms import ArticleColumnForm, ArticlePostForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import ArticleTag
from .forms import ArticleTagForm
import json
from translateyoudao.translate import translate
import json  
from urllib import parse  
import urllib.request, urllib.parse, urllib.request  


# 读取数据库中的栏目
@login_required(login_url='/account/login/')
# 防止提交表单时遇到的CSRF问题的一种方式
@csrf_exempt
def article_column(request):
    if request.method == 'GET':
        # 读取用户在数据库中的栏目
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request, 'article/column/article-column.html', {'columns':columns, 'column_form':column_form})
    
    if request.method == 'POST':
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name)
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse('1')


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST['column_name']
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse('1')
    except:
        return HttpResponse('0')


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article_column(request):
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('0')


@login_required(login_url='/account/login')
@csrf_exempt
def article_post(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                id = new_article.id
                slug = new_article.slug
                tags = request.POST['tags']
                if tags:
                    for atag in json.loads(tags):
                        tag = request.user.tag.get(tag=atag)
                        new_article.article_tag.add(tag)
                return HttpResponse(json.dumps({'e': 1,'id':id,'slug':slug}))
            except:
                return HttpResponse(json.dumps({'e': 2}))
        else:
            return HttpResponse(json.dumps({'e': 3}))
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        # 得到当前用户的所有标签
        article_tags = request.user.tag.all()
        # 打印出文章标签从数据库中提取出标签的sql语句
        print(article_tags.query)
        return render(request, 'article/column/article_post.html', {'article_post_form':article_post_form, 'article_columns':article_columns, 'article_tags':article_tags})


@login_required(login_url='/account/login')
def article_list(request):
    articles_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(articles_list, 5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request, 'article/column/article_list.html', {"articles":articles, 'page':current_page})


@login_required(login_url='/account/login')
def article_detail(request,id,slug):
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    return render(request, 'article/column/article_detail.html', {'article':article})


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article(request):
    article_id = request.POST['article_id']
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url='/account/login')
@csrf_exempt
def redit_article(request,article_id):
    if request.method == "GET":
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id=article_id)
        this_article_form = ArticlePostForm(initial={"title":article.title})
        this_article_column = article.column
        return render(request, 'article/column/redit_article.html', {'article':article, 'article_columns':article_columns, 'this_article_column':this_article_column, 'this_article_form':this_article_form})
    else:
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
            return HttpResponse('1')
        except:
            return HttpResponse('2')


@login_required(login_url='/account/login')
@csrf_exempt
def article_tag(request):
    if request.method == "GET":
        article_tags = ArticleTag.objects.filter(author=request.user)
        article_tag_form = ArticleTagForm()
        return render(request, "article/tag/tag_list.html", {"article_tags":article_tags, "article_tag_form":article_tag_form})

    if request.method == "POST":
        tag_post_form = ArticleTagForm(data=request.POST)
        if tag_post_form.is_valid():
            try:
                new_tag = tag_post_form.save(commit=False)
                new_tag.author = request.user
                new_tag.save()
                return HttpResponse("1")
            except:
                return HttpResponse("the data cannot be save.")
        else:
            return HttpResponse("Sorry, the form is not valid.")


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article_tag(request):
    tag_id = request.POST['tag_id']
    try:
        tag = ArticleTag.objects.get(id=tag_id)
        tag.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


def youdaofanyi(request):  
    ''''' 
    有道翻译功能 
    '''  
    query = {}  # 定义需要翻译的文本  
    fanyi = request.POST.get('fanyi_content', '')  
    query['q'] = fanyi  # 输入要翻译的文本  
    url = 'http://fanyi.youdao.com/openapi.do?keyfrom=11pegasus11&key=273646050&type=data&doctype=json&version=1.1&' + parse.urlencode(  
        query)  # 有道翻译api  
    response = urllib.request.urlopen(url, timeout=3)  
    # response = urllib.parse.urlopen(url)  
  
    # 编码转换  
    try:  
        html = response.read().decode('utf-8')  
        d = json.loads(html)  
        explains = d.get('basic').get('explains')  # 翻译后输出  
        a1 = d.get('basic').get('uk-phonetic')  # 英式发音  
        a2 = d.get('basic').get('us-phonetic')  # 美式发音  
        explains_list = []  
        for result in explains:  
            explains_list.append(result)  
        # 输出  
        fanyi_dict = {  
            'q': query['q'],  
            'yinshi': a1,  
            'meishi': a2,  
            'explains_list': explains_list,  
        }  
        return fanyi_dict  
    except Exception as e:  
        print (e) 


def listblogs(request):  
        fanyi_dict = {}  
        fanyi_form = fanyiForm()  
        if request.method == 'POST':  
            fanyi_form = fanyiForm(request.POST)  
            if fanyi_form.is_valid():  
                fanyi_dict = youdaofanyi(request)  
        bloglist = {  
            'fanyi_form' : fanyi_form, # 翻译的表单  
            'fanyi_dict' : fanyi_dict, # 翻译出来的文本  
        }  
        return render(request, 'fanyi.html', bloglist)      






























