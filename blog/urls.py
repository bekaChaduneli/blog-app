from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('blogs/', views.BlogList.as_view(), name='blog-list'),
    path('blogs/<int:pk>/', views.BlogDetail.as_view(), name='blog-detail'),
    path('blogs/<int:pk>/highlight/', views.BlogHighlight.as_view(), name='blog-highlight'),
    path('authors/', views.AuthorList.as_view(), name='user-list'),
    path('authors/<int:pk>/', views.AuthorDetail.as_view(), name='user-detail'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),  # New registration view
])