from django.urls import path
from .views import SignInView,SignUpView,MyTokenObtainPairView,ProfileView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
	path('signin/', SignInView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('token/',MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/',ProfileView.as_view(),name='profile')
]