from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Examples:
    url(r'^$', 'nebulosa.views.home', name='home'),
    url(r'^concepts$', 'nebulosa.views.concepts', name='concepts'),
    url(r'^nebulosa', 'nebulosa.views.related', name='nebulosa'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

