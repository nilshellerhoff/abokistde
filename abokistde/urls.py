"""abokistde URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from . import views, management_urls
from . import legacy_urls
from api.urls import urlpatterns as api_urlpatterns

__DIR__ = os.path.dirname(__file__)

urlpatterns = [
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('account/', include('django_registration.backends.one_step.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path("account/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path('vuetify_app', views.index, name="home"),
]

urlpatterns += api_urlpatterns

urlpatterns += management_urls.urlpatterns

urlpatterns += legacy_urls.urlpatterns

# serving PWA app
dist_dir = os.path.join(__DIR__, '../frontend/dist/pwa')
static_files = [file for file in os.listdir(dist_dir) if file != 'index.html']

for path in static_files:
    urlpath = f"/{path.split('/')[-1]}"
    file_path = os.path.join(dist_dir, path)
    urlpatterns += static(urlpath, document_root=file_path)

urlpatterns += [
    re_path('', TemplateView.as_view(template_name="index.html")),
]