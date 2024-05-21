from typing import List

from abokistde.models import Provider, Extractor, PublishingChannel


class ArdMediathek:
    def __init__(self):
        self.extractor, _ = Extractor.objects.get_or_create(name="ardmediathek")
        self.api_base = "https://api.ardmediathek.de/page-gateway/widgets/ard/api/v1"

    def searchChannel(self, query: str) -> List[PublishingChannel]:


    def getChannelInfo(self, url):
        try:
            j = JsonScraper()
            channel = j.getChannelDetails(url)
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

    def getVideos(self, channel):
        """
        Returns the latest videos, currently 15 using the rss api
        """
        try:
            rss = RssFeed(channel.channel_id)
            videos = []
            for video in rss.getVideos():
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