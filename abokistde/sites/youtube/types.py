from typing import TypedDict


class Channel(TypedDict):
    name: str
    url: str
    channel_id: str
    thumbnail_url: str


class YtEpisode(TypedDict):
    title: str
    url: str
    episode_id: str
    thumbnail_url: str
    channel_id: str
