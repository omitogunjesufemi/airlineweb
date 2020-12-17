from django.urls import path
from app.view.login_view import views

urlpatterns = [
    path('login/', views.login_get, name='login'),
    path('login_post/', views.login_page_post, name='login_post'),
    path('logout/', views.logout_view, name='logout'),
]