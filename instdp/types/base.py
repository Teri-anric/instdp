import inspect
from typing import Dict, Any


class CallableMixin:
    def __init__(self, func):
        self.callback = func
        callback = inspect.unwrap(self.callback)
        self.spec = inspect.getfullargspec(callback)

    def _prepare_kwargs(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        if self.spec.varkw:
            return kwargs

        return {
            k: v for k, v in kwargs.items() if k in self.spec.args or k in self.spec.kwonlyargs
        }

    def __call__(self, *args, **kwargs: Any) -> Any:
        return self.callback(*args, **self._prepare_kwargs(kwargs))
