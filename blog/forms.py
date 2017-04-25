#! /usr/bin/env python3
#-*- coding:utf-8 -*-

from django import forms
from .models import Article,Comment

#评论表单
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment #设置表单form关联的模型model
        fields = ['username','useremail','content'] #设置在模板中渲染的字段
        
        widgets = {
            'username':forms.TextInput(attrs={
                'placeholder':"您的昵称（必填）",}),
            'useremail':forms.TextInput(attrs={
                'placeholder':"如需要邮件回复请输入（选填）",}),
            'content':forms.Textarea(attrs={
                'placeholder':"评论内容（必填）",}),
        }
        
#搜索表单
#class SearchForm(forms.Form):
#    search_entry = forms.CharField(label='输入文章标题关键字')
