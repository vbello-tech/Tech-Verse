from django.contrib import admin
from .models import Room, Message, Conversation, DirectMessage

# Register your models here.

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Conversation)
admin.site.register(DirectMessage)
