from __future__ import unicode_literals
from django.db import models

# Create your models here.


class UserInfo(models.Model):

    userName = models.CharField(max_length=32)
    passWord = models.CharField(max_length=64)

    def __unicode__(self):
        return self.userName

