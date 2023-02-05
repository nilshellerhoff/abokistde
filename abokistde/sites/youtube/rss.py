## Use the youtube RSS url to get information

import requests
import xmltodict

class RssFeed:
    def __init__(self, channel_id: str):
        self.url = "https://www.youtube.com/feeds/videos.xml?channel_id=" + channel_id
        self.xml = requests.get(self.url).text
        self.data = xmltodict.parse(self.xml)

    def getChannelDetails(self):
        """
        Fetches channel details from a 
        """
        channel_url = self.data["feed"]["author"]["uri"]
        name = self.data["feed"]["author"]["name"]
        return {
            "channel_id": channel_url.split("/")[-1],
            "name": name,
            "url": channel_url,
            "channel_created": self.data["feed"]["published"],
        }

    def getVideos(self):
        """
        Returns a list of the 15 latest videos
        """
        videos = []
        for video in self.data["feed"]["entry"]:
            videos.append({
                "title": video["title"],
                "url": video["link"]["@href"],
                "thumbnail_url": video["media:group"]["media:thumbnail"]["@url"],
                "published": video["published"],
                "description": video["media:group"]["media:description"],
                "video_id": video["yt:videoId"],
            })
        return videos