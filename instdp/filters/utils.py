from types import FunctionType

from . import BaseFilter
from ..types.handler import FilterObject


def validate_filter(filter):
    if isinstance(filter, (FunctionType, BaseFilter)):
        return FilterObject(callback=filter)
    else:
        raise TypeError(f"The filter must be instance BaseFilter or function, not {type(filter)}")
