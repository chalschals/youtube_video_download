
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from downloader.views import YoutubeDownloader
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', YoutubeDownloader)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
