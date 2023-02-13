from abokistde.models import PublishingChannel, Episode, User, Provider
from .graphql import GraphQlClient

class Ardaudiothek:
    def __init__(self):
        # self.provider = Provider.objects.filter(extractor__name = 'ardaudiothek')[0]
        pass
    
    def getChannels(self):
        try:
            graphql = GraphQlClient()
            return graphql.getChannels()
        except Exception as e:
            print(e)
            return []

    def getEpisodes(self, publishing_channel):
        try:
            graphql = GraphQlClient()
            return graphql.getEpisodes(publishing_channel)
        except Exception as e:
            print(e)
            return []