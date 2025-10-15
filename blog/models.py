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


class Blog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=120, blank=True, null=True)
    post_image = models.ImageField(blank=False, upload_to="BlogImage/")
    body = FroalaField(options={
        'toolbarInline': True,
    })
    publish_date = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(default=code())

    def get_detail(self):
        return reverse("blog:detail", kwargs={
            'slug': self.slug
        })

    # def save(self, *args, **kwargs):
    #     # Generate a random slug if the instance is being created and slug is empty
    #     if not self.slug:
    #         self.slug = code()
    #
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.title
