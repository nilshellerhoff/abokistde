from abokistde.sites import youtube
from .models import PublishingChannel, Extractor
from abokistde.sites.youtube import Youtube

def getWatchedChannels():
    """Get all channels that are watched"""
    return PublishingChannel.objects.filter(usersubscription__user__isnull=False).distinct()

def getNewEpisodes():
    """Get new episodes from all sites"""
    channels_watched = getWatchedChannels()
    yt = Youtube()
    for channel in channels_watched:
        if channel.provider.extractor.name == 'youtube':
            yt.getVideos(channel)

def getChannelInfo(url : str):
    """get the channel info from the given url"""
    youtube = Youtube()
    return youtube.getChannelInfo(url)

def search(query : str):
    """Search for a query"""
    youtube = Youtube()
    return youtube.searchChannel(query)

def fetch_data(extractor: Extractor):
    """Fetch data from the given extractor"""
    if extractor.name == 'youtube':
        yt = Youtube()
        for channel in getWatchedChannels():
            yt.getVideos(channel)