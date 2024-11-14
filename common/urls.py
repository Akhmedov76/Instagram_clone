from django.urls import path

from app_accounts import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('verify-email/', views.VerificationView.as_view(), name='verify_email'),
]
