from .base import BaseFilter
from instagrapi.types import DirectMessage
from instdp.types import DirectItemType
from typing import Union, List

class ItemTypeFilter(BaseFilter):
    def __init__(self, item_type: Union[List[Union[DirectItemType, str]], DirectItemType, str]):
        super().__init__()
        if isinstance(item_type, str) or isinstance(item_type, DirectItemType):
            self.item_types = [item_type]
        else:
            self.item_types = item_type

    def check(self, msg: DirectMessage, **kwargs):
        if not self.item_types:
            return True

        for item_type in self.item_types:
            if isinstance(item_type, DirectItemType) and item_type.value == msg.item_type:
                return True
            elif msg.item_type == item_type:
                return True
        return False

