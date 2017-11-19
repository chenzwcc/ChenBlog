# coding=utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .models import Article
from operation.models import ArticleComments
# Create your views here.


class ArticleView(View):
    def get(self,request,type_id='1'):
        if type_id=='1':
            current='Python'
        elif type_id=='2':
            current="Django"
        elif type_id == '3':
            current = u"爬虫"
        elif type_id == '4':
            current = "Tornado"
        elif type_id == '5':
            current = "Flask"
        elif type_id == '6':
            current = "AI"
        elif type_id == '7':
            current = u"数据库"
        else:
            current = u'其他'

        all_article = Article.objects.filter(type=int(type_id)).order_by('-add_time')
        hot_article = Article.objects.filter(type=int(type_id)).order_by('-click_nums')[:6]

        return render(request,'article.html',{'all_article':all_article,'hot_article':hot_article,'current':current})


class ArticleDetailView(View):
    def get(self,request,type_id='1',num_id='1'):
        # 得到某类的所有文章
        article = Article.objects.get(id=int(num_id))
        #article_type = Article.objects.filter(type=type_id)
        # 得到只定的文章
        #article_title = article_type[int(num_id)-1]

        # 得到文章的全部评论
        all_commentas = ArticleComments.objects.filter(article=article)
        #article = Article.objects.get(title=article_title)

        article.click_nums+=1
        article.save()
        hot_article = Article.objects.filter(type=int(type_id)).order_by('-click_nums')[:6]

        return render(request,'article_detail.html',{
            'all_comments':all_commentas,
            'article':article,
            'hot_article':hot_article})


class AddCommentsView(View):
    """
       axaj添加课程评论
       """

    def post(self, request):
        article_id = request.POST.get('article_id', 0)
        comments = request.POST.get('comments', 0)

        # 判断用户是否登录
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        if article_id > 0 and comments:
            article_comments = ArticleComments()
            article = Article.objects.get(id=article_id)
            article_comments.article = article
            article_comments.comments = comments
            article_comments.user = request.user
            article_comments.save()

            """
            author = Author.objects.get(name=article.article)
            user = UserProfile.objects.get(nick_name=author)

            # 回复话题需要发生消息
            message = UserMessage()
            message.from_id = request.user.id
            message.user = user.id
            # 消息内容
            contents = '''{0}  评论了你的文章  {1}:{2}'''.format(
                request.user.nick_name, article.name, comments)

            message.message = contents
            message.save()
            """
            return HttpResponse('{"status":"success","msg":"添加评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加评论失败"}', content_type='application/json')


class WriteView(View):
    def get(self,request):
        return render(request,'write.html')