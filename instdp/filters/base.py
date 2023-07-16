from instdp.types.base import CallableMixin


class BaseFilter(CallableMixin):
    def __init__(self):
        super().__init__(self.check)

    def check(self, *args, **kwargs) -> bool:
        raise NotImplemented("")

    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)
