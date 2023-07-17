from io import BytesIO
from pathlib import Path
from pathlib import PurePath
from tempfile import NamedTemporaryFile
from typing import List
from typing import Union

from instagrapi import Client
from instagrapi.exceptions import ClientNotFoundError, DirectThreadNotFound
from instagrapi.extractors import (
    extract_direct_response,
    extract_direct_thread,
)
from instagrapi.types import (
    DirectMessage,
    DirectResponse,
    DirectShortThread,
    DirectThread,
    Media,
)


class MixinDirectAPI:
    _cl: Client

    def message_seen(self, message: DirectMessage) -> DirectResponse:
        result = self._cl.private_request(
            f"direct_v2/threads/{message.thread_id}/items/{message.id}/seen/",
            data=self._cl.with_default_data({}),
            with_signature=False,
        )
        return extract_direct_response(result)

    def answer_message(self, message: DirectMessage, text: str) -> DirectMessage:
        return self._cl.direct_answer(thread_id=message.thread_id, text=text)

    def send_message(self, thread_id: int, text: str) -> DirectMessage:
        return self._cl.direct_answer(thread_id=thread_id, text=text)

    def send_message_to_user(self, user_id: int, text: str) -> DirectMessage:
        return self._cl.direct_send(text=text, user_ids=[user_id])

    def send_message_to_users(self, user_ids: List[int], text: str) -> DirectMessage:
        return self._cl.direct_send(user_ids=user_ids, text=text)

    def send_message_to_threads(self, thread_ids: List[int], text: str):
        return self._cl.direct_send(thread_ids=thread_ids, text=text)

    def direct_thread_to_msg_id(self, thread_id: str, cursor: str = None, to_msg_id: int = None,
                                max_msg: int = None) -> DirectThread:
        assert self._cl.user_id, "Login required"
        params = {
            "visual_message_return_type": "unseen",
            "direction": "older",
            "seq_id": "40065",  # 59663
            "limit": "20",
        }
        items = []
        while True:
            if cursor:
                params["cursor"] = cursor
            try:
                result = self._cl.private_request(
                    f"direct_v2/threads/{thread_id}/", params=params
                )
            except ClientNotFoundError as e:
                raise DirectThreadNotFound(e, thread_id=thread_id, **self._cl.last_json)
            thread = result["thread"]
            for item in thread["items"]:
                items.append(item)
                if item.get('item_id', None) == to_msg_id:
                    break
            cursor = thread.get("oldest_cursor")
            if not cursor or cursor == "MINCURSOR" or (max_msg and len(items) == max_msg):
                break
        thread["items"] = items
        return extract_direct_thread(thread)

    def _send_file(self, file: Union[Path, BytesIO, str], user_ids: list[int] = None, thread_ids: list[int] = None,
                   bufsize: int = 16384, content_type="photo") -> DirectMessage:
        if not user_ids:
            user_ids = []
        if not thread_ids:
            thread_ids = []
        if isinstance(file, PurePath) or isinstance(file, str):
            return self._cl.direct_send_file(path=Path(file), user_ids=user_ids, thread_ids=thread_ids)

        with NamedTemporaryFile(delete=True) as fp:
            file.seek(0)
            while True:
                buf = file.read(bufsize)
                if not buf:
                    break
                fp.write(buf)
            file.seek(0)
            path = Path(fp.name)
            return self._cl.direct_send_file(path=path, user_ids=user_ids, thread_ids=thread_ids)

    def answer_photo(self, message: DirectMessage, photo: Union[Path, BytesIO, str], bufsize: int = 16384):
        return self.send_photo(thread_id=message.thread_id, photo=photo, bufsize=bufsize)

    def send_photo(self, thread_id: int, photo: Union[Path, BytesIO, str], bufsize: int = 16384):
        return self._send_file(file=photo, thread_ids=[thread_id], bufsize=bufsize, content_type="photo")

    def send_photo_to_threads(self, thread_ids: List[int], photo: Union[Path, BytesIO, str], bufsize: int = 16384):
        return self._send_file(file=photo, thread_ids=thread_ids, bufsize=bufsize, content_type="photo")

    def send_photo_to_user(self, user_id: int, photo: Union[Path, BytesIO, str], bufsize: int = 16384):
        return self._send_file(file=photo, user_ids=[user_id], bufsize=bufsize, content_type="photo")

    def send_photo_to_users(self, user_ids: List[int], photo: Union[Path, BytesIO, str], bufsize: int = 16384):
        return self._send_file(file=photo, user_ids=user_ids, bufsize=bufsize, content_type="photo")

    def answer_video(self, message: DirectMessage, video: Union[Path, BytesIO, str], bufsize: int = 16384):
        return self.send_video(thread_id=message.thread_id, video=video, bufsize=bufsize)

    def send_video(self, thread_id: int, video: Union[Path, BytesIO, str], bufsize: int = 16384):
        return self._send_file(file=video, thread_ids=[thread_id], bufsize=bufsize, content_type="video")

    def send_video_to_threads(self, thread_ids: List[int], video: Union[Path, BytesIO, str], bufsize: int = 16384):
        return self._send_file(file=video, thread_ids=thread_ids, bufsize=bufsize, content_type="video")

    def send_video_to_user(self, user_id: int, video: Union[Path, BytesIO, str], bufsize: int = 16384):
        return self._send_file(file=video, user_ids=[user_id], bufsize=bufsize, content_type="video")

    def send_video_to_users(self, user_ids: List[int], video: Union[Path, BytesIO, str], bufsize: int = 16384):
        return self._send_file(file=video, user_ids=user_ids, bufsize=bufsize, content_type="video")

    def search_direct(self, query: str) -> List[DirectShortThread]:
        return self._cl.direct_search(query=query)

    def thread_by_participants(self, user_ids: List[int]) -> DirectThread:
        return self._cl.direct_thread_by_participants(user_ids=user_ids)

    def delete_thread(self, thread_id: int) -> bool:
        return self._cl.direct_thread_hide(thread_id=thread_id)

    def media_share(self, media_id: str, user_id: int) -> DirectMessage:
        return self._cl.direct_media_share(media_id=media_id, user_ids=[user_id])

    def media_share_to_users(self, media_id: str, user_ids: List[int]) -> DirectMessage:
        return self._cl.direct_media_share(media_id=media_id, user_ids=user_ids)

    def answer_story_share(self, message: DirectMessage, story_id: str) -> DirectMessage:
        return self.story_share(story_id=story_id, thread_id=message.thread_id)

    def story_share(self, thread_id: int, story_id: str) -> DirectMessage:
        return self._cl.direct_story_share(story_id=story_id, thread_ids=[thread_id])

    def story_share_to_threads(self, thread_ids: List[int], story_id: str) -> DirectMessage:
        return self._cl.direct_story_share(story_id=story_id, thread_ids=thread_ids)

    def story_share_to_user(self, user_id: int, story_id: str) -> DirectMessage:
        return self._cl.direct_story_share(story_id=story_id, user_ids=[user_id])

    def story_share_to_users(self, user_ids: List[int], story_id: str) -> DirectMessage:
        return self._cl.direct_story_share(story_id=story_id, user_ids=user_ids)

    def thread_mark_unread(self, thread_id: int) -> bool:
        return self._cl.direct_thread_mark_unread(thread_id=thread_id)

    def message_delete(self, thread_id: int, message_id: int) -> bool:
        return self._cl.direct_message_delete(thread_id=thread_id, message_id=message_id)

    def delete_message(self, message: DirectMessage) -> bool:
        return self._cl.direct_message_delete(thread_id=message.thread_id, message_id=int(message.id))

    def answer_profile_share(self, message: DirectMessage, user_id: str) -> DirectMessage:
        return self.profile_share(thread_id=message.thread_id, user_id=user_id)

    def profile_share(self, user_id: str, thread_id: int) -> DirectMessage:
        return self._cl.direct_profile_share(user_id=user_id, thread_ids=[thread_id])

    def profile_share_to_threads(self, user_id: str, thread_ids: List[int]) -> DirectMessage:
        return self._cl.direct_profile_share(user_id=user_id, thread_ids=thread_ids)

    def profile_share_to_user(self, user_id: str, to_user_id: int) -> DirectMessage:
        return self._cl.direct_profile_share(user_id=user_id, user_ids=[to_user_id])

    def profile_share_to_users(self, user_id: str, to_user_ids: List[int]) -> DirectMessage:
        return self._cl.direct_profile_share(user_id=user_id, user_ids=to_user_ids)

    def direct_media(self, thread_id: int, amount: int = 20) -> List[Media]:
        return self._cl.direct_media(thread_id=thread_id, amount=amount)
