from django.db import models
from django.contrib.auth.models import User


class Extractor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Provider(models.Model):
    # display name of the provider (e.g. 'YouTube')
    name = models.CharField(max_length=200)
    # URL to the provider's website
    url = models.URLField()
    # icon URL
    icon_url = models.URLField()
    # extractor: which module is used to extract the data from the provider
    extractor = models.ForeignKey(Extractor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def toDict(self):
        return {
            "extractor": self.extractor.name,
            "name": self.name,
            "url": self.url,
            "icon_url": self.icon_url
        }


class PublishingChannel(models.Model):
    # Name as displayed on the website
    name = models.CharField(max_length=200)
    # Description of what the channel typically publishes (if available)
    description = models.TextField(null=True, blank=True)
    # URL to the channel's website
    url = models.URLField()
    # Channel ID as used by the provider (e.g. 'UCXuqSBlHAE6Xw-yeJA0Tunw' for LTT on youtube)
    channel_id = models.CharField(max_length=200, null=True, blank=True)
    # URL to a thumbnail image of the channel
    thumbnail_url = models.URLField(null=True, blank=True)
    # Provider of the channel as technical name (e.g. 'youtube')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name + ' - ' + self.provider.name

    def toDict(self):
        return {
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "channel_id": self.channel_id,
            "thumbnail_url": self.thumbnail_url,
            "provider": self.provider.toDict()
        }


class Episode(models.Model):
    # Title of the episode
    title = models.CharField(max_length=200)
    # Description of the episode if given
    description = models.TextField(null=True, blank=True)
    # Type of the episode (e.g. 'video' or 'audio')
    type = models.CharField(max_length=200, choices=[
        ('video', 'Video'),
        ('audio', 'Audio')
    ])
    # direct link to the player on the provider's website
    url = models.URLField()
    # id of the episode as used by the provider (e.g. on youtube the part '9bZkp7q19f0' for Gangnam style, https://www.youtube.com/watch?v=9bZkp7q19f0)
    episode_id = models.CharField(max_length=200, null=True, blank=True)
    # thumbnail url (max resolution)
    thumbnail_url = models.URLField(null=True, blank=True)
    # duration of the episode in seconds
    duration = models.IntegerField(null=True, blank=True)
    # number of views (if available)
    viewcount = models.IntegerField(null=True, blank=True)
    # date of publishing (if available)
    published = models.DateTimeField(null=True, blank=True)
    # date of last update (if available)
    updated = models.DateTimeField(null=True, blank=True)
    # channel the episode is published on
    publishing_channel = models.ForeignKey(PublishingChannel, on_delete=models.CASCADE)

    def __str__(self):
        return self.publishing_channel.name + ': ' + self.title


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publishing_channel = models.ForeignKey(PublishingChannel, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' - ' + self.publishing_channel.name


class HiddenEpisode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' - ' + self.episode.title
