# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-19 10:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20170416_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='text',
            field=models.TextField(verbose_name='正文'),
        ),
    ]
