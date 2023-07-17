from .base import BaseFilter
from typing import Type, Any


class ExceptionFilter(BaseFilter):
    def __init__(self, exception_cls: Type[Any] = None):
        self.exception_cls = exception_cls

    def __call__(self, e: Exception):
        if not self.exception_cls:
            return True

        return isinstance(e, self.exception_cls)
