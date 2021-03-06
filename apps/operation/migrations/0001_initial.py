# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-19 07:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(max_length=300, verbose_name='\u8bc4\u8bba\u5185\u5bb9')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.Article', verbose_name='\u6587\u7ae0')),
            ],
            options={
                'verbose_name': '\u6587\u7ae0\u8bc4\u8bba',
                'verbose_name_plural': '\u6587\u7ae0\u8bc4\u8bba',
            },
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(default=0, verbose_name='\u63a5\u53d7\u7528\u6237')),
                ('message', models.CharField(max_length=500, verbose_name='\u7528\u6237\u6d88\u606f')),
                ('has_read', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u8bfb')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u6d88\u606f',
                'verbose_name_plural': '\u7528\u6237\u6d88\u606f',
            },
        ),
    ]
