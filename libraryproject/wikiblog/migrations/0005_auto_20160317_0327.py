# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-17 03:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wikiblog', '0004_auto_20160317_0224'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='hashtag',
            field=models.ManyToManyField(default='all', to='wikiblog.Hashtag'),
        ),
    ]