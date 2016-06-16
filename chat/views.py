from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room, messages


@login_required
def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")

    msgs = messages.objects.all()

    room = []
    msg = []
    msg_type = []
    sender = []
    for i in msgs:
        room.append(i.room)
        sender.append(i.sender)
        msg.append(i.message)
        msg_type.append(i.message_type)

    mesgs = zip(room, sender, msg, msg_type)

    # Render that in the index template
    return render(request, "index.html", {
        "rooms": rooms,
        #"messages":mesgs
    })
