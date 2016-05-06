# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-27 02:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wikiblog', '0011_auto_20160322_0508'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=60, unique=True)),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]