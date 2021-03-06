from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.index.as_view(), name="index"),
    path('admin/', admin.site.urls),
    path('home/', include('home.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
