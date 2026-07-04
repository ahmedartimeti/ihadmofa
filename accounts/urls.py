from django.urls import path
from .views import LoginView, account_logout, register

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', account_logout, name='logout'),
    path('register/', register, name='register'),
]
