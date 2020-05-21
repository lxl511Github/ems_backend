from django.db import models

# Create your models here.


class equ(models.Model):
    serialNum = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    equ_type = models.CharField(max_length=30)
    add_time = models.DateTimeField(auto_now_add=True)
    admin_per = models.CharField(max_length=20)
    equ_status = models.CharField(max_length=10)
    category = models.CharField(max_length=20, default=None)

    def __str__(self):

        return self.serialNum


class loanMsg(models.Model):
    loanName = models.CharField(max_length=20)
    jobNum = models.CharField(max_length=20)
    department = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    equName = models.CharField(max_length=20, default=None)
    equ_num = models.CharField(max_length=20)
    category = models.CharField(max_length=20, default=None)

    def __str__(self):
        return self.equ_num


class Repay(models.Model):
    serialNum = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    equ_status = models.CharField(max_length=5)
    desc = models.CharField(max_length=120, default=None)
    date = models.DateTimeField(auto_now_add=True)
    admin = models.CharField(max_length=10)

    def __str__(self):

        return self.serialNum
