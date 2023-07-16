from types import FunctionType

from .base import BaseFilter


class FuncFilter(BaseFilter):
    def __init__(self, func):
        self.check = func
        super().__init__()


def validate_filter(filter):
    if isinstance(filter, FunctionType):
        return FuncFilter(func=filter)
    if isinstance(filter, BaseFilter):
        return filter
    else:
        raise TypeError(f"The filter must be instance BaseFilter or function, not {type(filter)}")
