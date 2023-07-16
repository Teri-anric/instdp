from enum import Enum

class MessageType(Enum):
    voice = 'voice_media'
    placeholder = 'placeholder'
    text = 'text'
    video_call = 'video_call_event'
    raven_media = 'raven_media'
    reel = 'reel_share'
    media_share = 'media_share'
    link = 'link'
    media = 'media'
    action_log = 'action_log'
    like = 'like'
