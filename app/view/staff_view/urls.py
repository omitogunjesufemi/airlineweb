from django.urls import path
from app.view.staff_view import views

urlpatterns = [
    path('', views.staff_home, name="staff_home"),
    path('edit_staff/', views.edit_staff, name="edit_staff"),
]
