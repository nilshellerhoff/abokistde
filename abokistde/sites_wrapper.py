from typing import List

from abokistde.sites import youtube
from .models import PublishingChannel, Extractor
from abokistde.sites.youtube import Youtube
from abokistde.sites.ardaudiothek import Ardaudiothek
from .sites.mediathekviewweb import MediathekViewWeb


def getNewEpisodes(channel_id=None):
    """Get new episodes from all sites"""
    if channel_id:
        channels = [PublishingChannel.objects.get(pk=channel_id)]
    else:
        channels = PublishingChannel.objects.filter(usersubscription__user__isnull=False).distinct()
    yt = Youtube()
    aa = Ardaudiothek()
    mv = MediathekViewWeb()
    for channel in channels:
        if channel.provider.extractor.name == 'youtube':
            yt.getVideos(channel)
        elif channel.provider.extractor.name == 'ardaudiothek':
            aa.getEpisodes(channel)
        elif channel.provider.extractor.name == "mediathekviewweb":
            mv.getEpisodes(channel)
        else:
            raise "Extractor not supported"


def getChannelInfo(url : str):
    """get the channel info from the given url"""
    youtube = Youtube()
    return youtube.getChannelInfo(url)


def search(query : str) -> List[PublishingChannel]:
    """Search for a query"""
    youtube = Youtube()
    mv = MediathekViewWeb()
    return [*youtube.searchChannel(query), *mv.searchChannel(query)]


def fetch_data(extractor: Extractor):
    """Fetch data from the given extractor"""
    if extractor.name == 'youtube':
        yt = Youtube()
        for channel in getWatchedChannels():
            yt.getVideos(channel)
    if extractor.name == 'ardaudiothek':
        aa = Ardaudiothek()
        aa.getChannels()
    if extractor.name == 'mediathekviewweb':
        mv = MediathekViewWeb()
        mv.getChannels()