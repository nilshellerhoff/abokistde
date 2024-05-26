from __future__ import annotations

from typing import List, TypedDict

from abokistde.models import PublishingChannel, Episode, User, Provider, Extractor
import xmltodict
import requests
from .jsonscraper import JsonScraper
from .rss import RssFeed


class Youtube:
    def __init__(self):
        self.provider, created = Provider.objects.update_or_create(
            name="Youtube",
            defaults=dict(
                url="https://www.youtube.com/",
                icon_url="https://www.youtube.com/s/desktop/5191a190/img/favicon_144x144.png",
                extractor=Extractor.objects.get(name='youtube')
            )
        )

    def search(self, query: str) -> TypedDict('ChannelEpisode',
                                              {'channel': List[PublishingChannel], 'episode': List[Episode]}):
        try:
            channels: List[PublishingChannel] = []
            episodes: List[Episode] = []

            j = JsonScraper()
            results_channels, results_episodes = j.search_channel(query)

            for channel in results_channels:
                channel_obj, _ = PublishingChannel.objects.update_or_create(
                    channel_id=channel["channel_id"],
                    defaults=dict(
                        name=channel["name"],
                        url=channel["url"],
                        provider=self.provider,
                        thumbnail_url=channel["thumbnail_url"]
                    )
                )
                channels.append(channel_obj)

            for episode in results_episodes:
                episode_obj, _ = Episode.objects.update_or_create(
                    episode_id=episode["episode_id"],
                    defaults={
                        "publishing_channel": PublishingChannel.objects.get(channel_id=episode["channel_id"]),
                        "title": episode["title"],
                        "url": episode["url"],
                        "thumbnail_url": episode["thumbnail_url"],
                        "type": "video"
                    }
                )
                episodes.append(episode_obj)

            return {"channel": channels, "episode": episodes}

        except Exception as e:
            print(e)
            return {"channel": [], "episode": []}

    def get_channel_info(self, url: str) -> PublishingChannel:
        try:
            j = JsonScraper()
            channel = j.get_channel_details(url)
            return PublishingChannel.objects.update_or_create(
                channel_id=channel["channel_id"],
                defaults={
                    "name": channel["name"],
                    "description": channel["description"],
                    "url": channel["url"],
                    "channel_id": channel["channel_id"],
                    "thumbnail_url": channel["thumbnail_url"],
                }
            )[0]
        except Exception as e:
            print(e)
            return None

    def get_videos(self, channel: PublishingChannel) -> List[Episode]:
        """
        Returns the latest videos, currently 15 using the rss api
        """
        try:
            rss_extractor = RssFeed(channel.channel_id)
            videos = []
            for video in rss_extractor.getVideos():
                videos.append(Episode.objects.update_or_create(
                    episode_id=video["video_id"],
                    defaults=dict(
                        publishing_channel=channel,
                        title=video["title"],
                        url=video["url"],
                        thumbnail_url=video["thumbnail_url"],
                        description=video["description"],
                        published=video["published"],
                        type="video",
                    )
                )[0])

            return videos
        except Exception as e:
            print(e)
            return []
