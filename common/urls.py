from django.urls import path

from app_accounts import views
from app_post.views import *

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('verify-email/', views.VerificationView.as_view(), name='verify_email'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('update/<int:pk>/', PostUpdateAPIView.as_view(), name='post-update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),

    path('comment/<int:post_id>/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('like/<int:post_id>/', LikeCreateAPIView.as_view(), name='like-create'),
]
