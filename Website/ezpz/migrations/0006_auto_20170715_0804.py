# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-15 08:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ezpz', '0005_imagefeedback_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='priority',
            field=models.FloatField(null=True),
        ),
    ]
