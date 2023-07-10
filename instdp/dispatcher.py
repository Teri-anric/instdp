from instagrapi import Client
from .types.handler import Handler

from instagrapi.extractors import (
    extract_direct_response
)
from instagrapi.types import (
    DirectMessage,
    DirectResponse,
    DirectShortThread,
    DirectThread,
    Media,
)


class InstDispatcher:
    
    def __init__(self, client: Client):
        self._cl = client
        super().__init__()