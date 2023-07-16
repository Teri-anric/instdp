from .base import BaseFilter
from instagrapi.types import DirectMessage
from instdp.types import DirectItemType
from typing import Union, List

class ItemTypeFilter(BaseFilter):
    def __init__(self, item_type: Union[List[DirectItemType], DirectItemType]):
        super().__init__()
        if isinstance(self.item_type, str):
            self.item_types = [item_type]
        else:
            self.item_types = item_type

    def check(self, msg: DirectMessage, **kwargs):
        if not self.item_types:
            return True

        for item_type in self.item_types:
            if msg.item_type == item_type:
                return True
        return False

