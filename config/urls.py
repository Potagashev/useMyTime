from django.contrib import admin
from django.urls import path, include

from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('project/', include('project.urls')),
    path('project_properties/', include('project_properties.urls')),
    path('timer/', include('timer.urls')),
    path('program_timer/', include('programs_timer.urls')),
    path('report/', include('report.urls')),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += doc_urls
