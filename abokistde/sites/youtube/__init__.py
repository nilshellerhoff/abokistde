from abokistde.models import PublishingChannel, Episode, User, Provider
import xmltodict
import requests
from .jsonscraper import JsonScraper
from .rss import RssFeed

class Youtube:
    def __init__(self):
        self.provider = Provider.objects.filter(extractor__name = 'youtube')[0]

    def searchChannel(self, query):
        j = JsonScraper()
        channels = []
        for channel in j.searchChannel(query):
            channels.append(PublishingChannel.objects.update_or_create(
                channel_id = channel["channel_id"],
                defaults = dict(
                    name = channel["name"],
                    url = channel["url"],
                    provider = self.provider
                )
            )[0])

        return channels

    def getChannelInfo(self, url):
        j = JsonScraper()
        channel = j.getChannelDetails(url)
        return PublishingChannel.objects.update_or_create(
            channel_id = channel["channel_id"],
            defaults= {
                "name": channel["name"],
                "description": channel["description"],
                "url": channel["url"],
                "channel_id": channel["channel_id"],
                "thumbnail_url": channel["thumbnail_url"],
            }
        )[0]

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