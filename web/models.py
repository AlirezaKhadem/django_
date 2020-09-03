from django.db import models

from django.contrib.auth.models import User


# Create your models here.

class Passwordresetcode(models.Model):
    code = models.CharField(max_length=32)
    email = models.CharField(max_length=120)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    time = models.DateTimeField()


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    token = models.CharField(max_length=48)

    def __str__(self):
        return "{}-token".format(self.user)


class Expense(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateTimeField()
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{} ** {} | {}".format(self.user, self.date, self.amount)


class Income(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateTimeField()
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{} ** {} | {}".format(self.user, self.date, self.amount)
