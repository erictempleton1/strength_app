# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-02 01:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strong_lifts', '0003_stronglifts_edited_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stronglifts',
            name='added_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]