from django.urls import path
from . import views
app_name = 'books'
urlpatterns = [
    path('', views.book_list, name='books'),
    path('add/', views.book_create, name='book_add'),
    path('<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('<int:pk>/delete/', views.book_delete, name='book_delete'),
]
