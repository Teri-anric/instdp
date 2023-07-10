    
class DirectMinix:
    def __init__(self):
        self._message_handlers = []

    def message(self):
        def decorator(func):
            self._message_handlers.append(Handler(func))
    
    def _seen_message(self, message: DirectMessage):
        result = self._cl.private_request(
            f"direct_v2/threads/{message.thread_id}/items/{message.id}/seen/",
            data=self._cl.with_default_data({}),
            with_signature=False,
        )
        return extract_direct_response(result)

    def polling_direct(self, interval: int = 10, selected_filter = "unread", auto_seen: bool = True):
        threads = self._cl.direct_threads(selected_filter = selected_filter, thread_message_limit = 20)
        for thread in threads:
            pass
        