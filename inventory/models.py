# models.py in your app
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_user_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Box(models.Model):
    length = models.FloatField()
    breadth = models.FloatField()
    height = models.FloatField()
    area = models.FloatField(default=None)
    volume = models.FloatField(default=None)
    creator = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT,default=0)
    created_by = models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

