from .xzLoader import xzLoader

class Mediathekview:
    def __init__(self):
        pass

    def getChannels(self):
        xz = xzLoader()
        return xz.loadNew()
        
    def getEpisodes(self, publishing_channel):
        xz = xzLoader()
        return xz.loadNew()
