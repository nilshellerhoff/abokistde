from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from abokistde.models import PublishingChannel, Episode, User, Provider, Extractor


class GraphQlClient:
    def __init__(self):
        self.url = "https://api.ardaudiothek.de/graphql"
        transport = AIOHTTPTransport(url=self.url)
        self.client = Client(transport=transport,
                             fetch_schema_from_transport=True)
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
        channels = []
        for node in result['programSets']['nodes']:
            provider, created = Provider.objects.update_or_create(
                name=node['publicationService']['title'],
                defaults=dict(
                    url=node['publicationService']['homepageUrl'],
                    icon_url=node['publicationService']['image']['url'].replace(
                        "{width}", "128"),
                    extractor=self.extractor
                )
            )

            channel, created = PublishingChannel.objects.update_or_create(
                name=node['title'],
                provider=provider,
                defaults=dict(
                    description=node['synopsis'],
                    url=node['sharingUrl'],
                    channel_id=node['rowId'],
                    thumbnail_url=node['image']['url'].replace(
                        "{width}", "128") if node['image'] else None
                )
            )

            channels.append(channel)

        return channels

    def getEpisodes(self, publishing_channel):
        channel_id = publishing_channel.channel_id

        query = gql("""
query getEpisodes ($channel_id: Int!) {
    programSets (filter: { id: { equalTo: $channel_id }}) {
        nodes {
            items (orderBy: PUBLISH_DATE_DESC first: 20 filter: { isPublished: {equalTo: true}}) {nodes{
                title
                synopsis
                sharingUrl
                rowId
                image { url }
                duration
                firstPublishDate
            }}
        }
    }
}
""")

        params = {"channel_id": int(channel_id)}


        result = self.client.execute(query, variable_values=params)
        episodes = []
        for node in result['programSets']['nodes'][0]['items']['nodes']:
            episode, created = Episode.objects.update_or_create(
                episode_id = node['rowId'],
                defaults=dict(
                    title=node['title'],
                    description=node['synopsis'],
                    url=node['sharingUrl'],
                    thumbnail_url=node['image']['url'].replace("{width}", "1280") if node['image'] else None,
                    duration=node['duration'],
                    published=node['firstPublishDate'],
                    publishing_channel=publishing_channel
                )
            )
            episodes.append(episode)

        return episodes
        