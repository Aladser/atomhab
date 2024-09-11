from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from authen_drf.apps import AuthenDrfConfig
from authen_drf.views import *

app_name = AuthenDrfConfig.name

urlpatterns = [
    path('', UserListAPIView.as_view(), name='list'),
    path('<int:pk>', UserRetrieveAPIView.as_view(), name='detail'),
    path('<int:pk>/update', UserUpdateAPIView.as_view(), name='update'),
    path('<int:pk>/delete', UserDestroyAPIView.as_view(), name='delete'),

    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', LoginView.as_view(permission_classes = (AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes = (AllowAny,)), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]