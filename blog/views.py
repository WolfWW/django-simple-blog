#-*- coding:utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,FormView
from blog.models import Article,Category,Tag
from blog.forms import CommentForm
import markdown2

#这类视图与ListView通用视图功能一致，所以继承通用视图完成
class IndexView(ListView):
    template_name = 'blog/index.html'
	#告诉视图对这个页面进行渲染
    context_object_name = 'article_list'
	#给上下文变量取名，和模板中的那个变量一致

	#重写get_queryset方法，只显示已发布的文章
    def get_queryset(self):
	    article_list = Article.objects.filter(status='published').order_by('-created_time')[:5]
	    return article_list
    
    #重写，返回分类和标签列表
    def get_context_data(self,**kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('category')
        kwargs['tag_list'] = Tag.objects.all().order_by('tag')
        kwargs['title'] = 'Wolf‘s House'
        return super(IndexView,self).get_context_data(**kwargs)
		
class ArticleView(DetailView):
    model = Article   #不指定queryset就要指定model
    template_name = 'blog/detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'  #URLconf中主键的关键字参数的名称

    #重写，把正文转换成markdown格式。该方法使用pk_url_kwarg参数查找对象
    def get_object(self):
	    obj = super(ArticleView,self).get_object()
	    obj.text = markdown2.markdown(obj.text,extras=['fenced-code-blocks',])
	    return obj
        
    #把评论form添加到context
    def get_context_data(self,**kwargs):
        kwargs['comment_list'] = self.object.comment_set.all().order_by('-created_time')
        kwargs['form'] = CommentForm()
        kwargs['category_list'] = Category.objects.all().order_by('category')
        kwargs['tag_list'] = Tag.objects.all().order_by('tag')
        return super(ArticleView,self).get_context_data(**kwargs)

class AllView(ListView):
    template_name = 'blog/index.html'  #和首页一样
    context_object_name = 'article_list'  #要的就是文章列表，也是一样

	#重写get_queryset方法，从已发布的文章中按分类筛选
    def get_queryset(self):
	    article_list = Article.objects.filter(status='published').order_by('-created_time')
	    return article_list
    
    #重写，返回分类和标签列表
    def get_context_data(self,**kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('category')
        kwargs['tag_list'] = Tag.objects.all().order_by('tag')
        kwargs['title'] = '所有文章'
        return super(AllView,self).get_context_data(**kwargs)
        
class CategoryView(ListView):
    template_name = 'blog/index.html'  #和首页一样
    context_object_name = 'article_list'  #要的就是文章列表，也是一样

	#重写get_queryset方法，从已发布的文章中按分类筛选
    def get_queryset(self):
	    article_list = Article.objects.filter(category=self.kwargs['category_id'],status='published').order_by('-created_time')
	    return article_list
    
    #重写，返回分类和标签列表
    def get_context_data(self,**kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('category')
        kwargs['tag_list'] = Tag.objects.all().order_by('tag')
        kwargs['title'] = '分类目录：%s' % Category.objects.filter(id=self.kwargs['category_id'])[0].category
        return super(CategoryView,self).get_context_data(**kwargs)

#和CategoryView完全一样        
class TagView(ListView):
    template_name = 'blog/index.html'  #和首页一样
    context_object_name = 'article_list'  #要的就是文章列表，也是一样

	#重写get_queryset方法，从已发布的文章中按标签筛选
    def get_queryset(self):
	    article_list = Article.objects.filter(tag=self.kwargs['tag_id'],status='published').order_by('-created_time')
	    return article_list
    
    #重写，返回分类和标签列表
    def get_context_data(self,**kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('category')
        kwargs['tag_list'] = Tag.objects.all().order_by('tag')
        kwargs['title'] = '标签目录：%s' % Tag.objects.filter(id=self.kwargs['tag_id'])[0].tag
        return super(TagView,self).get_context_data(**kwargs)
        
class CommentView(FormView):
    form_class = CommentForm
    template_name = 'blog/detail.html'
    #指定评论提交后渲染的模板文件
    #评论成功后返回文章详情页
    
    def form_valid(self,form):
        #从当前url获取被评论的文章
        target_article = get_object_or_404(Article,pk=self.kwargs['article_id'])
        #返回生成实例，暂不保存评论
        comment = form.save(commit=False)
        comment.article = target_article #将评论与文章关联
        comment.save()
        # 用Article中定义的方法获取重定向的URL
        self.success_url = target_article.get_absolute_url()
        return HttpResponseRedirect(self.success_url)
'''        
#搜索文章       errors字段和valid方法还没弄明白 
class SearchView(FormView):
    form_class = SearchForm
    template_name = 'blog/search_form.html'
    
    def get_queryset(self):
	    article_list = Article.objects.filter(title__contains=q,status='published').order_by('-created_time')
	    return article_list
'''
def search(request):
    category_list = Category.objects.all().order_by('category')
    tag_list = Tag.objects.all().order_by('tag')
    errors=[]  #先自带隐藏错误，如果是地址栏输入search进入，直接跳到最后的return
    #若用户点击search则执行下列代码
    if 'q' in request.GET:
        q=request.GET['q']
        if not q:
            errors.append('请输入搜索内容。')
        elif len(q)>20:
            errors.append('最多只能搜索长度20的内容。')
        else:
            article_list=Article.objects.filter(title__contains=q,status='published').order_by('-created_time')
            return render(request,'blog/search_form.html',{'article_list':article_list,'category_list':category_list,'tag_list':tag_list,'query':q})
    return render(request,'blog/search_form.html',{'category_list':category_list,'tag_list':tag_list,'errors':errors})