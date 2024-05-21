from django.contrib import admin
from .models import PublishingChannel, Episode, Provider, Extractor, UserSubscription, SubscriptionCategory
from abokistde import sites_wrapper

class VideoInline(admin.TabularInline):
    model = Episode
    extra = 3

class PublishingChannelAdmin(admin.ModelAdmin):
    inlines = [VideoInline]
    model = PublishingChannel
    search_fields = ['name', 'provider__name']
    list_display = ('name', 'provider', 'get_extractor')
    list_filter = ['provider__extractor']

    def get_extractor(self, obj: PublishingChannel):
        return obj.provider.extractor

class ProviderAdmin(admin.ModelAdmin):
    model = Provider
    search_fields = ['name']
    list_display = ('name', 'extractor')
    list_filter = ('extractor',)


def fetch_data(modeladmin, request, queryset):
    for extractor in queryset:
        sites_wrapper.fetch_data(extractor)

class ExtractorAdmin(admin.ModelAdmin):
    model = Extractor
    actions = [fetch_data]

admin.site.register(Extractor, ExtractorAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(PublishingChannel, PublishingChannelAdmin)
admin.site.register(Episode)
admin.site.register(UserSubscription)
admin.site.register(SubscriptionCategory)