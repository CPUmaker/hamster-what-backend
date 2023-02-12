from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('', include('core.urls')),
    # path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='ECE651 Backend API Document', description='This API document includes all ednpoints that has been implemented.')),
]

urlpatterns += static('media/', document_root=settings.MEDIA_ROOT)
