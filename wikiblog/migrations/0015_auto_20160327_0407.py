# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-27 04:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wikiblog', '0014_page_accessed_date'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='page_accessed_date',
            new_name='page_accessed',
        ),
    ]
