# Generated by Django 2.1.15 on 2020-05-19 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equiments', '0007_loanmsg_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanmsg',
            name='equName',
            field=models.CharField(default=None, max_length=20),
        ),
    ]
