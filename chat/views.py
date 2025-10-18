from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Message

# Create your views here.


def index(request):
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})


@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[:50]
    return render(request, 'chat/room.html', {
        'room': room,
        'messages': messages
    })
