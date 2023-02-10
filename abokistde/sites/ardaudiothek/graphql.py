from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from abokistde.models import PublishingChannel, Episode, User, Provider, Extractor

class GraphQlClient:
    def __init__(self):
        self.url = "https://api.ardaudiothek.de/graphql"
        transport = AIOHTTPTransport(url=self.url)
        self.client = Client(transport=transport, fetch_schema_from_transport=True)
        self.extractor = Extractor.objects.get(name='ardaudiothek')
        
    def getChannels(self):
        query = gql("""
{
  programSets {
    nodes {
      title
      synopsis
      sharingUrl
      rowId
      image { url }
      publicationService {
        title
        homepageUrl
        image { url }
      }
    }
  }
}
""")
        result = self.client.execute(query)

        for node in result['programSets']['nodes']:
            provider, created = Provider.objects.update_or_create(
                name = node['publicationService']['title'],
                defaults = dict(
                    url=node['publicationService']['homepageUrl'],
                    icon_url=node['publicationService']['image']['url'].replace("{width}", "128"),
                    extractor=self.extractor
                )
            )

            channel, created = PublishingChannel.objects.update_or_create(
                name = node['title'],
                provider = provider,
                defaults = dict(
                    description = node['synopsis'],
                    url = node['sharingUrl'],
                    channel_id = node['rowId'],
                    thumbnail_url = node['image']['url'].replace("{width}", "128") if node['image'] else None
                )
            )