from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.AccountView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
