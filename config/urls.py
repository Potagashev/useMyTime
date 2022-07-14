from django.contrib import admin
from django.urls import path, include

from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('', include('project.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += doc_urls
