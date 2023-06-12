from django.urls import path
from django.conf import settings
from auth.login.views import AuthDropSigninView, AuthVendorSigninView
from auth.registration.views import AuthRegisterDropView, AuthRegisterVendorView
from auth.reset_password.views import AuthResetPasswordView
from auth.new_password.views import AuthNewPasswordView

app_name = 'auth'

urlpatterns = [
    path('vendor/login/', AuthVendorSigninView.as_view(template_name = 'pages/auth/login.html'), name='vendor-login'),
    path('vendor/registration/', AuthRegisterVendorView.as_view(template_name = 'pages/auth/registration.html'), name='signin'),

    path('dropshipper/login/', AuthDropSigninView.as_view(template_name = 'pages/auth/login.html'), name='signin'),
    path('dropshipper/registration/', AuthRegisterDropView.as_view(template_name = 'pages/auth/registration.html'), name='signin'),

    path('reset-password', AuthResetPasswordView.as_view(template_name = 'pages/auth/reset-password.html'), name='reset-password'),
    path('new-password', AuthNewPasswordView.as_view(template_name = 'pages/auth/new-password.html'), name='new-password'),
]