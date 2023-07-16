import abc

from instdp.types.base import CallableMixin


class BaseFilter(CallableMixin):
    def __init__(self):
        super().__init__(self.check)

    @abc.abstractmethod
    def check(self, *args, **kwargs):
        pass

