from abokistde.models import PublishingChannel, Episode, User, Provider
from .graphql import GraphQlClient

class Ardaudiothek:
    def __init__(self):
        # self.provider = Provider.objects.filter(extractor__name = 'ardaudiothek')[0]
        pass
    
    def getChannels(self):
        graphql = GraphQlClient()
        graphql.getChannels()