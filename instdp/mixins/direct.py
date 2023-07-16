from instagrapi import Client

from instdp.filters import FuncFilter, validate_filter
from instdp.types import Handler


class DirectMixin:
    _cl: Client

    def __init__(self):
        self._message_handlers = []
        self._message_filters = {}

    def validation_filters(self, *filters, **kw_filters):
        _filters = []
        for filter in filters:
            _filters.append(validate_filter(filter))

        for key_filter, data_filter in kw_filters:
            cls_filter = self._message_filters.get(key_filter, None)
            if cls_filter is None:
                raise ValueError(f"Not key-word parameter {key_filter}")

    def message(self, *filters, **kw_filters):
        def decorator(func):
            self.register_message_handler(func, *filters, **kw_filters)

    def register_message_handler(self, func, *filters, **kw_filters):
        filters = self.validation_filters(*filters, **kw_filters)
        handler = Handler(func, *filters)
        self._message_handlers.append(handler)
        return func

    def filter(self, key=None):
        def decorator(func):
            filter = FuncFilter(func)
            if key is None:
                return filter
            self.register_filter(key, filter)
            return func

    def register_filter(self, key, filter):
        self._message_filters[key] = validate_filter(filter)

    def polling_direct(self, interval: int = 10, selected_filter="unread", auto_seen: bool = True):
        threads = self._cl.direct_threads(selected_filter=selected_filter, thread_message_limit=20)
        for thread in threads:
            # get message last seen
            new_msg_id = thread.last_seen_at.get(str(self._cl.user_id), {}).get("item_id", None)
            # not last seen msg -> load to last seen msg
            if any([new_msg_id == message.id for message in thread.messages]):
                thread = self.direct_thread_to_msg_id(thread_id=thread.id, to_msg_id=new_msg_id)

            msg_to_prosses = []
            # filrter message is seen
            for message in reverse(thread.messages):
                if new_msg_id == message.id:
                    break
                # add msg to prosses
                if not (message.is_sent_by_viewer or message.user_id == self._cl.user_id):
                    msg_to_prosses.append(message)

            for msg in msg_to_prosses:
                msg.thread = thread
                if auto_seen:
                    self.message_seen(msg)
                self.handler_notify(msg)
