from django.urls import path

from abokistde.management_views import migrate_view, collectstatic_view, createsuperuser_view

urlpatterns = [
    # Legacy endpoints for old frontend
    path('management/migrate', migrate_view, name='migrate'),
    path('management/collectstatic', collectstatic_view, name='collectstatic'),
    path('management/createsuperuser', createsuperuser_view, name='createsuperuser'),
]
