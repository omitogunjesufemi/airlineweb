from django.urls import path
from app.view.aircraft_view import views

urlpatterns = [
    path('register/', views.register_aircraft, name="register_aircraft"),
    path('list_aircraft/', views.list_aircraft, name="list_aircraft"),
    path('aircraft_details/<int:aircraft_id>/', views.aircraft_details, name="aircraft_details"),
    path('edit_aircraft/<int:aircraft_id>/', views.edit_aircraft, name="edit_aircraft"),
    path('delete_aircraft/<int:aircraft_id>/', views.delete_aircraft, name="delete_aircraft"),
]
