from django.urls import path
from . import views
app_name = 'meetings'
urlpatterns = [
    path('', views.meeting_list, name='meetings'),
    path('add/', views.meeting_create, name='meeting_add'),
    path('<int:pk>/edit/', views.meeting_edit, name='meeting_edit'),
    path('<int:pk>/done/', views.meeting_done, name='meeting_done'),
    path('<int:pk>/defer/', views.meeting_defer, name='meeting_defer'),
    path('<int:pk>/delete/', views.meeting_delete, name='meeting_delete'),
]
