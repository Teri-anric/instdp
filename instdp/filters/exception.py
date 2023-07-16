from .base import BaseFilter


class ExceptionFilter(BaseFilter):
    def __init__(self, exception_cls: type = None):
        super().__init__()
        self.exception_cls = exception_cls

    def check(self, e: Exception):
        if not self.exception_cls:
            return True

        return isinstance(e, self.exception_cls)
