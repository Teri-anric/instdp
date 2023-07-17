import abc

from ..types.base import CallableMixin


class BaseFilter(abc.ABC):
    
    @abc.abstractmethod
    def __call__(self, event, **kwargs):
        pass

class FilterObject(CallableMixin):
    def __init__(self, callback: BaseFilter):
        self.callback = callback
