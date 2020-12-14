from django.urls import path
from app.view.flight_view import views

urlpatterns = [
    path('register_flight/', views.register_flight, name="register_flight"),
    path('list_flight/', views.list_flight, name="list_flight"),
    path('edit_flight/<int:flight_id>/', views.edit_flight, name="edit_flight"),
    path('flight_details/<int:flight_id>/', views.flight_details, name="flight_details"),
    path('delete_flight/<int:flight_id>/', views.delete_flight, name="delete_flight"),
]