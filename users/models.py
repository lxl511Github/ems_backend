from django.db import models

# Create your models here.


class Users(models.Model):
    u_id = models.IntegerField()
    name = models.CharField(max_length=20)
    apartment = models.CharField(max_length=5)
    registerTime = models.DateTimeField(auto_created=True)

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Roles(models.Model):
    r_id = models.IntegerField()
    r_name = models.CharField(max_length=10)

    class Meta:
        db_table = 'roles'
        verbose_name = '角色'
        verbose_name_plural = verbose_name


class Source(models.Model):
    s_id = models.IntegerField()
    s_name = models.CharField(max_length=10)

    class Meta:
        db_table = 'source'
        verbose_name = '权限'
        verbose_name_plural = verbose_name
