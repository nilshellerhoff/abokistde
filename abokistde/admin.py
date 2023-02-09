from django.contrib import admin

from .models import PublishingChannel, Episode, Provider

class VideoInline(admin.TabularInline):
    model = Episode
    extra = 3

class PublishingChannelAdmin(admin.ModelAdmin):
    inlines = [VideoInline]
    model = PublishingChannel

admin.site.register(Provider)
admin.site.register(PublishingChannel, PublishingChannelAdmin)
admin.site.register(Episode)
