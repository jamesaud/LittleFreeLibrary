# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-27 04:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wikiblog', '0013_auto_20160327_0305'),
    ]

    operations = [
        migrations.CreateModel(
            name='page_accessed_date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_accessed', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wikiblog.User')),
            ],
        ),
    ]
