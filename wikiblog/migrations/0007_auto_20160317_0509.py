# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-17 05:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wikiblog', '0006_remove_page_hashtag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hashtag',
            old_name='topic',
            new_name='tag',
        ),
    ]
