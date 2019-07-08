from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from accounts.models import User
from pufiki190630.utilities import generate_slug_and_save, DEFAULT_SLUG_LENGTH


class Chat(models.Model):
    STATUS_CHOICES = (
        (1, _('Open')),
        (2, _('Closed')),
    )

    slug = models.CharField(max_length=DEFAULT_SLUG_LENGTH, unique=True, editable=False)  # handled by save method
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        generate_slug_and_save(self, Chat, *args, **kwargs)


class Message(models.Model):
    BODY_PRINT_LIMIT = 30

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    is_from_user = models.BooleanField(default=True)
    body = models.CharField(max_length=512)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return (self.body[:Message.BODY_PRINT_LIMIT] + '...') \
            if len(self.body) > Message.BODY_PRINT_LIMIT \
            else self.body
