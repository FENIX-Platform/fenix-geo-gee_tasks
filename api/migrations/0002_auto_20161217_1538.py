# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-17 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='argument',
            field=models.PositiveIntegerField(null=True),
        ),
    ]