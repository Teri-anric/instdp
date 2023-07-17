import abc


class BaseFilter(abc.ABC):

    @abc.abstractmethod
    def __call__(self, event, **kwargs):
        pass
