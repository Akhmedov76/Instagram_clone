from django.urls import path

from app_accounts import *
from app_post.views import *

router = DefaultRouter()

router.register('post', post_views.PostView, basename='posts')
router.register('comment', post_views.CommentView, basename='comments')

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/', VerificationView.as_view(), name='verify_email'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('comment/<int:post_id>/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('like/<int:post_id>/', LikeCreateAPIView.as_view(), name='like-create'),
] + router.urls
