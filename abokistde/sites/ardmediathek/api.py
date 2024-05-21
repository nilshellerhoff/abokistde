from typing import List, Dict, Any

import requests

from abokistde.models import PublishingChannel, Provider


class Api:
    def __init__(self):
        self.api_base = "https://api.ardmediathek.de"
        self.extractor = "ardmediathek"

    def search_channel(self, query: str) -> List[PublishingChannel]:
        """
        Searches for a channel by query
        """
        url = f"{self.api_base}/search-system/search/shows/ard"
        params = {
            "query": query,
            "pageSize": 48,
            "childCont": False,
            "platform": "MEDIA_THEK"
        }

        r = requests.get(url, params=params)
        return self.parse_show_reponse(r.json())

    def parse_show_reponse(self, data: Dict[str, Any]) -> List[PublishingChannel]:
        channels = []
        for show in data["teasers"]:
            provider_name = show["publicationService"]["name"] if "publicationService" in show else "ARD"
            provider, _ = Provider.objects.update_or_create(extractor=self.extractor, name=provider_name)

            channel_id = show["links"]["target"]["urlId"]
            channel, _ = PublishingChannel.objects.update_or_create(provider=provider, channel_id=show["id"], defaults={
                "name": show["mediumTitle"],
                "url": show[]

            }