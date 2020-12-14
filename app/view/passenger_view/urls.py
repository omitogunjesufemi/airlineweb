from django.urls import path
from app.view.passenger_view import views

urlpatterns = [
    path('register_passenger/<int:flight_id>/', views.register_passenger, name="register_passenger"),
    path('list_passenger/', views.list_passenger, name="list_passenger"),
    path('edit_passenger/<int:passenger_id>/', views.edit_passenger, name="edit_passenger"),
    path('passenger_details/<int:passenger_id>/', views.passenger_details, name="passenger_details"),
    path('delete_passenger/<int:passenger_id>/', views.delete_passenger, name="delete_passenger"),
]