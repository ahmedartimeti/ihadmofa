from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from accounts.views import profile_settings
from notifications import views as notification_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='planner:tasks', permanent=False), name='home'),
    path('settings/', profile_settings, name='settings'),
    path('accounts/', include('accounts.urls')),
    path('tasks/', include('planner.urls')),
    path('books/', include('books.urls')),
    path('meetings/', include('meetings.urls')),
    path('reports/', include('reports.urls')),
    path('notifications/', include('notifications.urls')),
    path('manifest.json', notification_views.manifest, name='pwa_manifest'),
    path('sw.js', notification_views.service_worker, name='service_worker'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
