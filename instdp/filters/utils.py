from types import FunctionType

from . import BaseFilter
from ..types.handler import FilterObject


def validate_filter(filter_):
    if isinstance(filter_, (FunctionType, BaseFilter)):
        return FilterObject(callback=filter_)
    else:
        raise TypeError(f"The filter must be instance BaseFilter or function, not {type(filter_)}")
