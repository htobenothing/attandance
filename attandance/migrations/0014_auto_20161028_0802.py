# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-28 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attandance', '0013_auto_20161028_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='update_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
