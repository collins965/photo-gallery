from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from photo_gallery.views import dashboard_view

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # App routes
    path('', include('photo_gallery.urls')),

    # Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),

    # Login/Logout
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'), name='login'),

    path('accounts/logout/', auth_views.LogoutView.as_view(
        next_page='login'), name='logout'),

    # Password change (for logged-in users)
    path('accounts/password/change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change_form.html'), name='password_change'),

    path('accounts/password/change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'), name='password_change_done'),

    # Password reset (for forgotten passwords via email)
    path('accounts/password/reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        success_url='/accounts/password/reset/done/'
    ), name='password_reset'),

    path('accounts/password/reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'), name='password_reset_done'),

    path('accounts/password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url='/accounts/password/reset/complete/'
    ), name='password_reset_confirm'),

    path('accounts/password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]

# Media files (development only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
