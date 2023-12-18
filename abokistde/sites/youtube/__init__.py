from abokistde.models import PublishingChannel, Episode, User, Provider, Extractor
import xmltodict
import requests
from .jsonscraper import JsonScraper
from .rss import RssFeed

class Youtube:
    def __init__(self):
        self.provider, created = Provider.objects.update_or_create(
            name = "Youtube",
            defaults = dict(
                url = "https://www.youtube.com/",
                icon_url = "https://www.youtube.com/s/desktop/5191a190/img/favicon_144x144.png",
                extractor = Extractor.objects.get(name='youtube')
            )
        )
        
    def searchChannel(self, query):
        try:
            j = JsonScraper()
            channels = []
            for channel in j.searchChannel(query):
                    channels.append(PublishingChannel.objects.update_or_create(
                    channel_id = channel["channel_id"],
                    defaults = dict(
                        name = channel["name"],
                        url = channel["url"],
                        provider = self.provider,
                        thumbnail_url = channel["thumbnail_url"]
                    )
                )[0])

            return channels
        except Exception as e:
            print(e)
            return []

    def getChannelInfo(self, url):
        try:
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
        except Exception as e:
            print(e)
            return None

    def getVideos(self, channel):
        """
        Returns the latest videos, currently 15 using the rss api
        """
        try:
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
        except Exception as e:
            print(e)
            return []