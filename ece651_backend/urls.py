from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static('media/', document_root=settings.MEDIA_ROOT)
