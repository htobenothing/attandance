# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-27 23:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attandance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancehistory',
            name='Create_Date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]