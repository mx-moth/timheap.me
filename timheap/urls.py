import wagtail.admin.urls
import wagtail.core.urls
import wagtail.documents.urls
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic.base import TemplateView
from wagtail.contrib.sitemaps.views import sitemap

from .views import ErrorView

handler404 = ErrorView.as_view(template_name='layouts/404.html', status=404)
handler500 = ErrorView.as_view(template_name='layouts/500.html', status=500)

urlpatterns = [
    path('robots.txt', TemplateView.as_view(
        content_type='text/plain', template_name='robots.txt')),
    path('sitemap.xml', sitemap),

    path('admin/', include(wagtail.admin.urls)),

    path('_docs/', include(wagtail.documents.urls)),

    path('404/', handler404),
    path('500/', handler500),

    path('', include(wagtail.core.urls)),
]


if settings.DEFAULT_FILE_STORAGE == \
        'django.core.files.storage.FileSystemStorage':
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
