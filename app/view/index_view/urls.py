from django.urls import path
from app.view.index_view import views

urlpatterns = [
    path('', views.index, name='index'),
]