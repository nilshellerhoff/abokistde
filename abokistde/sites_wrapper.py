from abokistde.sites import youtube

def getNewEpisodes():
    """Get new episodes from all sites"""
    youtube.getNewEpisodes()

def getChannelInfo(url : str):
    """get the channel info from the given url"""
    return youtube.getChannelInfo(url)