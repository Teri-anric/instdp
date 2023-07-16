import time
from types import FunctionType
from typing import Dict, Any
from typing import List, Union

from instagrapi import Client
from instagrapi.types import (
    DirectMessage,
    DirectThread,
)

from instdp.filters import FuncFilter, validate_filter, BaseFilter, ExceptionFilter
from instdp.types import Handler


class DirectMixin:
    _cl: Client

    def __init__(self):
        self._is_stop = False
        self._message_handlers: List[Handler] = []
        self._message_kw_filters: Dict[str, Union[type, FunctionType]] = {}
        self._exception_handlers: List[Handler] = []
        self._context: Dict[str, Any] = {}

    def __setitem__(self, key, value):
        self._context[key] = value

    def __getitem__(self, item):
        return self._context.get(key, None)

    def __delitem__(self, key):
        self._context.pop(key, None)

    def init_kw_filters(self, kw_filters) -> List[BaseFilter]:
        filters = []
        for key, data in kw_filters.items():
            cls_filter = self._message_kw_filters.get(key)
            filters.append(cls_filter(data))
        return filters

    def message(self, *filters, **kw_filters):
        def decorator(func):
            self.register_message_handler(func, *filters, **kw_filters)

        return decorator

    def register_message_handler(self, func, *filters, **kw_filters):
        filters = [validate_filter(x) for x in filters]
        filters.extend(self.init_kw_filters(kw_filters))

        handler = Handler(func, filters)
        self._message_handlers.append(handler)
        return func

    def filter(self, key: str = None):
        def decorator(func):
            filter = FuncFilter(func)
            if key is None:
                return filter
            self.register_filter(key, filter)
            return func

        return decorator

    def register_filter(self, key: str, cls_filter: type):
        if not issubclass(cls_filter, BaseFilter) and not isinstance(cls_filter, FunctionType):
            if isinstance(cls_filter, BaseFilter):
                raise ValueError("must be a class or function(return Filter) not an instance")
            raise TypeError(f"most be a subclass BaseFilter, not be {cls_filter}")
        self._message_kw_filters[key] = cls_filter

    @property
    def default_context(self):
        return {'cl': self._cl, 'client': self._cl, 'dp': self, "dispatcher": self}

    def handler_notify(self, message: DirectMessage, thread: DirectThread):
        for handler in self._message_handlers:
            try:
                if handler(message, thread=thread, **self.default_context, **self._context):
                    break
            except Exception as e:
                self.exception_handler_notify(exception=e, handler=handler, message=message)

    def exception_handler_notify(self, exception: Exception, handler: Handler, message: DirectMessage):
        for handler in self._exception_handlers:
            if handler(exception, handler=handler, message=message, **self.default_context, **self._context):
                break

    def exception_handler(self, exception: type):
        def decorator(func):
            self.register_exception_handler(func=func, exception=exception)
            return func

        return decorator

    def register_exception_handler(self, func, exception: type):
        filter_ = ExceptionFilter(exception_cls=exception)
        handler = Handler(func, [filter_])
        self._exception_handlers.append(handler)

    def polling_direct(self, interval: int = 10, selected_filter="unread", auto_seen: bool = True, infinite=True):
        self._is_stop = False
        while True:
            time.sleep(interval)
            threads = self._cl.direct_threads(selected_filter=selected_filter, thread_message_limit=20)
            for thread in threads:
                # get message last seen
                new_msg_id = thread.last_seen_at.get(str(self._cl.user_id), {}).get("item_id", None)
                # not last seen msg -> load to last seen msg
                if not any([new_msg_id == message.id for message in thread.messages]):
                    thread = self.direct_thread_to_msg_id(thread_id=thread.id, to_msg_id=new_msg_id)

                msg_to_prosses = []
                # filrter message is seen
                for message in thread.messages:
                    if new_msg_id == message.id:
                        break
                    # add msg to prosses
                    if not (message.is_sent_by_viewer or message.user_id == self._cl.user_id):
                        msg_to_prosses.append(message)

                for msg in msg_to_prosses:
                    if auto_seen:
                        self.message_seen(msg)
                    self.handler_notify(msg, thread=thread)

            if not infinite or self._is_stop:
                return
