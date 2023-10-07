from django.urls import path
from api import views

urlpatterns = [
    path('post/', views.PostView.as_view(), name='posts'),
    path('post/<str:pk>/', views.PostDetailView.as_view(), name='detail_post')
]
