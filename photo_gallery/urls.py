from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.index, name='index'),
    # Photo upload and editing
    path('upload/', views.photo_upload, name='photo_upload'),
    path('upload/<int:photo_id>/', views.photo_upload, name='edit_photo'),
    # Photo detail and like
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('photo/<int:photo_id>/like/', views.like_photo, name='like_photo'),
    # delete photo
    path('photo/delete/<int:photo_id>/', views.photo_delete, name='photo_delete'),
    # Search
    path('search/', views.search_results, name='search_results'),
    # User profile and dashboard
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),  
    # Authentication views
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),     
    path('logout/', views.logout_view, name='logout'),   
]
