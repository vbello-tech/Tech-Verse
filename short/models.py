import random
import string
import uuid

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from froala_editor.fields import FroalaField


# Create your models here.
def code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def user_dir(instance, filename):
    return f'PostUploads/{instance.author.username}/{filename}'


class Short(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.FileField(upload_to=user_dir)
    slug = models.SlugField(blank=True, null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_likers')
    publish_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-publish_date']

    def save(self, *args, **kwargs):
        # Generate a random slug if the instance is being created and slug is empty
        if not self.pk and not self.slug:
            self.slug = code()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug


class Comment(models.Model):
    post = models.ForeignKey('Short', related_name="short_comment", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="short_comment_author", on_delete=models.CASCADE)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post, self.author)
