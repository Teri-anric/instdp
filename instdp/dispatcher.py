from instagrapi import Client
from instdp.mixins.direct import DirectMixin
from instdp.mixins.direct_api import MixinDirectAPI

class BaseDispatcher:
    _cl: Client

    def __init__(self, client: Client):
        self._cl = client
        super().__init__()

class DirectDispatcher(BaseDispatcher, DirectMixin, MixinDirectAPI):
    pass

class InstDispatcher(BaseDispatcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._direct = DirectDispatcher(self._cl)
