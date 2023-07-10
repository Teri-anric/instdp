from instagrapi import Client
from .types.handler import Handler

class InstDispatcher:
    def __init__(self, client: Client):
        self._cl = client
        self._message_handlers = []

    def message(self):
        def decorator(func):
            self._message_handlers.append(Handler(func))


    def polling(self, interval: int = 5, auto_seen: bool = True):
        self._cl.direct_threads()
