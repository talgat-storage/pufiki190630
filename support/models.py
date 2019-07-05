from django.db import models

from accounts.models import User


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    body = models.CharField(max_length=512)

    def __str__(self):
        return self.title
