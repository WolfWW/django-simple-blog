#! /usr/bin/env python3
#-*- coding:utf-8 -*-

from django import forms
from .models import Article,Comment

#���۱�
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment #���ñ�form������ģ��model
        fields = ('username','content') #������ģ������Ⱦ���ֶ�
        
#������
#class SearchForm(forms.Form):
#    search_entry = forms.CharField(label='�������±���ؼ���')
