from types import FunctionType

from .base import BaseFilter, FilterObject


def validate_filter(filter):
    if isinstance(filter, (FunctionType, BaseFilter)):
        return FilterObject(callback=filter)
    else:
        raise TypeError(f"The filter must be instance BaseFilter or function, not {type(filter)}")
