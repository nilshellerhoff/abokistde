from django.urls import path, include

urlpatterns = [
    path('api/', include('api.viewset_urls')),
]
