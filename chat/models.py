import random
import string

from django.conf import settings
from django.db import models


# Create your models here.
def code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate a random slug if the instance is being created and slug is empty
        if not self.pk and not self.slug:
            self.slug = code()

        super().save(*args, **kwargs)


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.user.username}: {self.content[:50]}'
