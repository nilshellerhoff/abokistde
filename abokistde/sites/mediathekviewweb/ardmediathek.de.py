import requests
import re

EPISODE_API_URL = "https://api.ardmediathek.de/page-gateway/pages/ard/item/{episode_id}"

class ArdMediathekScraper:
    def get_channel_info(self, video_url):
        episode_id = re.search(r"/([A-Za-z0-9]{50,})/$", video_url).group(1)
        r = requests.get(EPISODE_API_URL.format(episode_id=episode_id))
        data = r.json()