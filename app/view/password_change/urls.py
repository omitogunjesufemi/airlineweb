from django.urls import path
from app.view.password_change import views

urlpatterns = [
    path('change_password/', views.change_password, name='change_password'),
]