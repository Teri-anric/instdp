from instagrapi import Client
from instagrapi.types import DirectMessage, DirectThread
from instagrapi.exceptions import DirectThreadNotFound
from instdp.types import Handler
from instdp.filters import FuncFilter, BaseFilter
from types import FunctionType

class DirectMixin:
    _cl : Client

    def __init__(self):
        self._message_handlers = []
        self._message_filters = {}

    def validation_filters(self, *filters, **kw_filters):
        _filters = []
        for filter in filters:
            if isinstance(filter, FunctionType):
                _filters.append(FuncFilter(func=filter))
            elif isinstance(filter, BaseFilter):
                _filters.append(filter)
            else:
                raise TypeError("Filter ")


        for key_filter, data_filter in kw_filters:
            cls_filter = self._message_filters.get(key_filter, None)
            if cls_filter is None:
                raise RuntimeError("not ")

    def message(self, *filters, **kw_filters):
        def decorator(func):
            self.register_message_handler(func, *filters, **kw_filters)

    def register_message_handler(self, func, *filters, **kw_filters):
        filters = self.validation_filters(*filters, **kw_filters)
        handler = Handler(func, *filters)
        self._message_handlers.append(handler)
        return func
    
    def _seen_message(self, message: DirectMessage):
        result = self._cl.private_request(
            f"direct_v2/threads/{message.thread_id}/items/{message.id}/seen/",
            data=self._cl.with_default_data({}),
            with_signature=False,
        )
        return extract_direct_response(result)

    def direct_thread_to_msg_id(self, thread_id: str, cursor: str = None, to_msg_id: int = None, max_msg: int = None) -> DirectThread:
        assert self._cl.user_id, "Login required"
        params = {
            "visual_message_return_type": "unseen",
            "direction": "older",
            "seq_id": "40065",  # 59663
            "limit": "20",
        }
        items = []
        while True:
            if cursor:
                params["cursor"] = cursor
            try:
                result = self._cl.private_request(
                    f"direct_v2/threads/{thread_id}/", params=params
                )
            except ClientNotFoundError as e:
                raise DirectThreadNotFound(e, thread_id=thread_id, **self._cl.last_json)
            thread = result["thread"]
            for item in thread["items"]:
                items.append(item)
                if item.get('item_id', None) == to_msg_id:
                    break
            cursor = thread.get("oldest_cursor")
            if not cursor or cursor == "MINCURSOR" or (max_msg and len(items) == max_msg):
                break
        thread["items"] = items
        return extract_direct_thread(thread)

    def polling_direct(self, interval: int = 10, selected_filter = "unread", auto_seen: bool = True):
        threads = self._cl.direct_threads(selected_filter = selected_filter, thread_message_limit = 20)
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
                #add msg to prosses
                if not (message.is_sent_by_viewer or message.user_id == self._cl.user_id):
                    msg_to_prosses.append(message)

            for msg in msg_to_prosses:
                msg.thread = thread
                self.handler_notify(msg)
