from django.urls import path
from . import views

app_name = 'notifications'
urlpatterns = [
    path('push/public-key/', views.public_key, name='push_public_key'),
    path('push/subscribe/', views.subscribe, name='push_subscribe'),
    path('push/unsubscribe/', views.unsubscribe, name='push_unsubscribe'),
    path('push/test/', views.test_push, name='push_test'),
]
