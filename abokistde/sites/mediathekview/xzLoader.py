import lzma
import requests
import re
import json
from abokistde.models import PublishingChannel, Episode, User, Provider, Extractor
from datetime import datetime, timezone

class xzLoader:
    def __init__(self) -> None:
        self.urlNew = "http://verteiler1.mediathekview.de/Filmliste-diff.xz"
        self.urlOld = "http://verteiler1.mediathekview.de/Filmliste-akt.xz"
        self.extractor = Extractor.objects.get_or_create(name='mediathekview')[0]

    def loadFile(self, url):
        r = requests.get(url)
        data = lzma.decompress(r.content)
        return data.decode("utf-8")

    def parseData(self, data):
        """Parse the data (it is in some JSON form, but with identical keys)"""
        data = data.replace("{", "[").replace("}", "]")
        data = re.sub(r'"[A-Za-z0-9_]*":', "", data)
        with open("data.json", "w") as f:
            f.write(data)
        return data
    
    def getJson(self, data):
        return json.loads(self.parseData(data))

    def getCsv(self, data):
        return self.parseData(data).replace(" ", "").replace("],[", "\n").replace("[", "").replace("]", "")

    def loadNew(self):
        data = self.loadFile(self.urlNew)
        metadata, headers, *videos = self.getJson(data)

        print(f"Loaded {len(videos)} videos")

        # for v in videos:
        #     provider, _ = Provider.objects.update_or_create(
        #         name = v[0],
        #         extractor = self.extractor
        #     )

        #     channel, _ = PublishingChannel.objects.update_or_create(
        #         name = v[1],
        #         provider = provider
        #     )

        #     dur_parts = [int(x) for x in v[5].split(":")]
        #     dur_secs = dur_parts[0] * 60 * 60 + dur_parts[1] * 60 + dur_parts[2]
        #     published = datetime.fromtimestamp(int(v[16]), tz=timezone.utc).isoformat() if v[16] != "" else None

        #     episode, _ = Episode.objects.update_or_create(
        #         title=v[2],
        #         publishing_channel = channel,
        #         defaults=dict(
        #             description=v[7],
        #             type="video",
        #             url=v[9],
        #             duration = dur_secs,
        #             published = published,
        #         )
        #     )

    def load(self, path):
        with lzma.open(path, 'rb') as f:
            return f.read()

if __name__ == "__main__":
    xz = xzLoader()
    xz.loadNew()