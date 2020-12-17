from app.view.booking_view import views
from django.urls import path

urlpatterns = [
    path('register_booking/<int:flight_id>', views.register_booking, name='register_booking'),
    path('edit_booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('booking_details/<int:booking_id>/', views.booking_details, name='booking_details'),
    path('list_booking/', views.list_booking, name='list_booking'),
    path('passenger_booking/', views.passenger_booking_list, name='passenger_booking'),
]