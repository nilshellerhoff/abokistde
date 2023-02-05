"""
Scraping YouTube using JSON embedded in the HTML

When loading a YouTube page, the initial data is embedded in the HTML as JSON in the variable ytInitialData. We can use this to scrape the data we need, although in a somewhat limited way.
"""

import requests
import json
import os
import re
from .nestedobject import NestedObject

__DIR__ = os.path.dirname(os.path.realpath(__file__))

class JsonScraper:
    def __init__(self, cookies=None, headers=None):
        self._setCookies(cookies)
        self._setHeaders(headers)

    def _setCookies(self, cookies):
        if cookies:
            self.cookies = cookies
        else:
            cookiepath = os.path.join(__DIR__, "jsonscraper-cookies.json")
            with open(cookiepath, "r") as f:
                cookies_loaded = json.load(f)
            
            self.cookies = {}
            for c in cookies_loaded:
                self.cookies[c["Name raw"]] = c["Content raw"]
   
    def _setHeaders(self, headers):
        if headers:
            self.headers = headers
        else:
            self.headers = {
                "User-Agent" : "Mozilla/5.0 (Linux; Android 8.0.0; PRA-LX3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36",
                "Accept-Language" : "en-US,en;q=0.5"
            }

    def getHtml(self):
        r = requests.get(self.url, headers=self.headers, cookies=self.cookies)
        # decode string sequences like \x22
        self.html = r.text

    def decodeJson(self, json):
        # if the string starts with a single quote, we need to decode the string
        if json[0] == "'":
            json = json[1:-1]
            json = json.encode('utf-8').decode('unicode_escape')
            json.replace("\/", "/")

        return json

    def getJson(self):
        self.getHtml()
        initialData = self.html.split('var ytInitialData = ')[1].split(';</script>')[0].strip()
        initialData = self.decodeJson(initialData)
        self.json = NestedObject(json.loads(initialData))

    def getChannelDetails(self, url):
        self.url = url
        self.getJson()

        channel_id = self.json["responseContext"]["serviceTrackingParams"]['_["service"] == "GFEEDBACK"'][0]["params"]['_["key"] == "browse_id"'][0]["value"]
        # allVideosPlaylist = self.json["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"].filter(
        #     lambda x: x["itemSectionRenderer"]["contents"][0]["shelfRenderer"] and x["itemSectionRenderer"]["contents"][0]["shelfRenderer"]["title"]["runs"][0]["text"] == "Videos"
        # )[0]["itemSectionRenderer"]["contents"][0]["shelfRenderer"]["playAllButton"]["buttonRenderer"]["navigationEndpoint"]["watchEndpoint"]["playlistId"]

        name = self.json["metadata"]["channelMetadataRenderer"]["title"]
        description = self.json["metadata"]["channelMetadataRenderer"]["description"]
        url = self.json["metadata"]["channelMetadataRenderer"]["channelUrl"] # with channel id
        # url = self.json["metadata"]["channelMetadataRenderer"]["vanityChannelUrl"] # with handle
        thumbnail_url = self.json["metadata"]["channelMetadataRenderer"]["avatar"]["thumbnails"][-1]["url"]

        return {
            "name": name,
            "description": description,
            "url": url,
            "channel_id": channel_id,
            "thumbnail_url": thumbnail_url,
        }

    def searchChannel(self, query):
        """
        Perform a search on YouTube and return all the channels of all the videos
        """
        self.url = f"https://www.youtube.com/results?search_query={query}"
        self.getJson()

        videoItems = self.json["contents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"].filter(lambda x: "videoWithContextRenderer" in x.keys())
        byLineTexts = videoItems.map(lambda x: x["videoWithContextRenderer"]["shortBylineText"]["runs"][0])

        return [{
            "name": x["text"],
            "url": x["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"],
            "id": x["navigationEndpoint"]["browseEndpoint"]["browseId"],
        } for x in byLineTexts]