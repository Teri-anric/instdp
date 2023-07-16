from .base import CallableMixin

class Handler(CallableMixin):
    def __init__(self, func, filters=None):
        super().__init__(func)
        self.filters = filters

    def register_filter(self, filter_):
        self.filters.append(filter_)

    def check(self, *args, **kwargs):
        if not self.filters:
            return True
        for event_filter in self.filters:
            if not event_filter(*args, **kwargs):
                return False
        return True


    def __call__(self, *args, **kwargs):
        if check:
            super().__call__(*args, **kwargs)