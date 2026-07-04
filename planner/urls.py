from django.urls import path
from . import views

app_name = 'planner'
urlpatterns = [
    path('', views.task_list, name='tasks'),
    path('add/', views.task_create, name='task_add'),
    path('<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('<int:pk>/done/', views.task_done, name='task_done'),
    path('<int:pk>/defer/', views.task_defer, name='task_defer'),
    path('<int:pk>/remind/', views.task_remind, name='task_remind'),
    path('send-today-plan-email/', views.send_today_plan_email, name='send_today_plan_email'),
]
