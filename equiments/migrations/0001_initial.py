# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2020-03-12 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='equ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serialNum', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('admin_per', models.CharField(max_length=20)),
                ('equ_status', models.CharField(max_length=5)),
            ],
        ),
    ]
