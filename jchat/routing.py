from channels.routing import route
channel_routing = [
    route("http.request", "chat.consumers.http_consumer"),
]
