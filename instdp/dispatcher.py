from instagrapi import Client
from .types.handler import Handler


class InstDispatcher:
    def __init__(self, client: Client):
        self._cl = client
        self._message_handlers = []

    def message(self):
        def decorator(func):
            self._message_handlers.append(Handler(func))


    def polling_direct(self, interval: int = 10, selected_filter = "unread", auto_seen: bool = True):
        threads = self._cl.direct_threads(selected_filter = selected_filter, thread_message_limit = 20)
        for thread in threads:
            pass
