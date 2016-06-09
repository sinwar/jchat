from channels import Group

# connected to websocket
def ws_add(message):
    Group("chat").add(message.reply_channel)

def ws_message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    Group("chat").send({
        "text": "[user] %s" % message.content['text'],
    })

def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)