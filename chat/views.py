from django.shortcuts import render
import json
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
    mesgs = []
    for i in msgs:
        k = json.dumps({'room':i.room.id, 'sender':i.sender, 'message':i.message, 'msg_type':i.message_type})
        mesgs.append(k)

    httpoutput = json.dumps(dict({'messages': mesgs}))

    # Render that in the index template
    return render(request, "index.html", {
        "rooms": rooms,
        "messages":httpoutput
    })
