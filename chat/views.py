from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Room, Message, Conversation, DirectMessage
from django.contrib.auth import get_user_model
from .forms import CreateRoomForm

User = get_user_model()


# Create your views here.


def index(request):
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})


def create_room(request):
    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chat:index')
    else:
        form = CreateRoomForm(request.POST)
    context = {'form': form}
    return render(request, 'chat/create_room.html', context)


@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[:50]
    return render(request, 'chat/room.html', {
        'room': room,
        'messages': messages
    })


# NEW: DM Views
@login_required
def dm_inbox(request):
    """Show all conversations for the current user"""
    conversations = request.user.conversations.all()

    # Get conversation details with other user
    conversation_list = []
    for conv in conversations:
        other_user = conv.participants.exclude(id=request.user.id).first()
        last_message = conv.messages.last()
        unread_count = conv.messages.filter(is_read=False).exclude(sender=request.user).count()

        conversation_list.append({
            'conversation': conv,
            'other_user': other_user,
            'last_message': last_message,
            'unread_count': unread_count
        })

    return render(request, 'chat/dm_inbox.html', {
        'conversations': conversation_list
    })


@login_required
def dm_conversation(request, conversation_id):
    """Show a specific DM conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Verify user is a participant
    if not conversation.participants.filter(id=request.user.id).exists():
        return redirect('chat:dm_inbox')

    # Get other user
    other_user = conversation.participants.exclude(id=request.user.id).first()

    # Get messages
    messages = conversation.messages.all()[:100]

    # Mark messages as read
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    return render(request, 'chat/dm_conversation.html', {
        'conversation': conversation,
        'other_user': other_user,
        'messages': messages
    })


@login_required
def start_dm(request, username):
    """Start or continue a DM with another user"""
    other_user = get_object_or_404(User, username=username)

    if other_user == request.user:
        return redirect('chat:dm_inbox')

    # Check if conversation already exists
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()

    # Create new conversation if it doesn't exist
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    return redirect('chat:dm_conversation', conversation_id=conversation.id)


@login_required
def user_list(request):
    """Show list of users to start DM with"""
    users = User.objects.exclude(id=request.user.id).order_by('username')
    return render(request, 'chat/user_list.html', {'users': users})
