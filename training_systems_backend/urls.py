from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

api_urls = [
    path("product/", include("apps.products.urls")),
    path("lesson/", include("apps.lessons.urls")),
]

urlpatterns = [
    path("api/", include((api_urls, ""))),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
