from django.urls import path
from .views import LoginView, account_logout, recover_password, register

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', account_logout, name='logout'),
    path('register/', register, name='register'),
    path('recover/', recover_password, name='recover'),
]
