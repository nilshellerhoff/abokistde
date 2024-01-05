from django.urls import path, include

from abokistde.legacy_views import search_online
from rest_framework.authtoken import views

urlpatterns = [
    path('api/search_online/', search_online, name='search_online'),
    path('api/', include('api.viewset_urls')),
    path('api/token/', views.obtain_auth_token),

]
