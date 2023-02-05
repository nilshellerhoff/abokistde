from abokistde.models import PublishingChannel, Episode, User
import xmltodict
import requests
from .jsonscraper import JsonScraper
from .rss import RssFeed

class Youtube:
    def __init__(self):
        pass

    def searchChannel(self, query):
        j = JsonScraper()
        channels = []
        for channel in j.searchChannel(query):
            channels.append(PublishingChannel.objects.update_or_create(
                channel_id = channel["channel_id"],
                defaults = dict(
                    name = channel["name"],
                    url = channel["url"],
                    provider = "youtube",
                )
            )[0])

        return channels

    def getVideos(self, channel):
        """
        Returns the latest videos, currently 15 using the rss api
        """
        rss = RssFeed(channel.channel_id)
        videos = []
        for video in rss.getVideos():
            videos.append(Episode.objects.update_or_create(
                episode_id = video["video_id"],
                defaults = dict(
                    publishing_channel = channel,
                    title = video["title"],
                    url = video["url"],
                    thumbnail_url = video["thumbnail_url"],
                    description = video["description"],
                    published = video["published"],
                    type = "video",
                )
            )[0])
        
        return videos