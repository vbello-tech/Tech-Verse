import random
import string
import uuid

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

# Create your models here.


class Blog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=120, blank=True, null=True)
    post_image = models.ImageField(blank=False, upload_to="BlogImage/")
    body = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # def get_detail(self):
    #     return reverse("blog:detail", kwargs={
    #         'id': self.id
    #     })

    def __str__(self):
        return self.title
