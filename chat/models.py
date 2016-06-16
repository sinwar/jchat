import json
from django.db import models
from django.utils.six import python_2_unicode_compatible
from channels import Group

from .settings import MSG_TYPE_MESSAGE, MSG_TYPE_ENTER, MSG_TYPE_LEAVE, MSG_TYPE_ALERT, MSG_TYPE_WARNING, MSG_TYPE_MUTED


@python_2_unicode_compatible
class Room(models.Model):
    """
    A room for people to chat in.
    """

    # Room title
    title = models.CharField(max_length=255)

    # If only "staff" users are allowed (is_staff on django's User)
    staff_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return Group("room-%s" % self.id)

    def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
        """
        Called to send a message to the room on behalf of a user.
        """
        final_msg = {"room": str(self.id), "message": message, "username": user.username, "msg_type": msg_type}

        # save in messages
        if message!=None:
            messages.objects.create(room=self, sender=user.username, message=message, message_type=msg_type)
        # Send out the message to everyone in the room

        if msg_type == MSG_TYPE_ENTER:
            messages.objects.create(room=self, sender=user.username, message='join', message_type=msg_type)

        elif msg_type == MSG_TYPE_LEAVE:
            messages.objects.create(room=self, sender=user.username, message='leave', message_type=msg_type)

        elif msg_type == MSG_TYPE_WARNING:
            messages.objects.create(room=self, sender=user.username, message='warning', message_type=msg_type)

        elif msg_type == MSG_TYPE_ALERT:
            messages.objects.create(room=self, sender=user.username, message='alert', message_type=msg_type)

        elif msg_type == MSG_TYPE_MUTED:
            messages.objects.create(room=self, sender=user.username, message='muted', message_type=msg_type)


        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )


@python_2_unicode_compatible
class messages(models.Model):
    """
    all the messages will be saved in this model
    """

    room = models.ForeignKey(Room)

    sender = models.CharField(max_length=256)

    message = models.TextField()

    message_type = models.IntegerField()


    def __str__(self):
        return self.message
