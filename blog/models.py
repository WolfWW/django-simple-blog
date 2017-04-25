#! /usr/bin/env python3
#-*- coding:utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse

#创建文章模型
class Article(models.Model):
#models中所有的模型都是django.db.models.Model的子类
    #用来给文章状态提供选项的二元组
    STATUS_CHOICES = (
	    ('draft','草稿'),
		('published','已发布'),
		)

	#创建文章的标题、正文、创建时间、文章状态、分类等属性
    title = models.CharField('标题',max_length=50)
    text = models.TextField('正文',)
    created_time = models.DateTimeField('创建时间',auto_now_add=True)
    #auto_now_add在对象创建时默认使用当前时间
    status = models.CharField('文章状态',max_length=10,choices=STATUS_CHOICES)
    #choices参数会表现为一个下拉框
    category = models.ForeignKey('Category',verbose_name='分类',null=True,on_delete=models.SET_NULL)
    tag = models.ManyToManyField('Tag',verbose_name='标签',blank=True)
    #on_delete=models.SET_NULL表示删除某个分类（category）后该分类下所有的Article的外键设为null（空）；如on_delete=models.CASCADE则当删除外键时，会删除所有包含该外键的对象，这是外键的默认值
    #引用外键前，如还未定义外键，要给外键名加引号；已定义则不用引号
    #verbose_name的作用是给属性一个适合阅读的名字

    #定义一个方法返回标题，否则只能返回一个无意义的表示	
    def __str__(self):
	    return self.title
        
    #新增方法，得到当前文章的url，用于CommentView
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'article_id':self.pk})

#创建分类模型		
class Category(models.Model):
    category = models.CharField('分类',max_length=30)
	
    def __str__(self):
	    return self.category
        
#创建标签模型		
class Tag(models.Model):
    tag = models.CharField('标签',max_length=15)
	
    def __str__(self):
	    return self.tag
        
#创建评论模型
class Comment(models.Model):
    username = models.CharField(verbose_name='您的昵称',max_length=30)
    useremail = models.EmailField(verbose_name='邮件地址',max_length=100,blank=True)
    content = models.TextField(verbose_name='评论内容')
    created_time = models.DateTimeField('评论时间',auto_now_add=True)
    article = models.ForeignKey(Article,verbose_name='文章',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content[:25]
