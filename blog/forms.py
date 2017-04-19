#! /usr/bin/env python3
#-*- coding:utf-8 -*-

from django import forms
from .models import Article,Comment

#评论表单
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment #设置表单form关联的模型model
        fields = ('username','content') #设置在模板中渲染的字段
        
#搜索表单
#class SearchForm(forms.Form):
#    search_entry = forms.CharField(label='输入文章标题关键字')
