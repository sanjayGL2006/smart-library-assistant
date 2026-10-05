from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def kill_sw(request):
    return HttpResponse("self.registration.unregister();", content_type="application/javascript")

urlpatterns = [
    path("sw.js", kill_sw),
    path("django-admin/", admin.site.urls), 
    path("knowledge/", include("knowledge.urls")),
    path("", include("core.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
