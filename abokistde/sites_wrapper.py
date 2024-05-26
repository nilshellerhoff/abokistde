from typing import Dict, TypedDict, List

from abokistde.sites import youtube
from .models import PublishingChannel, Extractor, Episode
from abokistde.sites.youtube import Youtube
from abokistde.sites.ardaudiothek import Ardaudiothek

def getNewEpisodes(channel_id=None):
    """Get new episodes from all sites"""
    if channel_id:
        channels = [PublishingChannel.objects.get(pk=channel_id)]
    else:
        channels = PublishingChannel.objects.filter(usersubscription__user__isnull=False).distinct()
    yt = Youtube()
    aa = Ardaudiothek()
    for channel in channels:
        if channel.provider.extractor.name == 'youtube':
            yt.get_videos(channel)
        if channel.provider.extractor.name == 'ardaudiothek':
            aa.getEpisodes(channel)

def getChannelInfo(url : str):
    """get the channel info from the given url"""
    youtube = Youtube()
    return youtube.get_channel_info(url)


def search(query: str) -> TypedDict('ChannelEpisode', {'channel': List[PublishingChannel], 'episode': List[Episode]}):
    """Search for a query"""
    youtube = Youtube()
    return youtube.search(query)


def fetch_data(extractor: Extractor):
    """Fetch data from the given extractor"""
    if extractor.name == 'youtube':
        yt = Youtube()
        for channel in getWatchedChannels():
            yt.get_videos(channel)
    if extractor.name == 'ardaudiothek':
        aa = Ardaudiothek()
        aa.getChannels()