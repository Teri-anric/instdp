from typing import Union, List

from instagrapi.types import DirectMessage

from ..types import DirectItemType
from .base import BaseFilter


class ItemTypeFilter(BaseFilter):
    def __init__(self, item_type: Union[List[Union[DirectItemType, str]], DirectItemType, str]):
        if isinstance(item_type, (str, DirectItemType)):
            self.item_types = [item_type]
        else:
            self.item_types = item_type

    def __call__(self, msg: DirectMessage, **kwargs) -> bool:
        if not self.item_types:
            return True

        for item_type in self.item_types:
            if isinstance(item_type, DirectItemType) and item_type.value == msg.item_type:
                return True
            if msg.item_type == item_type:
                return True
        return False
