from abokistde.models import PublishingChannel, Episode, User
import xmltodict
import requests
import re

def getNewEpisodes():
    """Get new videos from youtube"""

    channels = _getWatchedChannels()
    _getNewVideosChannels(channels)

# this is deprecated only for old frontend
def getChannelInfo(url : str):
    """get the channel info from the given url"""

    if "@" in url:
        # this is a user url like youtube.com/@LinusTechTips
        xmlurl = "https://www.youtube.com/feeds/videos.xml?user=" + url.split("@")[-1].split("/")[0].split("?")[0]
    else:
        # we assume this is a channel url like youtube.com/channel/UCXuqSBlHAE6Xw-yeJA0Tunw
        xmlurl = "https://www.youtube.com/feeds/videos.xml?channel_id=" + url.split("/")[-1].split("?")[0]
    
    xml = requests.get(xmlurl).text
    data = xmltodict.parse(xml)

    channel_url = data["feed"]["author"]["uri"]
    name = data["feed"]["author"]["name"]
    return {
        "provider": "youtube",
        "channel_id": channel_url.split("/")[-1],
        "name": name,
        "thumbnail": "",
        "url": channel_url,
    }

def _getWatchedChannels():
    """get the channels which are watched"""
    return PublishingChannel.objects.all()

def _getNewVideosChannels(channels: list[PublishingChannel]):
    """get all new videos from the given channels"""

    for channel in channels:
        _getNewVideosChannel(channel)

def _getNewVideosChannel(channel: PublishingChannel):
    """get all new videos from the given channel"""
    
    channelId = PublishingChannel.channel_id
    
    # TODO error handling
    if channelId is None:
        return
    
    _getNewVideosXml(channel)

def _getNewVideosXml(channel: PublishingChannel):
    """use the rss api to fetch the videos"""

    url = "https://www.youtube.com/feeds/videos.xml?channel_id=" + channel.channel_id

    xml = requests.get(url).text
    data = xmltodict.parse(xml)

    for v in data["feed"]["entry"]:
        Episode.objects.update_or_create(
            episode_id = v["yt:videoId"],
            defaults = dict(
                title = v["title"],
                description = v["media:group"]["media:description"],
                type = "video",
                url = v["link"]["@href"],
                thumbnail_url = v["media:group"]["media:thumbnail"]["@url"].replace("hqdefault", "maxresdefault"),
                duration = None,
                viewcount = v["media:group"]["media:community"]["media:statistics"]["@views"],
                published = v["published"],
                updated = v["updated"],
                publishing_channel = channel,
            )
        )