# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-14 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nltkApi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainedmodel',
            name='pickled_name',
            field=models.CharField(max_length=65536),
        ),
    ]
