from django.urls import path
from . import views
urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(),name='register'),
    path('auth/login/',views.LoginView.as_view(),name='login'),
    path('auth/logout/',views.LogoutView.as_view(),name='logout'),
    path('auth/me/',views.ShowInformationView.as_view(),name='me')
]

