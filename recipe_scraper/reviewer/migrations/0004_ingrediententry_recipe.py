# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-18 21:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviewer', '0003_auto_20170918_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingrediententry',
            name='recipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='reviewer.Recipe'),
            preserve_default=False,
        ),
    ]
