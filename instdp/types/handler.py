from .base import CallableMixin


class Handler(CallableMixin):
    def __init__(self, callback, filters=None):
        self.callback = callback
        super().__init__()
        self.filters = filters

    def register_filter(self, filter_):
        if not self.filters:
            return self.filters.append(filter_)
        self.filters = [filter_]

    def check(self, *args, **kwargs):
        if not self.filters:
            return True
        for event_filter in self.filters:
            if not event_filter(*args, **kwargs):
                return False
        return True

    def __call__(self, *args, **kwargs):
        check = self.check(*args, **kwargs)
        if check:
            super().__call__(*args, **kwargs)
        return check
